# Leases Recover Abandoned Work; Fencing Rejects the Old Owner

> **Who this is for**: Engineers implementing worker ownership for jobs that may outlive a process, connection, or deployment.

Before reading this, see how the job is created atomically in **[Atomic Transitions and Outbox](01_atomic_transitions_and_outbox.md)**.

---

## 1. RUNNING becomes permanent when its owner dies

Worker A changes a job from PENDING to RUNNING, then its container is killed. A status flag or a session lock cannot answer whether A will return, so the job remains stuck or an operator resets it blindly.

text
Worker A claims job-55
  → jobs.status = RUNNING
  → A crashes
  → no finally block runs
  → job-55 stays RUNNING forever


A **lease** makes ownership temporary. The claim records an expiry; heartbeats move it forward; another worker may recover the job after the expiry.

text
10:00:00  A claims until 10:01:30
10:00:30  A heartbeats until 10:02:00
10:00:41  A crashes
10:02:00  lease expires
10:02:01  B recovers and claims


That still leaves one danger: A may be partitioned rather than dead and return after B claims. Every attempt therefore gets a unique **attempt token** used as a fencing predicate.

> **The near-miss**: worker_id looks like a fencing value. A deployment can reuse the same pod name, process label, or logical worker ID, letting an old process match a later attempt. Keep worker_id for logs; generate a fresh token on every claim.

---

## 2. Claim only work that can execute now

The worker calculates its free slots before entering the claim transaction:

sql
WITH candidates AS (
    SELECT id
    FROM jobs
    WHERE status = 'PENDING'
      AND next_attempt_at <= now()
    ORDER BY priority DESC, next_attempt_at, created_at
    FOR UPDATE SKIP LOCKED
    LIMIT :available_slots
)
UPDATE jobs AS j
SET status = 'RUNNING',
    attempt = attempt + 1,
    attempt_token = gen_random_uuid(),
    worker_id = :worker_id,
    lease_expires_at = now() + interval '90 seconds',
    started_at = COALESCE(started_at, now())
FROM candidates
WHERE j.id = candidates.id
RETURNING j.id, j.attempt, j.attempt_token, j.lease_expires_at;


One row might become:

text
job-55 | RUNNING | attempt=1 | token-a | worker-A | expires=10:01:30


**Invariant**: each returned row immediately occupies one execution slot. No claimed job waits behind an in-memory semaphore while its lease is renewed.

SKIP LOCKED prevents claimers from waiting on one another; it does not make the selection fair. Keep a matching partial index, measure oldest-ready age by priority/tenant, and add aging or reserved capacity when strict priority starves work.

---

## 3. Heartbeat success is a precondition for continuing

Renew with database time and the unique token:

sql
UPDATE jobs
SET lease_expires_at = now() + interval '90 seconds'
WHERE id = :job_id
  AND status = 'RUNNING'
  AND attempt_token = :attempt_token
  AND lease_expires_at > now()
RETURNING lease_expires_at;


Exactly one returned row means the attempt still owns the lease. Zero rows means it expired, was recovered, was cancelled, or already terminated. The worker cancels its local operation and enters a fenced state in which it may record diagnostic evidence but may not mutate job or workflow rows.

Run heartbeats in a lightweight task independent from the provider call. The work supervisor contract is:

text
provider task ───────────────┐
                            ├── first failure cancels the sibling
heartbeat task ──────────────┘
                                  │
                                  └── no completion unless last heartbeat succeeded


⚠️ Logging a heartbeat exception and letting work continue creates the exact stale-worker race the lease was supposed to control.

Choose a lease several times longer than normal heartbeat jitter and shorter than the maximum acceptable recovery delay. A common starting ratio is heartbeat every one-third of the lease, then tune from measured scheduler pauses, database latency, and provider behavior. Use the database's clock for claim, heartbeat, and expiry comparisons so worker clock skew cannot steal or extend ownership.

---

## 4. Recovery replaces the token before work resumes

When A's lease expires, a bounded reconciler first returns the job to PENDING:

sql
WITH expired AS (
    SELECT id, attempt_token
    FROM jobs
    WHERE status = 'RUNNING'
      AND lease_expires_at <= now()
    ORDER BY lease_expires_at
    FOR UPDATE SKIP LOCKED
    LIMIT :repair_limit
)
UPDATE jobs AS j
SET status = 'PENDING',
    next_attempt_at = now(),
    attempt_token = NULL,
    worker_id = NULL,
    lease_expires_at = NULL,
    last_error_class = COALESCE(last_error_class, 'LEASE_EXPIRED'),
    last_error = COALESCE(last_error, 'worker stopped heartbeating')
FROM expired
WHERE j.id = expired.id
  AND j.status = 'RUNNING'
  AND j.attempt_token = expired.attempt_token
RETURNING j.id;


Worker B then uses the normal claim and receives a new token:

text
job-55 | RUNNING | attempt=2 | token-b | worker-B | expires=10:03:31


Do not reuse token-a, even when the same worker process immediately retries. The token identifies one ownership epoch, not an executor identity.

> **Key insight**: Expiry decides when another attempt may start; the token decides whose late writes are still valid. A lease without fencing recovers availability but not correctness.

---

## 5. Every terminal write uses the same fence

Completion is conditional on current ownership:

sql
UPDATE jobs
SET status = 'SUCCEEDED',
    result_ref = :result_ref,
    finished_at = now(),
    attempt_token = NULL,
    worker_id = NULL,
    lease_expires_at = NULL
WHERE id = :job_id
  AND status = 'RUNNING'
  AND attempt_token = :attempt_token
  AND lease_expires_at > now()
RETURNING id;


Retry scheduling, permanent failure, workflow completion, and compensation scheduling use the same token in their transaction. Application code must check that exactly one row changed before acknowledging the message or reporting success.

text
10:02:01  B owns token-b
10:02:05  partitioned A returns with token-a
10:02:06  A completion UPDATE → 0 rows
10:02:07  B completion UPDATE → 1 row


Preserve A's external response in logs or a quarantine record; do not overwrite B. [Idempotency and External Effects](03_idempotency_and_external_effects.md) decides whether the provider result can be adopted safely.

---

## 6. A lease does not make a provider effect exactly once

A loses its lease while an HTTP request is already inside the provider. B starts after expiry and sends the same business request. Database fencing rejects A's local completion, but it cannot recall either network request.

Use a stable provider idempotency key across token-a and token-b. The attempt token protects local writes; the operation key protects the business effect. They must not be the same value because their lifetimes differ.

⚠️ A lease shorter than routine provider latency causes healthy work to be recovered and replayed. Heartbeat it or split the task; do not merely increase it beyond the maximum acceptable recovery delay.

⚠️ A lease longer than deployment and incident recovery targets leaves dead work invisible for too long. Measure time-to-reclaim, not only heartbeat success.

---

## 7. A failure-injection test proves the stale owner loses

The following PostgreSQL script is self-contained. It pauses A beyond expiry, recovers and claims as B, then asserts that A cannot complete:

sql
CREATE TEMP TABLE lease_test_jobs (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL,
    attempt INTEGER NOT NULL DEFAULT 0,
    attempt_token TEXT,
    lease_expires_at TIMESTAMPTZ,
    result_ref TEXT
);

INSERT INTO lease_test_jobs (id, status) VALUES (55, 'PENDING');

UPDATE lease_test_jobs
SET status = 'RUNNING',
    attempt = 1,
    attempt_token = 'token-a',
    lease_expires_at = clock_timestamp() + interval '100 milliseconds'
WHERE id = 55 AND status = 'PENDING';

SELECT pg_sleep(0.15);

UPDATE lease_test_jobs
SET status = 'PENDING', attempt_token = NULL, lease_expires_at = NULL
WHERE id = 55
  AND status = 'RUNNING'
  AND attempt_token = 'token-a'
  AND lease_expires_at <= clock_timestamp();

UPDATE lease_test_jobs
SET status = 'RUNNING',
    attempt = 2,
    attempt_token = 'token-b',
    lease_expires_at = clock_timestamp() + interval '10 seconds'
WHERE id = 55 AND status = 'PENDING';

DO $$
DECLARE
    changed INTEGER;
BEGIN
    UPDATE lease_test_jobs
    SET status = 'SUCCEEDED', result_ref = 'stale-a'
    WHERE id = 55 AND status = 'RUNNING' AND attempt_token = 'token-a';
    GET DIAGNOSTICS changed = ROW_COUNT;
    IF changed <> 0 THEN
        RAISE EXCEPTION 'stale token-a completed the job';
    END IF;

    UPDATE lease_test_jobs
    SET status = 'SUCCEEDED', result_ref = 'current-b'
    WHERE id = 55 AND status = 'RUNNING' AND attempt_token = 'token-b';
    GET DIAGNOSTICS changed = ROW_COUNT;
    IF changed <> 1 THEN
        RAISE EXCEPTION 'current token-b failed to complete the job';
    END IF;
END $$;

SELECT status, attempt, result_ref FROM lease_test_jobs WHERE id = 55;


The final row is SUCCEEDED | 2 | current-b. If it contains stale-a, any completion path omitted the token predicate.

**How you know it is working**: token-mismatch updates stay at zero, expired-lease recovery time stays within its SLO, and lost-heartbeat metrics correlate with worker restarts or event-loop stalls.

Do not use leases to coordinate a short database-only transaction; a row lock already has a failure-aware owner in the database session. Do not rely on leases alone for irreversible external effects.

---

**Next**: [Idempotency and External Effects](03_idempotency_and_external_effects.md)


εξήγησε μου λίγο αυτό. Το lease είναι πόση ώρα ένα request παραμενει inflight γι να αποφυγουμε stucked πραγματα. Το heartbeat ειναι σημα οτι ακομα κανει process, οποτε κανει prolong το lease ετσι?
Ναι, αυτή είναι η βασική ιδέα. Απλώς θα το έλεγα λίγο πιο ακριβώς:
Το lease δεν είναι το πόσο επιτρέπεται συνολικά να τρέχει το request/job. Είναι το:

«Μέχρι πότε θεωρούμε ότι αυτός ο συγκεκριμένος worker εξακολουθεί να έχει ownership αυτού του job, αν δεν ακούσουμε ξανά από αυτόν.»
Παράδειγμα:
12:00:00  Worker A κάνει claim το job
          lease_expires_at = 12:01:30

12:00:30  heartbeat
          lease_expires_at = 12:02:00

12:01:00  heartbeat
          lease_expires_at = 12:02:30

12:01:30  heartbeat
          lease_expires_at = 12:03:00
Άρα ναι: το heartbeat λέει "είμαι ακόμα ζωντανός και το επεξεργάζομαι" και παρατείνει το lease.
Αν όμως ο worker πεθάνει:

12:00:00  claim
          lease → 12:01:30

12:00:30  heartbeat
          lease → 12:02:00

12:00:41  💥 worker crashes

          κανένα άλλο heartbeat

12:02:00  lease expires

12:02:01  άλλος worker μπορεί να πάρει το job
Οπότε το lease λύνει ακριβώς το πρόβλημα που λες: να μην έχεις ένα job:
RUNNING
για πάντα επειδή το container/process που το εκτελούσε πέθανε.
Αλλά το σημαντικό κομμάτι είναι το fencing token
Το lease από μόνο του δεν αρκεί.
Φαντάσου:

A έχει job
token = abc
lease expires 12:02

12:02  θεωρούμε ότι A πέθανε

B παίρνει το job
token = xyz

12:02:10  ο A ξαφνικά ξαναεμφανίζεται
Μπορεί ο A να μην είχε πεθάνει πραγματικά. Μπορεί απλώς να είχε:
network partition
event loop stall
DB connectivity issue
τεράστιο GC/pause
provider call που κόλλησε
Τότε έχεις δύο workers που νομίζουν ότι δουλεύουν το ίδιο πράγμα.
Γι' αυτό κάθε claim παίρνει νέο:

attempt_token
π.χ.
Attempt 1:
Worker A
token-a

Attempt 2:
Worker B
token-b
Και όταν κάνουν completion:
UPDATE jobs
SET status = 'SUCCEEDED'
WHERE id = 55
  AND attempt_token = :my_token
  AND lease_expires_at > now();
Ο A επιστρέφει με:
token-a
αλλά πλέον η DB έχει:
token-b
οπότε:
A → UPDATE 0 rows ❌
B → UPDATE 1 row  ✅
Αυτό είναι το fencing.
Άρα κράτα αυτό το mental model:

Lease
  = "μέχρι πότε έχεις το δικαίωμα να θεωρείσαι owner"

Heartbeat
  = "είμαι ακόμα ζωντανός → παράτεινε το ownership μου"

Lease expiry
  = "δεν σε εμπιστεύομαι πλέον → κάποιος άλλος μπορεί να πάρει τη δουλειά"

Attempt token / fencing token
  = "ακόμη κι αν επιστρέψεις αργότερα, δεν μπορείς να γράψεις πάνω
     στο αποτέλεσμα του νέου owner"
Και μια σημαντική διόρθωση στο "request remains inflight": συνήθως μιλάμε περισσότερο για το job execution παρά για το HTTP request. Το HTTP request μπορεί ήδη να έχει πάρει 202 Accepted και να έχει τελειώσει εδώ και πολλή ώρα, ενώ το background job συνεχίζει με lease + heartbeat.
άρα το fencing είναι idempotency token?
Όχι — είναι διαφορετικά πράγματα, αν και μοιάζουν επειδή και τα δύο είναι “tokens”.
Fencing token = προστατεύει το ownership του attempt. Απαντά: «Είσαι ακόμα ο τωρινός νόμιμος worker για αυτό το job;»

Attempt 1 → token-a
Attempt 2 → token-b
Αν ο παλιός worker επιστρέψει με token-a, η DB τον απορρίπτει γιατί πλέον ισχύει token-b.
Idempotency key = προστατεύει τη business operation από duplicate execution. Απαντά: «Έχουμε ήδη εκτελέσει αυτή τη λογική πράξη;»

Παράδειγμα, αν το job κάνει payment:

job attempt 1:
  fencing token = token-a
  idempotency key = payment-123

job attempt 2:
  fencing token = token-b
  idempotency key = payment-123
Πρόσεξε ότι το fencing token αλλάζει σε κάθε retry/claim, ενώ το idempotency key συνήθως μένει ίδιο για όλα τα retries της ίδιας business operation.
Ο λόγος είναι αυτός:

A → στέλνει payment στον provider
A → χάνει lease

B → παίρνει το job

A → επιστρέφει αργότερα
Το fencing:
A cannot update DB ✅
αλλά δεν μπορεί να αναιρέσει το HTTP request που ήδη έστειλε στον payment provider.
Εκεί χρειάζεσαι idempotency:

A → POST payment, key=payment-123
B → POST payment, key=payment-123

Provider:
"payment-123 το έχω ήδη κάνει"
→ δεν χρεώνει δεύτερη φορά
Οπότε:
fencing token
    προστατεύει ownership / DB writes
    lifetime = ένα attempt

idempotency key
    προστατεύει business side effect
    lifetime = ολόκληρη η logical operation
Αυτό είναι και το πιο σημαντικό σημείο του κειμένου: δεν πρέπει να χρησιμοποιήσεις το fencing token ως idempotency key, γιατί στο retry αλλάζει ακριβώς όταν θέλεις το idempotency key να παραμείνει ίδιο.





Σύνοψη του pattern που συζητήσαμε:

* **Η DB είναι το source of truth.** Δεν βασίζεσαι στο queue για να ξέρεις ποια δουλειά πρέπει να γίνει.
* Όταν έρχεται π.χ. `POST /runs`, μέσα σε **ένα DB transaction** γράφεις:

  * το `workflow_run`
  * το `job/step`
  * ένα **outbox record** που λέει «αυτό πρέπει να γίνει publish».
* Μετά το `COMMIT`, ένας ξεχωριστός outbox publisher διαβάζει τα pending records και τα στέλνει στο queue.
* Αυτό λύνει το failure window:

  ```text
  DB commit ✅
  process crash 💥
  queue publish ❌
  ```

  γιατί το pending outbox record παραμένει στη DB και μπορεί να γίνει retry.

Το queue message καλό είναι να μεταφέρει κυρίως:

```text
run_id
step_id
event/message_id
expected_version
idempotency key
```

και **όχι ολόκληρο αντίγραφο του authoritative object**. Ο worker παίρνει τα IDs και ξαναδιαβάζει το τρέχον state από τη DB.

Ο worker επίσης πρέπει να προστατεύεται από duplicates και stale messages. Συνήθως αυτό γίνεται με:

* **idempotency / processed message ID** για duplicate delivery
* **expected version** για optimistic concurrency

π.χ.:

```sql
UPDATE workflow_step
SET status = 'completed',
    version = version + 1
WHERE id = :step_id
  AND version = :expected_version;
```

Αν το `version` έχει ήδη αλλάξει, το message είναι stale και δεν επιτρέπεται να αλλάξει ξανά το state.

Υπάρχει και δεύτερο failure window:

```text
POST /runs
   ↓
DB COMMIT ✅
   ↓
API crashes πριν στείλει HTTP response 💥
```

Ο client δεν ξέρει ότι το request πέτυχε και μπορεί να το ξαναστείλει. Εκεί χρησιμοποιείς **Idempotency-Key**:

```http
POST /runs
Idempotency-Key: abc-123
```

και στη DB:

```text
idempotency_key UNIQUE
```

Αν έρθει ξανά το ίδιο logical request με το ίδιο key, **δεν δημιουργείς δεύτερο run**· επιστρέφεις το ήδη υπάρχον.

Άρα τα δύο βασικά reliability mechanisms είναι:

```text
HTTP request → DB
      │
      └── Idempotency Key
          προστατεύει από client retries

DB → Queue
      │
      └── Transactional Outbox
          προστατεύει από crash μεταξύ commit και publish

Queue → Worker → DB
      │
      ├── Message/Event ID
      │   προστατεύει από duplicate delivery
      │
      └── Expected Version
          προστατεύει από stale/concurrent work
```

Το βασικό mental model είναι:

> **Πρώτα κάνεις durable στη DB το τι πρέπει να συμβεί. Μετά όλα τα υπόλοιπα μπορούν να γίνουν retry.**

Δεν προσπαθείς να κάνεις «DB commit + queue publish + HTTP response» magically atomic. Αντίθετα, σχεδιάζεις το σύστημα έτσι ώστε οποιοδήποτε βήμα μετά το DB commit να μπορεί να επαναληφθεί με ασφάλεια.




ετσι θα φαινοταν ενα db template για jobs 

Ναι — για ένα generic production-grade `jobs` table με retries, lease, fencing, idempotency και observability, θα έβαζα περίπου αυτό:

```sql
CREATE TABLE jobs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- What this job is
    job_type            TEXT NOT NULL,
    payload             JSONB NOT NULL,
    result_ref          TEXT,

    -- Business-level deduplication
    idempotency_key     TEXT NOT NULL,

    -- State machine
    status              TEXT NOT NULL
                        CHECK (status IN (
                            'PENDING',
                            'RUNNING',
                            'SUCCEEDED',
                            'FAILED',
                            'CANCELLED'
                        )),

    -- Scheduling / retries
    priority            INTEGER NOT NULL DEFAULT 0,
    attempt             INTEGER NOT NULL DEFAULT 0,
    max_attempts        INTEGER NOT NULL DEFAULT 3,
    next_attempt_at     TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Current ownership / lease
    worker_id           TEXT,
    attempt_token       UUID,
    lease_expires_at    TIMESTAMPTZ,

    -- Failure information
    last_error_class    TEXT,
    last_error          TEXT,

    -- Timestamps
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    started_at          TIMESTAMPTZ,
    finished_at         TIMESTAMPTZ,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Optional optimistic concurrency
    version             BIGINT NOT NULL DEFAULT 0
);
```

Και conceptually:

| Field              | Τι λύνει                                 |
| ------------------ | ---------------------------------------- |
| `id`               | identity του job                         |
| `job_type`         | τι worker/handler πρέπει να το εκτελέσει |
| `payload`          | input                                    |
| `result_ref`       | reference στο αποτέλεσμα                 |
| `idempotency_key`  | αποτρέπει duplicate logical jobs/effects |
| `status`           | lifecycle                                |
| `priority`         | scheduling order                         |
| `attempt`          | πόσες φορές έχει γίνει claim             |
| `max_attempts`     | πότε σταματάμε retries                   |
| `next_attempt_at`  | retry/backoff scheduling                 |
| `worker_id`        | debugging / observability                |
| `attempt_token`    | **fencing token** του τωρινού attempt    |
| `lease_expires_at` | πότε χάνει ownership ο worker            |
| `last_error_*`     | debugging / retry decisions              |
| timestamps         | auditing / metrics                       |
| `version`          | optimistic concurrency, αν τη χρειάζεσαι |

Θα πρόσθετα και constraints/indexes, γιατί εκεί γίνεται πραγματικά production-grade:

```sql
CREATE UNIQUE INDEX jobs_idempotency_key_uq
ON jobs (idempotency_key);

CREATE INDEX jobs_ready_idx
ON jobs (priority DESC, next_attempt_at, created_at)
WHERE status = 'PENDING';

CREATE INDEX jobs_expired_leases_idx
ON jobs (lease_expires_at)
WHERE status = 'RUNNING';
```

Και ένα πολύ χρήσιμο consistency constraint:

```sql
ALTER TABLE jobs
ADD CONSTRAINT jobs_running_ownership_check
CHECK (
    (
        status = 'RUNNING'
        AND attempt_token IS NOT NULL
        AND worker_id IS NOT NULL
        AND lease_expires_at IS NOT NULL
    )
    OR
    status <> 'RUNNING'
);
```

### Πώς θα το σκεφτόμουν

Έχεις ουσιαστικά 4 διαφορετικά concepts μέσα στην ίδια row:

```text
Logical Job
────────────────────────
id
job_type
payload
idempotency_key


Scheduling
────────────────────────
status
priority
attempt
max_attempts
next_attempt_at


Current Ownership
────────────────────────
worker_id
attempt_token
lease_expires_at


History / diagnostics
────────────────────────
created_at
started_at
finished_at
last_error
result_ref
```

Το σημαντικότερο είναι να μην μπλέξεις αυτά τα IDs:

```text
job.id
    = "ποια δουλειά είναι αυτή"

idempotency_key
    = "ποια logical business operation είναι αυτή"

attempt_token
    = "ποιος έχει ownership αυτή τη στιγμή"

worker_id
    = "ποιος executor την εκτελεί"
```

Παράδειγμα μετά από crash/retry:

```text
id               = job-55
idempotency_key  = generate-report-customer-123

attempt           = 2
attempt_token     = token-b
worker_id         = worker-7
lease_expires_at  = 13:05:30
```

Το `id` και το `idempotency_key` παραμένουν ίδια.

Τα:

```text
attempt
attempt_token
worker_id
lease_expires_at
```

αλλάζουν καθώς αλλάζει ownership.

### Ένα field που προσωπικά θα πρόσθετα

Αν το job ανήκει σε workflow/run:

```sql
workflow_id UUID,
step_id     TEXT
```

ή γενικότερα:

```sql
run_id      UUID,
```

και ίσως:

```sql
tenant_id TEXT,
```

σε multi-tenant σύστημα.

Άρα ένα αρκετά πλήρες real-world row μπορεί να είναι:

```text
id
run_id
step_id
tenant_id

job_type
payload
result_ref

idempotency_key

status
priority

attempt
max_attempts
next_attempt_at

worker_id
attempt_token
lease_expires_at

last_error_class
last_error

version

created_at
updated_at
started_at
finished_at
```

Αυτό είναι ήδη **πολύ καλό reusable template** για SQS/Kafka/DB-polling workers, χωρίς να γίνει υπερβολικά framework-specific.

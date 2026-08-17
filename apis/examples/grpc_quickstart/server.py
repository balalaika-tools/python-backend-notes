import asyncio

import grpc

import orders_pb2
import orders_pb2_grpc


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    async def GetOrder(self, request, context):
        if request.order_id != "ord_42":
            await context.abort(grpc.StatusCode.NOT_FOUND, "order not found")
        return orders_pb2.Order(order_id=request.order_id, status="shipped")


async def main() -> None:
    server = grpc.aio.server()
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    address = "127.0.0.1:50051"
    server.add_insecure_port(address)  # Loopback-only learning baseline.
    await server.start()
    print(f"server ready on {address}", flush=True)
    try:
        await server.wait_for_termination()
    finally:
        await server.stop(grace=0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

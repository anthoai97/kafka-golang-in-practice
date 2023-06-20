

import asyncio
import logging

import grpc

import helloworld_pb2, helloworld_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
	# target = "http://localhost:8080"
	asyncio.run(run())
	# agent = HttpAgent(target=target)
	# agent.ping()
	# data = "Data "
	# for x in range(20):
	# 	time.sleep(1)
	# 	data = "Data " + str(x)
	# 	agent.sendInterval({'data' : "data {}".format(x)})
		
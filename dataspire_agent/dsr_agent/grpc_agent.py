

import logging
import time
import grpc
from http_agent import AppType
from grpc_status import rpc_status
from google.rpc import error_details_pb2
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import dsr_agent_pb2_grpc
import dsr_agent_pb2

_LOGGER = logging.getLogger(__name__)

class GRPCAgent:
	def __init__(
		self: AppType,
		*,
		agentName: str = "DataSpire Agent",
		target: str = "localhost:8080",
		timeout: int = 300, # Secconds
		interval: int = 3, # Secconds
	) -> None:
		self.target = target
		self.timeout = timeout
		self.interval = interval
		self.datas = []
		self.savedTime = None
		self.agentName = agentName
		self.channel = grpc.insecure_channel(self.target)

	def _handleError(self, rpc_error: grpc.RpcError):
		_LOGGER.error('Call failure: %s', rpc_error)
		status = rpc_status.from_call(rpc_error)
		for detail in status.details:
			if detail.Is(error_details_pb2.QuotaFailure.DESCRIPTOR):
				info = error_details_pb2.QuotaFailure()
				detail.Unpack(info)
				_LOGGER.error('Quota failure: %s', info)
			else:
				_LOGGER.error('Unexpected failure: %s' % detail)

	def send(self) -> None:
		stub = dsr_agent_pb2_grpc.AgentStub(self.channel)
		try:
			response = stub.SendAgentMessage(dsr_agent_pb2.AgentMessage(name="yuo"))
			logging.info("Greeter client received: " + response.message)
		except grpc.RpcError as rpc_error:
			self._handleError(rpc_error=rpc_error)



if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
	target = "localhost:50051"
	agent = GRPCAgent(target=target, healthCheck=True)
	# agent.health_check_call()
	# asyncio.run(run())
	# agent = HttpAgent(target=target)
	# agent.ping()
	# data = "Data "
	# for x in range(20):
	# 	time.sleep(1)
	# 	data = "Data " + str(x)
	# 	agent.sendInterval({'data' : "data {}".format(x)})
		
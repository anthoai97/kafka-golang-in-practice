from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import threading
import time
import grpc
from message_package import MessagePackage
from http_agent import AppType
from logger import logger
from datetime import datetime, timedelta
import dsr_agent_pb2_grpc

class GRPCAgent:
	def __init__(
		self: AppType,
		*,
		agent_id: str = "dataspire-agent",
		agent_name: str = "DataSpire Agent",
		target: str = "localhost:8080",
		timeout: int = 10, # Secconds
		interval: int = 0, # Secconds
	) -> None:
		self.agent_id = agent_id
		self.agent_name = agent_name
		self.target = target
		self.timeout = timeout
		self.interval = interval
		self.channel = grpc.insecure_channel(self.target)
		self.msgPack: MessagePackage = self._createMessagePackage()

	def _handleError(self, rpc_error: grpc.RpcError):
		logger.error(f"Call failed with code: {rpc_error.code()}")
		logger.error(f"Call failed with code: {rpc_error.debug_error_string()}")

	def _createMessagePackage(self) -> MessagePackage:
		now = datetime.now()
		return MessagePackage(
			agent_id = self.agent_id,
			agent = self.agent_name,
			deadline = now + timedelta(seconds= self.interval),
		)
	
	def send(self, data: any) -> None:
		self.msgPack.setData(data=data)
		if(self.msgPack.isReachDeadline() == False):
			return;
		# Async call
		thread = threading.Thread(target=self._executeRemote, args=(self.msgPack,), daemon=True)
		thread.start()
		self.msgPack = self._createMessagePackage()
	
	def _executeRemote(self, msgPack: MessagePackage) -> None:
		try:
			logger.info("Start execute send message")
			stub = dsr_agent_pb2_grpc.DsrAgentStub(self.channel)
			response = stub.SendMessage(msgPack.toGRPCMessagePackage(), timeout= self.timeout)
			logger.info("Send message success: " + response.message)
		except grpc.RpcError as rpc_error:
			msgPack.setResend()
			self._handleError(rpc_error=rpc_error)

def run():
	target = "localhost:50051"
	agent = GRPCAgent(target=target)
	data = "Data "
	# async with asyncio.TaskGroup() as tg:
	for x in range(20):
		data = "Data " + str(x)
		time.sleep(0)
		# agent.send(data={'request' : data}),
		agent.send(data={'request' : data},)
			# logger.info(f"Call failed with code: {x}")
			# data = "Data " + str(x)
			# tg.create_task(agent.send(data={'request' : data},))

if __name__ == "__main__":
	run()

		
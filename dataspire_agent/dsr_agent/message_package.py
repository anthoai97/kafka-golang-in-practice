import time
from datetime import datetime
from dsr_agent_pb2 import GRPCMessagePackage

class MessagePackage:
	def __init__(
		self,
		agent: str  = "DataSpire",
		agent_id: str = "dataspire-agent",
		deadline: datetime = datetime.now()
	) -> None:
		self.agent_id = agent_id
		self.agent = agent
		self.deadline = deadline
		self.data = []
		self.resend = 0

	def setData(self, data: any):
		self.data.append(data)

	def toMessage(self):
		return {
			'agent': self.agent,
			'agent_id': self.agent_id,
			'data': self.data,
			'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			'resend': self.resend,
		}
	
	def toGRPCMessagePackage(self) -> GRPCMessagePackage:
		return GRPCMessagePackage(
			agent =self.agent,
			agent_id = self.agent_id,
			data= str(self.data),
			timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			resend = self.resend,
		)

	def isReachDeadline(self) -> bool:
		now = datetime.now()
		if now < self.deadline:
			return False
		else:
			return True
		
	def setResend(self):
		self.resend += 1
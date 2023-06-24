import time
from datetime import datetime

class MessagePackage:
	def __init__(
		self,
		agent: str  = "DataSpire",
		deadline: datetime = datetime.now()
	) -> None:
		self.agent = agent
		self.deadline = deadline
		self.data = []
		self.resend = 0

	def setData(self, data: any):
		self.data.append(data)

	def toMessage(self):
		return {
			'agent': self.agent,
			'data': self.data,
			'timestamp': time.mktime(datetime.now().timetuple()),
			'resend': self.resend,
		}

	def isReachDeadline(self) -> bool:
		now = datetime.now()
		if now < self.deadline:
			return False
		else:
			return True
		
	def setResend(self):
		self.resend += 1
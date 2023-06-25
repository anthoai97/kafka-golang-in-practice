from datetime import datetime, timedelta
import json
import threading
from typing import TypeVar
from logger import logger
import requests

from message_package import MessagePackage

AppType = TypeVar("AppType")

class HttpAgent:
	def __init__(
		self: AppType,
		*,
		agent_id: str = "dataspire-agent",
		agent_name: str = "DataSpire Agent",
		target: str = "localhost:8080",
		path: str = "/webhook",
		timeout: int = 300,
		interval: int = 0,
	) -> None:
		self.agent_id = agent_id
		self.agent_name = agent_name
		self.target = target
		self.path = path
		self.timeout = timeout
		self.interval = interval
		self.msgPack: MessagePackage = self._createMessagePackage()

	def _createMessagePackage(self) -> MessagePackage:
		now = datetime.now()
		return MessagePackage(
			agent_id = self.agent_id,
			agent = self.agent_name,
			deadline = now + timedelta(seconds= self.interval),
		)

	def ping(self):
		try:
			url = self.target + '/ping'
			r = requests.get(url)
			r.raise_for_status()
			logger.info(r.json())
		except requests.exceptions.HTTPError as err:
			logger.error(err)

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
			url = self.target + self.path
			body = msgPack.toMessage()
			r = requests.post(
				url, timeout=self.timeout,
				data=json.dumps(body),
				headers={
					"Content-Type":"application/json",
					'Accept': 'text/plain'
					}
				)
			r.raise_for_status()
			logger.info(str(r.status_code) + ' => ' + str(body))
		except requests.exceptions.HTTPError as err:
			msgPack.setResend()
			logger.error(err)

if __name__ == "__main__":
	target = "http://localhost:8080"
	agent = HttpAgent(target=target)
	# agent.ping()
	data = "Data "
	for x in range(20):
		data = "Data " + str(x)
		# logger.info(data)
		agent.send({'request' : "data {}".format(x)})
		
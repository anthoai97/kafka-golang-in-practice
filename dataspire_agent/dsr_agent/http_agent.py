from datetime import datetime, timedelta
import json
import logging
import time
from typing import TypeVar
import requests

from message_package import MessagePackage

AppType = TypeVar("AppType")

class HttpAgent:
	def __init__(
		self: AppType,
		*,
		agentName: str = "DataSpire Agent",
		target: str = "localhost:8080",
		path: str = "/webhook",
		timeout: int = 300,
		interval: int = 0,
	) -> None:
		self.agentName = agentName
		self.target = target
		self.path = path
		self.timeout = timeout
		self.interval = interval
		self.msgPack = self._initMessagePackage()

	def _initMessagePackage(self) -> MessagePackage:
		now = datetime.now()
		return MessagePackage(
			agent = self.agentName,
			deadline = now + timedelta(seconds= self.interval),
		)

	def ping(self):
		try:
			url = self.target + '/ping'
			r = requests.get(url)
			r.raise_for_status()
			logging.info(r.json())
		except requests.exceptions.HTTPError as err:
			logging.error(err)

	def send(self, data: any):
		try:
			self.msgPack.setData(data=data)
			
			if(self.msgPack.isReachDeadline() == False):
				return;
		
			url = self.target + self.path
			body = self.msgPack.toMessage()
			r = requests.post(
				url, timeout=self.timeout,
				data=json.dumps(body),
				headers={
					"Content-Type":"application/json",
					'Accept': 'text/plain'
					}
				)
			r.raise_for_status()
			logging.info(str(r.status_code) + ' => ' + str(body))
			self.msgPack = self._initMessagePackage()
		except requests.exceptions.HTTPError as err:
			self.msgPack.setResend()
			logging.error(err)

if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
	target = "http://localhost:8080"
	agent = HttpAgent(target=target, interval=2)
	agent.ping()
	data = "Data "
	for x in range(20):
		time.sleep(1)
		data = "Data " + str(x)
		agent.send({'request' : "data {}".format(x)})
		
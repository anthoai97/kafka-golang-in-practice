import datetime
import logging
import time
from typing import TypeVar
import requests

AppType = TypeVar("AppType")

class HttpAgent:
	def __init__(
		self: AppType,
		*,
		agentName: str = "DataSpire Agent",
		target: str = "localhost:8080",
		path: str = "/webhook",
		timeout: int = 300,
		interval: int = 3,
	) -> None:
		self.target = target
		self.path = path
		self.timeout = timeout
		self.interval = interval
		self.datas = []
		self.savedTime = None
		self.agentName = agentName

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
			url = self.target + self.path
			body = {'agent': self.agentName, 'timestamp': time.mktime(datetime.datetime.now().timetuple()) , 'package': str(data)}
			r = requests.post(url, timeout=self.timeout, data=body)
			r.raise_for_status()
			logging.info(str(r.status_code) + ' => ' + str(data))
		except requests.exceptions.HTTPError as err:
			logging.error(err)

	def sendInterval(self, data: any):
		if self.savedTime is None:
			self.savedTime = datetime.datetime.now()
		
		now = datetime.datetime.now()
		x  = now - self.savedTime
		if x.total_seconds() > self.interval:
			self.send(self.datas)
			self.savedTime = datetime.datetime.now()
			self.datas = []
		else:
			self.datas.append(data)
	
if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
	target = "http://localhost:8080"
	agent = HttpAgent(target=target)
	agent.ping()
	data = "Data "
	for x in range(20):
		time.sleep(1)
		data = "Data " + str(x)
		agent.sendInterval({'data' : "data {}".format(x)})
		
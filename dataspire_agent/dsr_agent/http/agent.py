import logging
from typing import TypeVar
import requests

AppType = TypeVar("AppType")

# Target, Method, Timeout


class HttpAgent:
	def __init__(
		self: AppType,
		*,
		target: str = "localhost:8080"
	) -> None:
		self.target = target

	def ping(self):
		try:
			url = self.target + '/ping'
			r = requests.get(url, timeout=300)
			r.raise_for_status()
			logging.info(r.json())
		except requests.exceptions.HTTPError as err:
			raise SystemExit(err)

if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
	target = "http://localhost:8080"
	agent = HttpAgent(target=target)
	agent.ping()
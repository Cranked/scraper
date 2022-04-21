#Imports

from bs4 import BeautifulSoup
import requests , re , random , os ,time,sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from bin.proxies import *

class AZLyrics(Proxy_Checker):
	def __init__(self):
		Proxy_Checker.__init__(self)
		self.base_url = self.check_url
		self.url_max_retrires = 5
		self.max_retries = 5
		self.max_workers = 100
		self.timeout = 10
		self.az_logger()





	def az_logger(self):
		self.az_logger = logging.getLogger(__name__)
		self.az_logger.setLevel(logging.DEBUG)
		self.az_formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
		self.az_file_handler = logging.FileHandler(os.path.abspath('log_data/main.log'))
		self.az_file_handler.setLevel(logging.DEBUG)
		self.az_file_handler.setFormatter(self.az_formatter)
		self.az_logger.addHandler(self.az_file_handler)

	def get_url(self , url):
		flag = self.url_max_retrires
		while(flag):
			header = self.return_header()
			proxy = self.return_proxy()
			try:
				site = requests.get(self.check_url , headers = header , proxies = {'http':"http://"+proxy,'https':"https://"+proxy},timeout = self.timeout)
				if site.status_code == requests.codes.ok:
					html_soup = BeautifulSoup(site.text , 'html.parser')
					if len(html_soup.find_all('div',class_ = 'alert alert-info')) == 0:
						# self.az_logger.info('SuccessFul Get Request -> {} using Proxy -> {} on try-> {}'.format(url,proxy,flag))
						flag=0
						return html_soup
					else:
						self.az_logger.debug('Recapta Detected -> {} using Proxy -> {} on try-> {}'.format(url , proxy , flag))
						flag -= 1
						if flag == 0:
							return '0'
				else:
					self.az_logger.debug('Proxy Status Mismatch -> {} using Proxy -> {} on Try -> {}'.format(site.status_code , proxy , flag))
					flag -= 1
					if flag ==0:
						return '0'
			except Exception as E:
				self.az_logger.debug('Something Went Wrong -> {} using  Proxy -> {} Error -> {} on try-> {}'.format(url,proxy,E,flag))
				flag -= 1
				if flag == 0:
					return '0'
		return '0'
	def start_scrapping(self):
		try:
			self.loop = asyncio.get_event_loop()
			self.loop.set_debug(1)
			future = asyncio.ensure_future(self.async_get_proxies())
			self.loop.run_until_complete(future)
		except Exception as E:
			self.az_logger.warning('Warning Log -> {} Lineno -> {}'.format(E, sys.exc_info()[-1].tb_lineno))
		finally:
			self.loop.close()
if __name__ == "__main__":
	pass


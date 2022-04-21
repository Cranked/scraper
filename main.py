import json
from bin.azlyrics import *
from bin.proxies import *

url = "https://www.motogp.com/en/statistics/constructors-wc/All-seasons/All-classes/?page=1"

proxyChecker = Proxy_Checker()
proxyChecker.set_url(url)
proxyChecker.get_proxies()
proxyChecker.async_get_proxies()
proxyChecker.save_data()
hebele = AZLyrics()
hebele.set_url(url)
soup = hebele.get_url(url)

result=soup
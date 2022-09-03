import logging
import os
import re
import requests
from bs4 import BeautifulSoup


# setup
URL = "https://codecool.com/hu/kepzesek/karrier-felkeszito-kepzes/"
log_path = "scraping.log"
FORMAT = '%(asctime)s [%(levelname)s]:  %(message)s'
logging.basicConfig(format=FORMAT, filename=log_path, encoding="utf8")
log = logging.getLogger("scraping")
log.setLevel(10)

# get content
raw_page = requests.get(URL, timeout=5)
page = BeautifulSoup(raw_page.content, "html.parser")

# parse
results = [match.start() for match in re.finditer("A jelentkezés határideje:|Jelentkezési határidő:", str(raw_page.content, "utf8"))]
print(str(raw_page.content, "utf8"))
print(results)

# log
log.info("---------- Today's results: ----------")
for result in results:
    result_end_1 = str(raw_page.content, "utf8").find(" />", result)
    result_end_2 = str(raw_page.content, "utf8").find("</p>", result)
    result_end = result_end_1 if result_end_1 < result_end_2 else result_end_2
    log.info("from "+str(result)+": "+str(raw_page.content, "utf8")[result:result_end])
log.info("logfile size: "+ str(os.path.getsize(log_path)))
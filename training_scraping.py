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
mail_content = "Hi\n\nToday's results:\n\n"
mail_subject = "Codecool results!"

# get content
raw_page = requests.get(URL, timeout=5)
page = BeautifulSoup(raw_page.content, "html.parser")

# parse
results = [match.start() for match in re.finditer("A jelentkezés határideje:|Jelentkezési határidő:", str(raw_page.content, "utf8"))]

# log
log.info("---------- Today's results: ----------")
for result in results:
    result_end_1 = str(raw_page.content, "utf8").find(" />", result)
    result_end_2 = str(raw_page.content, "utf8").find("</p>", result)
    result_end = result_end_1 if result_end_1 < result_end_2 else result_end_2
    for_log = "from "+str(result)+": "+str(raw_page.content, "utf8")[result:result_end]
    log.info(for_log)
    mail_content += for_log+"\n"
log.info("logfile size: "+ str(os.path.getsize(log_path)))

# check update
matches = re.findall("november|október|december", str(raw_page.content, "utf8").lower())
if matches != []:
    for match in matches:
        mail_subject = "!!!! CODECOOL UPDATED to "+str(match)+" !!!!"

    # mail
    from mailjet_rest import Client
    api_key = ''
    api_secret = ''
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "",
            "Name": ""
        },
        "To": [
            {
            "Email": "",
            "Name": ""
            }
        ],
        "Subject": mail_subject,
        "TextPart": mail_content,
        "HTMLPart": mail_content.replace("\n","<br>")+"<br>More info at <a href='"+URL+"'>CodeCool</a>!",
        "CustomID": ""
        }
    ]
    }
    result = mailjet.send.create(data=data)


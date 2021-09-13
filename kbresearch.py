from bs4 import BeautifulSoup
import requests
import base64
import json

"""
Kb 증권 리서치 추출
"""

kbUrl = "https://www.kbsec.com/go.able?linkcd=s040203010001"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
response = requests.get(kbUrl, headers=headers)
html = response.text
soup = BeautifulSoup(html, "lxml")
pText = soup.select_one("p").text
jsonList = json.loads(pText)["list"]
companyGenerator = (item for item in jsonList if item["reportTag"] == "[KB: 기업]")
companyList = list(companyGenerator)
for i in range(len(companyList)):
    day = companyList[i]["publicDate"]
    code = companyList[i]["stkCd"]
    title = companyList[i]["docTitleSub"]
    writer = companyList[i]["analystNm"]
    documentid = companyList[i]["documentid"]
    urlLink = companyList[i]["urlLink"]

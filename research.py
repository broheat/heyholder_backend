import requests
from bs4 import BeautifulSoup
import re

"""
미래에셋증권 리서치 추출
"""

mrUrl = r"https://securities.miraeasset.com/bbs/board/message/list.do?categoryId=1545"

response = requests.get(mrUrl)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    dic = []
    for i in range(10):
        link = soup.select_one("#bbsTitle{0}".format(i))
        href = link.get("href")[16:-1].replace("'", "")
        arr = list(map(int, href.split(",")))
        if i == 0:  # 업로드 날짜.
            day = soup.select_one(
                "#contents > table > tbody > tr.first > td:nth-child(1)"
            ).text.rsplit()[0]
        else:
            day = day = soup.select_one(
                "#contents > table > tbody > tr:nth-child({0}) > td:nth-child(1)".format(
                    i + 1
                )
            ).text.rsplit()[0]

        linkPage = r"https://securities.miraeasset.com/bbs/board/message/view.do?messageId={0}&messageNumber={1}&messageCategoryId=0&startId=zzzzz~&startPage=1&curPage=2&searchType=2&searchText=&searchStartYear=2020&searchStartMonth=09&searchStartDay=10&searchEndYear=2021&searchEndMonth=09&searchEndDay=10&lastPageFlag=&vf_headerTitle=&categoryId=1545".format(
            arr[0], arr[1]
        )  # 리서치 링크
        code = re.search(r"\(([0-9]+).*?\)", link.text).group(1)  # 종목 코드
        title = link.text.split(")", 1)[1]  # 리서치 제목
        writer = soup.select_one(
            "#contents > table > tbody > tr:nth-child({0}) > td:nth-child(4)".format(
                i + 1
            )
        ).text.rsplit()[
            0
        ]  # 작성자
        result = dict(code=code, title=title, writer=writer, link=linkPage, day=day)
        dic.append(result)
        print(len(linkPage))


else:
    print(response.status_code)

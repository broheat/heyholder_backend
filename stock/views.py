from bs4 import BeautifulSoup
from .models import Research
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import re


def getStockNamu(company_id, company_secret):
    url = "https://www.mynamuh.com/login/loginAction.action"
    data = {
        "isCertLogin": "N",
        "userid": company_id,
        "ca_gb": "N",
        "passwd": company_secret,
    }
    balance_data = {"wm_menu_code": "1246,1247,1250,2974"}
    dic = {}
    i = 0

    with requests.Session() as s:
        log_req = s.post(url, data=data)

        balance_url = "https://www.mynamuh.com/tx/banking/inquiry/balance01.action"
        balance_req = s.post(balance_url, data=balance_data)

        soup = BeautifulSoup(balance_req.text, "lxml")
        type = soup.select_one("#totalListRow > tr:nth-child(1)>th")

        while type is not None and type.text == "주식":
            i = i + 1
            type = soup.select_one("#totalListRow > tr:nth-child({0})>th".format(i + 1))
            name = soup.select_one(
                "#totalListRow > tr:nth-child({0})>td.alignL".format(i)
            ).text.strip()
            code = soup.select_one(
                "#totalListRow>tr:nth-child({0})>td:nth-child(3)".format(i)
            ).text

            if len(code) > 6:
                return dic
                break
            else:
                pass

            count_text = soup.select_one(
                "#totalListRow>tr:nth-child({0})>td:nth-child(4)".format(i)
            ).text
            amount = int(count_text.replace(",", ""))

            dic[code] = [name, amount]
        return dic


def getResearch():
    url = r"https://securities.miraeasset.com/bbs/board/message/list.do?categoryId=1545"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        dic = []
        company = "미래에셋대우"
        lastResearch = Research.objects.filter(company=company).last()

        if lastResearch is None:
            for i in range(10):
                link = soup.select_one("#bbsTitle{0}".format(i))
                href = link.get("href")[16:-1].replace("'", "")
                arr = list(map(int, href.split(",")))
                code = re.search(r"\(([0-9]+).*?\)", link.text).group(1)  # 종목 코드
                writer = soup.select_one(
                    "#contents > table > tbody > tr:nth-child({0}) > td:nth-child(4)".format(
                        i + 1
                    )
                ).text.rsplit()[
                    0
                ]  # 작성자

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
                title = link.text.split(")", 1)[1]  # 리서치 제목

                linkPage = r"https://securities.miraeasset.com/bbs/board/message/view.do?messageId={0}&messageNumber={1}&messageCategoryId=0&startId=zzzzz~&startPage=1&curPage=2&searchType=2&searchText=&searchStartYear=2020&searchStartMonth=09&searchStartDay=10&searchEndYear=2021&searchEndMonth=09&searchEndDay=10&lastPageFlag=&vf_headerTitle=&categoryId=1545".format(
                    arr[0], arr[1]
                )  # 리서치 링크

                result = dict(
                    code=code,
                    title=title,
                    writer=writer,
                    link=linkPage,
                    day=day,
                    company=company,
                )
                dic.append(result)

            for i in reversed(range(len(dic))):
                r = Research.objects.create(**dic[i])
                r.save()
        else:
            for i in range(10):
                link = soup.select_one("#bbsTitle{0}".format(i))
                href = link.get("href")[16:-1].replace("'", "")
                arr = list(map(int, href.split(",")))
                code = re.search(r"\(([0-9]+).*?\)", link.text).group(1)  # 종목 코드
                writer = soup.select_one(
                    "#contents > table > tbody > tr:nth-child({0}) > td:nth-child(4)".format(
                        i + 1
                    )
                ).text.rsplit()[
                    0
                ]  # 작성자
                if lastResearch.code == code and lastResearch.writer == writer:
                    for i in reversed(range(len(dic))):
                        r = Research.objects.create(**dic[i])
                        r.save()
                    break

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
                title = link.text.split(")", 1)[1]  # 리서치 제목

                linkPage = r"https://securities.miraeasset.com/bbs/board/message/view.do?messageId={0}&messageNumber={1}&messageCategoryId=0&startId=zzzzz~&startPage=1&curPage=2&searchType=2&searchText=&searchStartYear=2020&searchStartMonth=09&searchStartDay=10&searchEndYear=2021&searchEndMonth=09&searchEndDay=10&lastPageFlag=&vf_headerTitle=&categoryId=1545".format(
                    arr[0], arr[1]
                )  # 리서치 링크

                result = dict(
                    code=code,
                    title=title,
                    writer=writer,
                    link=linkPage,
                    day=day,
                    company=company,
                )
                dic.append(result)

            for i in reversed(range(len(dic))):
                r = Research.objects.create(**dic[i])
                r.save()

    else:
        print("error")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getResearch, "interval", minutes=1)
    scheduler.start()

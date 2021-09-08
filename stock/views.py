import requests
from bs4 import BeautifulSoup


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

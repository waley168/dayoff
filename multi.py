from bs4 import BeautifulSoup
import requests

def multi(userName, userID, userPW):
    with requests.Session() as s:
        page = s.get('http://10.158.7.80/wGovFlow_SPC6/Default.aspx')
        soup = BeautifulSoup(page.content, 'lxml')

        payload_loginPage = {'txtUserName': userID, 'txtPassword': userPW, 'cmdOK.x': '60', 'cmdOK.y': '13'}

        payload_loginPage["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        payload_loginPage["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        payload_loginPage["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        s.post('http://10.158.7.80/wGovFlow_SPC6/Default.aspx', data=payload_loginPage)

        page = s.get('http://10.158.7.80/wGovFlow_SPC6/Offtra_Search1.aspx')
        soup = BeautifulSoup(page.content, 'lxml')


        page = s.post('http://10.158.7.80/wGovFlow_SPC6/Show1.aspx')

        soup = BeautifulSoup(page.content, 'lxml')
        table = soup.find('table', {'class': 'Grid3'})
        if table:
            trs = table.find_all('tr')[1:]
            if trs:
                rows = list()
                for tr in trs:
                    rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])
                for row in rows:
                    row[10] = userName
                print(rows)
                return rows
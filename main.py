from bs4 import BeautifulSoup
import requests
import pandas as pd
import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
import calendar
from multi import multi
import csv

def searchAll (fromTime, endTime):
    with requests.Session() as s:
        page = s.get('http://10.158.7.80/wGovFlow_SPC6/Default.aspx')
        soup = BeautifulSoup(page.content, 'lxml')

        payload_loginPage = {'txtUserName': 'E124498801', 'txtPassword': '19930622', 'cmdOK.x': '60', 'cmdOK.y': '13'}

        payload_loginPage["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        payload_loginPage["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        payload_loginPage["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        s.post('http://10.158.7.80/wGovFlow_SPC6/Default.aspx', data=payload_loginPage)

        page = s.get('http://10.158.7.80/wGovFlow_SPC6/Offtra_Search1.aspx')
        soup = BeautifulSoup(page.content, 'lxml')

        payload_loginPage = {''
                             'ctl00$ContentPlaceHolder1$txtDepno': '3000,3001,3002,3003,3004,3005,3006,3007,3008,3009,3010,3011,3012,3013,3014,3015,3016,3017',
                             'ctl00$ContentPlaceHolder1$txtComno': '001,001,001,001,001,001,001,001,001,001,001,001,001,001,001,001,001,001',
                             'ctl00$ContentPlaceHolder1$txtSdate': fromTime,
                             'ctl00$ContentPlaceHolder1$txtEdate': endTime,
                             'ctl00$ContentPlaceHolder1$cmdQuery': '查詢'
                             }
        payload_loginPage["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        payload_loginPage["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        payload_loginPage["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

        page = s.post('http://10.158.7.80/wGovFlow_SPC6/Offtra_Search1.aspx', data=payload_loginPage)

        soup = BeautifulSoup(page.content, 'lxml')
        table = soup.find('table', {'class': 'Grid'})
        columns = [th.text.replace('\n', '') for th in table.find('tr').find_all('th')]

        trs = table.find_all('tr')[1:]
        rows = list()
        for tr in trs:
            rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])
        df = pd.DataFrame(data=rows, columns=columns)
        df.to_csv('dayoff_all.csv', encoding='utf_8_sig')
        return df

class MyDateEntry(DateEntry):
    def __init__(self, master=None, **kw):
        DateEntry.__init__(self, master=None, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg='black', bd=1)
        # add label displaying today's date below
        tk.Label(self._top_cal, bg='gray90', anchor='w',
                 text='今日: %s' % date.today().strftime('%Y/%m/%d')).pack(fill='x')

def chmessage():
    datetimeobjectfrom = date.strftime(lbl_title2.get_date(),'%Y/%m/%d')
    datetimeobjectend = date.strftime(lbl_title4.get_date(), '%Y/%m/%d')
    searchdata = searchAll(datetimeobjectfrom, datetimeobjectend)
    message.config(text=searchdata)

def searchIng():
    with open('idandbirth.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        searchIngdata = list()
        for row in rows:
            message.config(text=row['dayoff_no'])
            searchresult = multi(row['dayoff_name'], row['dayoff_id'], row['dayoff_birth'])
            if searchresult:
                searchIngdata.extend(searchresult)
        if all(x is None for x in searchIngdata):
            message.config(text='沒有資料')
        else:
            searchcolumns = ['申請日期', '假別', '開始結束日期', '開始結束時間', '時數', '抵加班', '狀態', '駁回原因', '事由', '附件', '姓名']
            dfsearch = pd.DataFrame(data=searchIngdata, columns=searchcolumns)
            print(searchIngdata)
            dfsearch.to_csv('dayoff_ing.csv', encoding='utf_8_sig')
def define_layout(obj, cols=1, rows=1):
    def method(trg, col, row):

        for c in range(cols):
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj) == list:
        [method(trg, cols, rows) for trg in obj]
    else:
        trg = obj
        method(trg, cols, rows)

window = tk.Tk()
window.title('官二大請假系統')
align_mode = 'nswe'
pad = 5

div_h = 300
div_w = 400
div1 = tk.Frame(window,  width=div_w/2 , height=20)
div2 = tk.Frame(window,  width=div_w/2 , height=20)
div3 = tk.Frame(window,  width=div_w/2 , height=div_h)
div4 = tk.Frame(window,  width=div_w , height=div_h , bg='orange')
window.update()
win_size = min( window.winfo_width(), window.winfo_height())

div1.grid(column=0, row=0, padx=pad, pady=pad, sticky=align_mode)
div2.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=0, row=2, padx=pad, pady=pad, sticky=align_mode)
div4.grid(column=1, row=0, padx=pad, pady=pad, rowspan=3, sticky=align_mode)

define_layout(window, cols=2, rows=3)
define_layout([div1, div2, div3, div4])

last_day_of_month = calendar.monthrange(date.today().year,date.today().month)[1]
lbl_title2 = MyDateEntry(div1, year=date.today().year, month=date.today().month, day=1)
lbl_title4 = MyDateEntry(div2, year=date.today().year, month=date.today().month, day=last_day_of_month)

lbl_title2.grid(column=0, row=0, sticky=align_mode)
lbl_title4.grid(column=0, row=1, sticky=align_mode)

bt1 = tk.Button(div3, text='區間請假列表', bg='grey', fg='black', command=chmessage)
bt2 = tk.Label(div3, text='--------', fg='grey')
bt3 = tk.Button(div3, text='正在請假流程', bg='grey', fg='black', command=searchIng)

bt1.grid(column=0, row=0, sticky=align_mode)
bt2.grid(column=0, row=1, sticky=align_mode)
bt3.grid(column=0, row=2, sticky=align_mode)

message = tk.Label(div4, text='')
message.grid(column=0, row=0, sticky=align_mode)

define_layout(window, cols=2, rows=3)
define_layout(div4)
define_layout(div1)
define_layout(div2)
define_layout(div3, rows = 3)

window.mainloop()
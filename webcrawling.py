import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import seaborn as sns
import matplotlib.pyplot as plt
import datetime


def dataframeFromHTML(item_data):
    result_month = []
    result_price = []
    for i in item_data:
        temp = []

        month_ = i.find_all("td", {"class": "month"})
        price_ = i.find_all("td", {"class": ["price", "no_data", "no_data_last"]})
        floor_ = i.find_all("td", {"class": "floor"})

        if not month_:
            result_month.append(result_month[-1])
        for j in month_:
            result_month.append(datetime.datetime.strptime(j.text, '%Y.%m'))
        # 1) null, 2) 35,000 3) 35000/20
        for j in price_:
            tmp = j.text.replace(",", "")
            tmp = tmp.replace("-", "0")
            if tmp.find('/') != -1:
                temp.append(0)
            else:
                temp.append(int(tmp))

        result_price.append(temp)

    index = 0
    result_price0 = []
    result_price1 = []
    result_price2 = []
    for i in result_price:
        result_price0.append(result_price[index][0])
        result_price1.append(result_price[index][1])
        result_price2.append(result_price[index][2])
        index = index + 1

    total = {"date": result_month, "매매": result_price0, "전세": result_price1, "월세": result_price2}
    #print(total)
    df = pd.DataFrame(total, columns=['date', '매매', '전세', '월세'])
    #print(df)
    return df


def writeToExcel(df, path, _sheet_name):
    # add new sheet to the excel file
    # path = 'd:/result.xlsx'
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, sheet_name=_sheet_name)
    writer.save()


years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

dfs = []
for i in years:
    response = requests.get(
        'http://land.naver.com/article/molitPriceInfo.nhn?rletTypeCd=A01&tradeTypeCd=A1&rletNo=3211&cortarNo=1153010100&hscpTypeCd=A01%3AA03%3AA04&mapX=126.8843577&mapY=37.5123143&mapLevel=13&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=300&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=' +
        i + '&exclsSpc=&splySpcR=&cmplYn=')
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all("div", {"class": "chart_table_area"})
    item_data = item[0].find("tbody").find_all("tr")

    dfs.append(dataframeFromHTML(item_data))

total = {"date": [], "매매": [], "전세": [], "월세": []}
df_total = pd.DataFrame(total, columns=['date', '매매', '전세', '월세'])
for i in dfs:
    #print(i)
    df_total = df_total.append(i)

print(df_total)

writeToExcel(df_total, 'd:/result.xlsx', '1')

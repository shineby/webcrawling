import requests
import pandas as pd
from bs4 import BeautifulSoup

# http://land.naver.com/article/molitPriceInfo.nhn?rletTypeCd=A01&tradeTypeCd=A1&rletNo=3211&cortarNo=1153010100&hscpTypeCd=A01%3AA03%3AA04&mapX=126.8843578&mapY=37.5123053&mapLevel=13&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=700&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=2017&exclsSpc=&splySpcR=&cmplYn=
year = '2017'
response = requests.get(
    'http://land.naver.com/article/molitPriceInfo.nhn?rletTypeCd=A01&tradeTypeCd=A1&rletNo=3211&cortarNo=1153010100&hscpTypeCd=A01%3AA03%3AA04&mapX=126.8843577&mapY=37.5123143&mapLevel=13&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=300&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=' + year + '&exclsSpc=&splySpcR=&cmplYn=')
html = response.text

soup = BeautifulSoup(html, 'html.parser')
item = soup.find_all("div", {"class": "chart_table_area"})
item_data = item[0].find("tbody").find_all("tr")

month_ = item_data
price_ = item_data
floor_ = item_data
result_month = []
temp = []
result_price = []

for i in item_data:
    # print(i)
    temp = []

    month_ = i.find_all("td", {"class": "month"})
    price_ = i.find_all("td", {"class": "price"})
    floor_ = i.find_all("td", {"class": "floor"})
    # result.append(month_, price_,floor_)

    if not month_:
        result_month.append(result_month[-1])
    for j in month_:
        result_month.append(j.text)
    for j in price_:
        if j.text == '':
            print("-")
        else:
            temp.append(j.text)

    result_price.append(temp)

index = 0
for i in result_month:
    print(result_month[index], result_price[index])
    index = index + 1

tmp = pd.DataFrame(result_price, index=result_month)
print(tmp)
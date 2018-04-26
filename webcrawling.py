import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import seaborn as sns
import matplotlib.pyplot as plt

# http://land.naver.com/article/molitPriceInfo.nhn?rletTypeCd=A01&tradeTypeCd=A1&rletNo=3211&cortarNo=1153010100&hscpTypeCd=A01%3AA03%3AA04&mapX=126.8843578&mapY=37.5123053&mapLevel=13&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=700&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=2017&exclsSpc=&splySpcR=&cmplYn=
year = '2010'
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
    price_ = i.find_all("td", {"class": ["price","no_data","no_data_last"]})
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
            tmp = j.text.replace(",", "")
            tmp = tmp.replace("-", "0")
            if tmp.find('/') != -1:
                temp.append(0)
            else:
                temp.append(int(tmp))
            #if tmp.find('-') != -1:
    result_price.append(temp)

index = 0
for i in result_month:
    #print(result_month[index], result_price[index])
    index = index + 1

index = 0
result_price0 = []
result_price1 = []
result_price2 = []
for i in result_price:
    result_price0.append(result_price[index][0])
    result_price1.append(result_price[index][1])
    result_price2.append(result_price[index][2])
    index = index + 1


total = {"date": result_month, "매매": result_price0, "전세":result_price1, "월세":result_price2}
print(total)
df = pd.DataFrame(total, columns=['date', '매매', '전세', '월세'])
print(df)

# total = {"date": result_month, "price": result_price}
# tmp = pd.DataFrame(total)
# print(tmp)
# plt.figure(figsize=(8, 6))
# plt.plot(df,'g^')
# plt.show()

# df.to_excel('d:/test.xlsx')
book = load_workbook('d:/test.xlsx')
writer = pd.ExcelWriter('d:/test.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#
# ## Your dataframe to append.
df.to_excel(writer, sheet_name=year)
writer.save()
#writer.close()
# #tmp.to_excel('abc.xlsx', sheet_name=year)
# # print(tmp)
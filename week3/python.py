# 要求一：Python 取得網路上的資料並儲存到檔案中
# 台北市政府提供景點公開資料連線網址如下：
# https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json
# 請撰寫一隻 Python 程式，能從以上網址取得資料，並且將景點資料用一行一筆資料，每個欄
# 位用逗號隔開的格式，輸出到 data.csv 的檔案中，請將生成的 data.csv 檔案包含在你的作業
# 資料夾中。
# 請根據 xpostDate 欄位，僅輸出 2015 年以後 ( 包含 2015 年 ) 的資料。
# 提醒：區域資料請參考原始資料的地址欄位，必須是三個字，並且為以下區域的其中一個：中
# 正區、萬華區、中山區、大同區、大安區、松山區、信義區、士林區、文山區、北投區、內湖區、南港區。
# https://medium.com/seaniap/python-%E5%A6%82%E4%BD%95%E8%AE%80%E5%AF%ABcsv-%E8%88%87%E5%90%88%E4%BD%B5csv%E6%AA%94%E6%A1%88-5e9d5a4e577e

import urllib.request as request
import json
import csv

url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json'

with request.urlopen(url) as response:
    attractions = json.loads(response.read())["result"]["results"]
    
with open('data.csv', 'w+', newline='') as file:
    for attraction in attractions:
        if int(attraction['xpostDate'][:4]) >= 2015:
            stitle = (attraction['stitle'])
            address = (attraction['address'][5:8])
            longitude = (attraction['longitude'])
            latitude = (attraction['latitude'])
            # attraction["file"].lower().find("jpg") -> 找出 jpg 的index
            photo = (attraction["file"][:attraction["file"].lower().find("jpg")+3])
            writer = csv.writer(file)
            writer.writerow([stitle, address, longitude, latitude, photo])
        else:
            continue
        

# 要求二：Python 網頁爬取資料並儲存到檔案中 (Optional)
# PTT 電影版的網址如下：
# https://www.ptt.cc/bbs/movie/index.html
# 請撰寫一隻 Python 程式，從以上網頁爬取每一篇文章的標題，並且能持續往上一頁爬取，總
# 共爬取十頁。本題開放使用 BeautifulSoup 這個第三方套件。
# 程式在取得標題後，以一行一標題的格式，輸出到 movie.txt 中，將生成的 movie.txt 檔案包含
# 在你的作業資料夾中，並符合以下規範：
# 1. 僅輸出開頭為 [好雷]、[普雷]、[負雷] 的文章標題。
# 2. 輸出時，先輸出 [好雷] 開頭的所有標題，然後依序輸出 [普雷] 和 [負雷] 開頭的所有標題。

from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/movie/index.html"

positve = []
normal = []
negative = []

def crawler_Ptt(url):
    result = request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
})
    with request.urlopen(result) as response:
        data = response.read()
    root = BeautifulSoup(data, 'html.parser')
    titles = root.find_all('div', class_='title')

    for title in titles:
        if '好雷' in title.a.text[1:3]:
            positve.append(title.a.text)
        elif '普雷' in title.a.text[1:3]:
            normal.append(title.a.text)
        elif '負雷' in title.a.text[1:3]:
            negative.append(title.a.text)
        else:
            continue
    new_url = 'https://www.ptt.cc'+root.find('a', string='‹ 上頁')['href']
    return new_url

for _ in range(10):
    url = crawler_Ptt(url)
    
with open('movie.txt', 'w+') as file:
    for movie in positve + normal + negative:
        file.write(movie + '\n')
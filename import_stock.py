
# Scraping Stock Prices

import urllib
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import csv
import datetime
import getpass

# From Naver Finance
def stock_naver(curs, num_page, exchange):

    if exchange == 'KS':
        stock_code = open('kospi.csv', 'r')
    elif exchange == 'KQ':
        stock_code = open('kosdaq.csv', 'r')
    else:
        return

    csvReader = csv.reader(stock_code)

    next(csvReader) 
    for st in csvReader:
        code = st[0] + '.' + exchange
        print(code,st[1]) # Stock Codes
        records = []

        try:

            for page in range(1, num_page+1):
                url = 'http://finance.naver.com/item/sise_day.nhn?code=' + st[0] +'&page='+ str(page)
                html = urlopen(url)
                source = BeautifulSoup(html.read(), "html.parser")
                srlists=source.find_all("tr") 
                isCheckNone = None

                time.sleep(1)

                for i in range(1,len(srlists)-1): 
                    if(srlists[i].span != isCheckNone):
                        records.append(dict(date=srlists[i].find_all("td",align="center")[0].text.replace('.','-'), 
                                            Close=int(srlists[i].find_all("td",class_="num")[0].text.replace(',', '')), 
                                            High=int(srlists[i].find_all("td",class_="num")[3].text.replace(',', '')), 
                                            Low=int(srlists[i].find_all("td",class_="num")[4].text.replace(',', '')), 
                                            Volume=int(srlists[i].find_all("td",class_="num")[5].text.replace(',', ''))))

            # INSERT
            for record in records:
                sql = "INSERT INTO stock_daily (dt, StockCode, High, Low, Close, Volume) VALUES ('%s', '%s', %s, %s, %s, %s) \
                       ON DUPLICATE KEY UPDATE High=%s, Low=%s, Close=%s, Volume=%s" \
                      %  (record['date'], code, record['High'], record['Low'], record['Close'], record['Volume'], \
                          record['High'], record['Low'], record['Close'], record['Volume'])
                curs.execute(sql)

        except:
            pass


def main():

    # Number of Pages For Naver Finance Historical Data
    num_page = 1
    num_page = int(input("# of Pages (Enter for " + str(num_page) + "): ") or num_page)

    # MySQL Connection 
    user_mysql = input("MySQL user: ") 
    password_mysql = getpass.getpass("MySQL password: ")
    conn = pymysql.connect(host='localhost', user=user_mysql, password=password_mysql,
                           db='market_data', charset='utf8')

    # CREATE TABLE stock_daily (
    #   dt DATE,
    #   StockCode VARCHAR(100),
    #   High INT UNSIGNED,
    #   Low INT UNSIGNED,
    #   Close INT UNSIGNED,
    #   AdjClose INT UNSIGNED,
    #   Volume INT UNSIGNED,
    #   PRIMARY KEY (dt, StockCode)
    #   );

    # Cursor 
    curs = conn.cursor()

    # import KOSPI
    stock_naver(curs, num_page, 'KS')

    # import KOSDAQ
    stock_naver(curs, num_page, 'KQ')

    # Commit
    conn.commit()

    # Close
    conn.close()

if __name__ == '__main__':
    main()


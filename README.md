# Market

## 개요

- KOSPI와 KOSDAQ 종목 주가를 MySQL 테이블에 저장
- 네이버에서 주가를 가져오는 방식은 http://estenpark.tistory.com/353 을 참고하였음

## 구성파일

- import_stock.py: 파이썬 스크립트
- kospi.csv: 한국거래소의 KOSPI 종목 정보
- kosdaq.csv: 한국거래소의 KOSDAQ 종목 정보

## 요구사항

### Python 3

### 패키지 설치
1. [PyMySQL](https://github.com/PyMySQL/PyMySQL)
2. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## 사용법

### 파이썬 스크립트 수정
- DB 기본설정은 host: localhost, DB: market_data, table: stock_daily 
- 필요 시 스크립트에서 수정

### DB 테이블 생성

다음과 같이 테이블 생성하되 테이블 이름은 앞서 정한 이름과 일치시킴

```
CREATE TABLE stock_daily (
    dt DATE,
    StockCode VARCHAR(100),
    High INT UNSIGNED,
    Low INT UNSIGNED,
    Close INT UNSIGNED,
    AdjClose INT UNSIGNED,
    Volume INT UNSIGNED,
    PRIMARY KEY (dt, StockCode)
    );
```
여기서 
- StockCode: 종목코드
- High: 고가
- Low: 저가
- Close: 종가
- AdjClose: 수정종가 (현재 무시됨)
- Volume: 거래량

### 파이썬 스크립트 실행

- python 3으로 import_stock.py 실행한 후 페이지수, MySQL 사용자 ID와 암호 입력
- 페이지수는 네이버 금융의 일별시세 중 최대 몇 페이지의 데이터를 가져올지를 결정함

### 기타

- KOSPI 종목은 종목코드.KS, KOSDAQ 종목은 종목코드.KQ의 형식으로 저장됨
- 동일한 날짜와 종목으로 저장하려고 하면 덮어쓰임

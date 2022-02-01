import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

#sms api adatok
phone_number = "+12345678912"
account_sid = "ACCOUN SID HERE"
auth_token = "AUTH TOKEN HERE"
client = Client(account_sid, auth_token)

#tegnap és tegnapelőtti dátumok formázása
y_day = datetime.now() - timedelta(days=1)
yesterday = y_day.strftime('%Y-%m-%d')
y2_day = datetime.now() - timedelta(days=2)
before_yesterday = y2_day.strftime('%Y-%m-%d')

# tesla reszveny API adatok
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": "YOUR API HERE",
}

# api URL lekerdezés a parametérek alapján, tegnapi es tegnapelőtti adatok valtozókkal való behelyettesítése
response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()
yesterday_data = data['Time Series (Daily)'][yesterday]
before_yesterday_data = data['Time Series (Daily)'][before_yesterday]

# a végső adat kinyerése
stock_yesyerday = yesterday_data['4. close']
stock_before_yesyerday = before_yesterday_data['4. close']

# százalék számítás
price_inc_or_dec = float(stock_before_yesyerday) * 100 / float(stock_yesyerday) - 100
percentage = (round(price_inc_or_dec))

# newsapi paraméterek
parameters_tesla = {
    "q": "tesla",
    "from": yesterday,
    "sortBy": "relevancy",
    "apiKey": "b99e4d4243a842b989ae60deee4d579b",
}

# tesla hírek lekérdezése a newsapiról
response2 = requests.get("https://newsapi.org/v2/everything", params=parameters_tesla)
response2.raise_for_status()
tesla_news = response2.json()
title_list = []
description_list = []
#  első 3 legrelevánsabb hír
for i in range(3):
    articles = tesla_news["articles"][i]["title"]
    title_list.append(articles)
    description = tesla_news["articles"][i]["description"]
    description_list.append(description)

# formázás
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

# vizsgálat, hogy növekedett vagy csökkent
# utána sms küldés a változásról és a legfontosabb 3 hírről
if stock_yesyerday < stock_before_yesyerday:
    for i in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{percentage} %\nHeadline: {remove_tags(title_list[i])}\nBrief: {remove_tags(description_list[i])}",
            from_='+12393476430',
            to='+36307099284'
        )
        print(message.status)
else:
    for i in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{percentage} %\nHeadline: {remove_tags(title_list[i])}\nBrief: {remove_tags(description_list[i])}",
            from_='+12393476430',
            to='+36307099284'
        )
        print(message.status)

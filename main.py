import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# set twilio application (you must have to register first and use your individual identification)
phone_number = "TWILIO PHONE NUMBER"
account_sid = "YOUR ACCOUNT SID"
auth_token = "YOUR AUTH TOKEN"
client = Client(account_sid, auth_token)

# formatting the date
y_day = datetime.now() - timedelta(days=1)
yesterday = y_day.strftime('%Y-%m-%d')
y2_day = datetime.now() - timedelta(days=2)
before_yesterday = y2_day.strftime('%Y-%m-%d')

# tesla parameters
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": "YOUR API HERE",
}

# query the data from yesterday and before yesterday
response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()
yesterday_data = data['Time Series (Daily)'][yesterday]
before_yesterday_data = data['Time Series (Daily)'][before_yesterday]

# query the final data
stock_yesyerday = yesterday_data['4. close']
stock_before_yesyerday = before_yesterday_data['4. close']

# count the percentage
price_inc_or_dec = float(stock_before_yesyerday) * 100 / float(stock_yesyerday) - 100
percentage = (round(price_inc_or_dec))

# newsapi parameters
parameters_tesla = {
    "q": "tesla",
    "from": yesterday,
    "sortBy": "relevancy",
    "apiKey": "YOUR API KEY",
}

# query the information from newsapi website
response2 = requests.get("https://newsapi.org/v2/everything", params=parameters_tesla)
response2.raise_for_status()
tesla_news = response2.json()
title_list = []
description_list = []
#  the 3 most relecant news
for i in range(3):
    articles = tesla_news["articles"][i]["title"]
    title_list.append(articles)
    description = tesla_news["articles"][i]["description"]
    description_list.append(description)


# formatting
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


# examining the growth or fall
# sending sms about changes
if stock_yesyerday < stock_before_yesyerday:
    for i in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{percentage} %\nHeadline: {remove_tags(title_list[i])}\nBrief: {remove_tags(description_list[i])}",
            from_='TWILIO PHONE NUMBER',
            to='YOUR PHONE NUMBER'
        )
        print(message.status)
else:
    for i in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{percentage} %\nHeadline: {remove_tags(title_list[i])}\nBrief: {remove_tags(description_list[i])}",
            from_='TWILIO PHONE NUMBER',
            to='YOUR PHONE NUMBER'
        )
        print(message.status)

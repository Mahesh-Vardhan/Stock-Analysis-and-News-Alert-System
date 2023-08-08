import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"#The Company Four letter Code that you need alerts
COMPANY_NAME = "X Corp"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "VDL24M0ODB9TNF99"#Open Your own key on alphavantage for free
NEWS_API_KEY = "71dd4f58ddf14e97865156e1459306e0"
TWILIO_SID = "AC8d448bcfbf9d502bcfe8b2c42cb84404"
TWILIO_AUTH_TOKEN = "292961033539b7d6400b50aa9052cd35"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
print(round(difference, 4))
difference_percentage = (difference/float(yesterday_closing_price)) * 100
print(round(difference_percentage, 2))
up_down = None
if difference_percentage > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
if difference_percentage > -6:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)
    formatted_articles = [f"{STOCK_NAME}:{up_down}{difference_percentage}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+14782497219",#Senders Number that generated By Twilio API website
            to="+91!@#$%^&*()_"#Reciever's Number With Your country code
            )

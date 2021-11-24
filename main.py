import requests
import datetime

today = datetime.date.today() - datetime.timedelta(days=1)
yesterday = datetime.date.today() - datetime.timedelta(days=2)
today_end = str(today) + " 20:00:00"
yesterday_end = str(yesterday) + " 20:00:00"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
AV_ENDPOINT = "https://www.alphavantage.co/query"
AV_API_KEY = "W80D7G3OO1W43CNI"
AV_API_PARAMS = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "datatype": "json",
    "apikey": AV_API_KEY
}

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "b371ff702c36422ab68b193e7bd1ee88"
NEWS_API_PARAMS = {
    "apiKey": NEWS_API_KEY,
    "q": STOCK,
    "domains": "bloomberg.com"
}


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_response = requests.get(AV_ENDPOINT, params=AV_API_PARAMS)
stock_response.raise_for_status()
stock_data = stock_response.json()

today_stock_end = float(stock_data["Time Series (60min)"][today_end]["4. close"])
yesterday_stock_end = float(stock_data["Time Series (60min)"][yesterday_end]["4. close"])
percent_change = (abs(today_stock_end - yesterday_stock_end) / yesterday_stock_end) * 100

print(f"Today's {STOCK} closing price was {today_stock_end}\n"
      f"Yesterday's {STOCK} closing price was {yesterday_stock_end}\n"
      f"The percentage change was {int(percent_change)}%.")

if percent_change >= 5:
    print("Get News.")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_response = requests.get(NEWS_API_ENDPOINT, params=NEWS_API_PARAMS)
news_response.raise_for_status()
stock_news_data = news_response.json()

for i in range(0, 5):
    description = stock_news_data["articles"][i]["description"]
    url = stock_news_data["articles"][i]["url"]
    print(f"{description}\n{url}\n")

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """


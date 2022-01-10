import requests
import datetime
import smtplib
import json
import math

def diff_round(n):
    if n == 0:
        return 0
    sgn = -1 if n < 0 else 1
    scale = int(-math.floor(math.log10(abs(n))))
    if scale <= 0:
        scale = 1
    factor = 10 ** scale
    return sgn * math.floor(abs(n) * factor) / factor


def send_news(change):
    news_params = {
        "q": value,
        "apikey": "4cccbfbba1674de691b15294982bfe94"
    }
    news_req = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
    news = news_req.json()["articles"][:3]
    if change > 0:
        up_down = "+"
    else:
        up_down = "-"
    global msg
    msg += f"{key}: {up_down}{abs(change)}%\n"
    for i in range(0, 3):
        msg += f"Headline: {news[i]['title']}\n" \
               f"link: {news[i]['url']}\n\n"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        username = "alexleetest123@gmail.com"
        password = "testpassword@123"
        connection.starttls()
        connection.login(user=username, password=password)
        with open("email.json") as data:
            people = json.load(data)
            for name, email in people.items():
                try:
                    connection.sendmail(from_addr=username, to_addrs=email, msg=msg)
                except smtplib.SMTPRecipientsRefused:
                    print(f"email failed to sent to {name} at {email} ")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
today = datetime.date.today()
if 2 <= today.weekday() <= 5:
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)
elif today.weekday() == 0:

    yesterday = today - datetime.timedelta(days=2)
    day_before_yesterday = today - datetime.timedelta(days=3)
elif today.weekday() == 6:
    yesterday = today - datetime.timedelta(days=3)
    day_before_yesterday = today - datetime.timedelta(days=4)
else:
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=4)
msg = f"Subject:Stock Update from {day_before_yesterday} to {yesterday} \n\n"
with open("stocks.json") as file:
    try:
        data = json.load(file)
    except json.decoder.JSONDecodeError:
        print("You didn't enter any stocks and companies")
    else:
        for key, value in data.items():
            stock_params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": key,
                "apikey": "8KXBGNJYAER150DG"
            }
            stock_req = requests.get(url="https://www.alphavantage.co/query", params=stock_params)
            stock_req.raise_for_status()
            stock_data = stock_req.json().get("Time Series (Daily)")
            try:
                yesterday_open_price = stock_data[str(yesterday)]["1. open"]
            except TypeError:
                print(f"failed to get stock for {key}")
            else:
                day_before_yesterday_open_price = stock_data[str(day_before_yesterday)]["1. open"]
                change_in_price = (float(yesterday_open_price) - float(day_before_yesterday_open_price)) / float(
                    yesterday_open_price)
                if abs(change_in_price) >= 0:
                    send_news(diff_round(change_in_price))

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

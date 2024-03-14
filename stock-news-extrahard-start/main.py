import requests
import datetime as dt
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
one over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have g
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
subject = ""
message = ""

stock_parameters={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "ENTER TOKEN"
}

news_parameters={
    "apiKey":"ENTER TOKEN",
    "q":COMPANY_NAME,
}

#api for stock
stock_response = requests.get(
    url="https://www.alphavantage.co/query", 
    params=stock_parameters)

stock_response.raise_for_status()
stock_data = stock_response.json()

#api for new
news_response = requests.get(
    url="https://newsapi.org/v2/top-headlines",
    params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
articles = news_data["articles"][0:3]

#time
time = dt.datetime
now = time.now()
today_date = now.date()
yesterday = today_date.isoweekday() - 1 #will turn the day into int (monay=1, sunday=7)
week_num = time.today().isocalendar()[1]
yesterday_date = today_date.fromisocalendar(year=today_date.year, week=week_num, day=yesterday-1)
dayb4yesterday_day = yesterday_date.fromisocalendar(year=today_date.year, week=week_num, day=yesterday-2)

hour = str(now.time()).split(":")[0]
hour = int(hour)

yesterday_closed_price = float(stock_data["Time Series (Daily)"][f"{yesterday_date}"]["4. close"])
dayb4yesterday_closed_price = float(stock_data["Time Series (Daily)"][f"{dayb4yesterday_day}"]["4. close"])

#functions to calculate prices + generate message + subject
def calculate_close_price():
    global message
    different_closed_price = yesterday_closed_price - dayb4yesterday_closed_price
    percentage = (different_closed_price/dayb4yesterday_closed_price)*100
    if percentage > 0:
        message += f"{STOCK}: 🔺{float(percentage)}%\n\n"
    else:
        message += f"{STOCK}: 🔻{float(percentage)}%\n\n"
    return message

def generate_news():
    global message
    for i in range(0, 3):
        articles_title = articles[i]["title"]
        articles_desc = articles[i]["description"]
        articles_link = articles[i]["url"]
        #articles_image = articles[i]["urlToImage"]
        message += f"Headline: {articles_title}\nBrief: {articles_desc}\nClick on the link to read more: {articles_link}\n----------------------------------------------------\n"

def generate_subjct():
    global subject
    subject += f"Reminder: {message}"

def generate_message():
    calculate_close_price()
    generate_subjct()
    generate_news()
    #print_message = print(message)
    #return print_message

#call the function
generate_message()

#send email

user = "ENTER TOKEN"
password = "ENTER TOKEN"

if hour == 2:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=user, password=password)
    connection.sendmail(from_addr=user, to_addrs=user, msg=f"Subject: {subject}\n\n {message}.".encode("utf-8"))
    connection.close()




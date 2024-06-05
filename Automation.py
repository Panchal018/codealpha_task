import os
import requests # type: ignore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup # type: ignore
import schedule # type: ignore
import time

def rename_files(directory, new_name):
    for count, filename in enumerate(os.listdir(directory)):
        dst = f"{new_name}_{str(count)}.txt"
        src = f"{directory}/{filename}"
        dst = f"{directory}/{dst}"
        os.rename(src, dst)

def scrape_weather():
    url = 'https://example.com/weather'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    weather = soup.find('div', class_='weather').text
    return weather

def send_email(subject, body, to_email):
    from_email = "pa908114@gmail.com"
    password = "ak@pa123"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def daily_tasks():
    weather = scrape_weather()
    send_email("Daily Weather Report", weather, "recipient@example.com")
    rename_files('/path/to/directory', 'new_create_file')

schedule.every().day.at("07:00").do(daily_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)

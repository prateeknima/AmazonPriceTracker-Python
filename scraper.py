import requests
from bs4 import BeautifulSoup
import re
import smtplib
import time

#Set the link of the product to be tracked
url = "https://www.amazon.co.uk/Amazon-Kindle-Paperwhite-Waterproof-Twice-Storage/dp/B07747FR44/ref=sr_1_2?dchild=1&keywords=KINDLE&qid=1604670466&sr=8-2"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

page = requests.get(url, headers = headers)

bs = BeautifulSoup(page.content, 'html.parser') 

#set your tracking price for the product
trackPrice = 120
#Configure your email ID here
senderEmailID = ""
receiverEmailID = ""
#Setting up your password(For you don't wnat to type in your password you can generate an APP password through gmail security)
#Its format would be something like "oyiazadnxlkugaal
senderEmailPassword = ""    
currentPrice = 0

def trackProductPrice():
    product_title = bs.find(id="productTitle").get_text()
    price = str(bs.find(id="price_inside_buybox").get_text())
    price = price.split(".", 1)[0]
    price = re.sub("\W+","",price)
    global currentPrice
    currentPrice = float(price)  
    return float(price)
    
def email_service():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    #Setting up your login credentials

    server.login(senderEmailID,senderEmailPassword)
    subject = "The amazon product price is within your buy range"
    body = f"Buy before the price fluctuates \nYour desired price:{trackPrice}, Current price: {currentPrice} \nLink to the product : {url}"
    msg = f"Subject: {subject}\n\n\n{body}"    
    server.sendmail(senderEmailID,receiverEmailID,msg)
    server.quit()

#Running the loop each hour until the price falls below the desried price
while True:
    if(trackProductPrice() < trackPrice):
         email_service()
         break
    time.sleep(36000)

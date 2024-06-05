import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_EMAIL = YOUR_EMAIL_ID
PASSWORD = YOUR_PASSWORD
TO_ADDRESS = TO_ADDRESS

AMAZON_URL ="https://www.amazon.com/LEVOIT-Purifiers-Bedroom-Washable-Vital100S/dp/B0BNDM2RNG/ref=sr_1_5?crid=382J1K6E1UP95&dib=eyJ2IjoiMSJ9.i4cA1iQYMNtU0TUfP4n7vRjCcR5ufQL4DBIxZAstZhYv9c9qMMGGOdfaUl_hMHFY-eDmam24rTg5HxJB7WCCMnXIhy1yVJ9RZhxnZld4YmYlCGwHr9kGAWkM5_HC5ErtcM4U0qISXDg8mYw-Iup-J6OzY6FLUQY7B5fN0UDUSyR5G_S4wi4nNXsvfQ2y-s0OVaabBZQfbmE2qsi26Fezqe-CcyhWHh2H8zqnujU1DGo.B1mgKMsjoBQ-A6SDVTxxZrNNAVMn2mHRS6iMR2MvRX8&dib_tag=se&keywords=air%2Bpurifiers%2Bfor%2Bhome&psr=EY17&qid=1717394813&s=todays-deals&sprefix=air%2Bpuri%2Ctodays-deals%2C317&sr=1-5&th=1"
headers = {
    "Accept-Language" : "en-US,en;q=0.9",
    "User-Agent" :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

response = requests.get(AMAZON_URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

price_of_product = soup.find(class_="a-price").getText()
price_without_curr = price_of_product.split("$")[1]
price_as_float = float(price_without_curr)

BUY_PRICE = 150

if price_as_float < BUY_PRICE:
    message = soup.title.getText().strip()
    msg_dict = MIMEMultipart()
    msg_dict['From'] = MY_EMAIL
    msg_dict['To'] = TO_ADDRESS,
    msg_dict['Subject'] = "Amazon Price Alert!"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        try:
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=TO_ADDRESS,
                                msg=f"Subject: Amazon Price Alert!\n\n{message}\n\n{AMAZON_URL}".encode("utf-8")
                                )
        except ConnectionRefusedError:
            print("Error in sending email.")
        else:
            print("Email Sent.")

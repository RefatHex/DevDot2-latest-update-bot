import requests
from bs4 import BeautifulSoup

URL = 'https://dev.to/latest'

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

post = soup.find("div", class_="crayons-story__body")
title = post .find("h2", class_="crayons-story__title").text.strip()

print(title)

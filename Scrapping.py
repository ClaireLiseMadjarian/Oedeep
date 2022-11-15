from bs4 import BeautifulSoup
import requests

lien = 'https://digitalcomicmuseum.com'
page = requests.get(lien)
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.head)


from bs4 import BeautifulSoup
import requests

with open("https://digitalcomicmuseum.com") as f:
    soup = BeautifulSoup(f,'html.parser')

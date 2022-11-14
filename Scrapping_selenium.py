
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests

def login():
    driver.get("https://digitalcomicmuseum.com/login.php")
    username = driver.find_element(By.XPATH, '//*[@id="user"]')
    username.clear()
    username.send_keys('ClaireM')
    paswd = driver.find_element(By.XPATH, '//*[@id="passwrd"]')
    paswd.clear()
    paswd.send_keys('MINALES4432')
    submit = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/form/div/table/tbody/tr[2]/td[2]/div/input")
    submit.click()
driver = webdriver.Firefox()
login()
url = "https://digitalcomicmuseum.com/index.php?dlid="
for i in range(1000,1200):
    try :
        new_url = url + str(i)
        driver.get(new_url)
        #driver.get("https://digitalcomicmuseum.com/index.php?dlid=18772")
        temp = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[4]/div/a/img")

    except :
        continue
    temp.click()
    time.sleep(20)



"""
url = "https://digitalcomicmuseum.com/index.php?dlid="
for i in range(50000):
    new_url = url + str(i)
    driver.get(url)
    temp = driver.findElement(By.xpath("//img[@src='/images/download.gif']"))
# element = driver.find_element(By.LINK_TEXT, "index.php?cid=962")
# element.send_keys( Keys.ARROW_DOWN)
#print(driver.title)
"""
driver.close()
# <a href="index.php?cid=962">DCM Archives and Collections</a> C:\Users\jeronimo\Downloads\000.jpg
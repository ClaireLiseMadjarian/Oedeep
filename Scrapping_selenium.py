
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import subprocess

from os import listdir
from os.path import isfile, join

def get_genre():
    cellule = driver.find_element(By.XPATH, '//*[@id="catname"]')
    txt = cellule.text
    genre = txt.split("Search Results for the Genre: ")[1].split(" (sortable)")[0]
    return(genre)

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

def get_all_files():

    url = "https://digitalcomicmuseum.com/index.php?dlid="
    for i in range(1000, 1200):
        try:
            new_url = url + str(i)
            driver.get(new_url)
            # driver.get("https://digitalcomicmuseum.com/index.php?dlid=18772")
            temp = driver.find_element(By.XPATH,
                                       "/html/body/table[2]/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[4]/div/a/img")

        except:
            continue
        temp.click()
        time.sleep(20)


def get_files_by_genre(id):
    url = "https://digitalcomicmuseum.com/index.php?ACT=dogenresearch&terms="+str(id)
    driver.get(url)
    i = 1
    while(True):
        try :
            path = "/html/body/table[2]/tbody/tr/td/div[1]/div/table/tbody[1]/tr["+ str(i)+ "]/td[1]/a"
            link = driver.find_element(By.XPATH, path)
            link.click()
            temp = driver.find_element(By.XPATH,
                                       "/html/body/table[2]/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[4]/div/a/img")
            temp.click()
            time.sleep(20)



            i+=1
            driver.get(url)
        except:
            break




driver = webdriver.Firefox()
login()
get_files_by_genre(1)
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

def extract_file(filename, dict):
    pass
# <a href="index.php?cid=962">DCM Archives and Collections</a> C:\Users\jeronimo\Downloads\000.jpg
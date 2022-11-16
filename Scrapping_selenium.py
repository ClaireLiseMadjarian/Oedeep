from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import bs4
import os
from os import listdir
from os.path import isfile, join
import subprocess
import pandas as pd

id = 0
df = pd.DataFrame(columns=["id_img", "labels"])


def get_dico_genres(driver):
    dico = {}
    for id in range(1, 36):
        url = f'https://digitalcomicmuseum.com/index.php?ACT=dogenresearch&terms={id}'
        driver.get(url)
        cellule = driver.find_element(By.XPATH, '//*[@id="catname"]')
        txt = cellule.text
        genre = txt.split("Search Results for the Genre: ")[1].split(" (sortable)")[0]
        dico[genre] = id
    return (dico)


def login(driver):
    driver.get("https://digitalcomicmuseum.com/login.php")
    username = driver.find_element(By.XPATH, '//*[@id="user"]')
    username.clear()
    username.send_keys('ClaireM')
    paswd = driver.find_element(By.XPATH, '//*[@id="passwrd"]')
    paswd.clear()
    paswd.send_keys('MINALES4432')
    submit = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/form/div/table/tbody/tr[2]/td[2]/div/input")
    submit.click()


def get_all_files(driver):
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


def get_files_by_genre(id, driver):
    url = "https://digitalcomicmuseum.com/index.php?ACT=dogenresearch&terms=" + str(id)
    driver.get(url)
    i = 1
    while (True):
        try:
            path = "/html/body/table[2]/tbody/tr/td/div[1]/div/table/tbody[1]/tr[" + str(i) + "]/td[1]/a"
            try:
                list_pages = driver.find_elements(By.TAG_NAME, 'td')
            except:
                pass

            link = driver.find_element(By.XPATH, path)
            link.click()
            temp = driver.find_element(By.XPATH,
                                       "/html/body/table[2]/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[4]/div/a/img")
            before = os.listdir(".\cbr_files")
            temp.click()
            time.wait(20)
            # TODO complete file_path with filename
            # wait_download(file_path)
            after = os.listdir(".\cbr_files")
            change = set(after) - set(before)
            if len(change) == 1:
                file_name = change.pop()
            else :
                raise FileNotFoundError("unable to find downloaded file")
            extract_comic(file_name)
            i += 1
            driver.get(url)
        except:
            break


def genres_nbpages(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    pages = soup.find_all("td", {'width': '175'})
    nb_pages = []
    bd_genres = []
    for p in pages:
        t = p.text
        gen = t.rsplit(' (', 1)[0]
        nb = t.split('(')[1].split(')')[0]
        nb_pages.append(nb)
        bd_genres.append(gen)
    return bd_genres, nb_pages



def scrap() :
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir",
                           r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files")
    driver = webdriver.Firefox(firefox_profile=profile)
    login(driver)

    dico = get_dico_genres(driver)
    for i in range(1,35):
        get_files_by_genre(i,driver)


    driver.close()


def extract_comic(filename, bd_genres, pages):
    global id
    global df
    command = '7z e ".\cbr_files\\' + filename + '" -o".\extraction" -y'
    subprocess.run(
        command,
        shell=True)
    del_files()
    mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\extraction'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    i = 0
    for file in onlyfiles:
        if file.endswith(".jpg"):
            destination = ".\jpg_files\\" + str(id)
            os.rename(file, destination)
            id += 1
            i += 1
            genre = get_genre(i, bd_genres, pages)
            new_row = pd.Series({"id_img": id, "labels": genre})
            df = pd.concat([df, new_row.to_frame().T], ignore_index = True)


def get_genre(i, bd_genres, pages):
    for j in pages:
        if pages[0] <= i and i <= pages[1]:
            return bd_genres[pages.index(j)]


def del_files():
    mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        os.remove(file)


def wait_download(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)

    if os.path.isfile(file_path):
        pass
    else:
        raise ValueError("%s isn't a file!" % file_path)
scrap()
df.to_csv("labels.csv")
"""'
url = "https://digitalcomicmuseum.com/index.php?dlid="
for i in range(50000):
    new_url = url + str(i)
    driver.get(url)
    temp = driver.findElement(By.xpath("//img[@src='/images/download.gif']"))
# element = driver.find_element(By.LINK_TEXT, "index.php?cid=962")
# element.send_keys( Keys.ARROW_DOWN)
#print(driver.title)
"""
# <a href="index.php?cid=962">DCM Archives and Collections</a> C:\Users\jeronimo\Downloads\000.jpg

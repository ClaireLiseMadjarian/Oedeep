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

id = (0)
df = pd.DataFrame(columns=["id_img", "labels"])


def get_dico_genres(driver):
    dico = {}
    for id in range(1, 41):
        try:
            url = f'https://digitalcomicmuseum.com/index.php?ACT=dogenresearch&terms={id}'
            driver.get(url)
            cellule = driver.find_element(By.XPATH, '//*[@id="catname"]')
            txt = cellule.text
            genre = txt.split("Search Results for the Genre: ")[1].split(" (sortable)")[0]
            dico[genre] = id
        except:
            pass
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


def get_files_by_genre(id, driver, dico, df):
    i = 1
    while (True):
        url = "https://digitalcomicmuseum.com/index.php?ACT=dogenresearch&terms=" + str(id)
        driver.get(url)
        try:
            path = "/html/body/table[2]/tbody/tr/td/div[1]/div/table/tbody[1]/tr[" + str(i) + "]/td[1]/a"
            link = driver.find_element(By.XPATH, path)
            link.click()
            temp = driver.find_element(By.XPATH,
                                       "/html/body/table[2]/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[4]/div/a/img")
        except:
            break
        before = os.listdir(".\cbr_files")

        bd_genres, pages = [], []
        j = 1
        nb_pages = 1
        nb_block = 2
        while True:
            try :
                block = driver.find_element(By.XPATH,   '/html/body/table[2]/tbody/tr/td/div[1]/div[' + str(nb_block)+']')
                if "Grand Comic Database" in block.text :
                    break;
                else :
                    nb_block += 1
            except:
                break
        while True:
            try:
                table = driver.find_element(By.XPATH,
                                            "/html/body/table[2]/tbody/tr/td/div[1]/div[" + str(nb_block)+ "]/table/tbody/tr/td/table/tbody/tr[3]/td/table[" + str(
                                                j) + "]")

            except:
                break

            content = table.text.split()
            if "page)" in content:
                id_page = content.index("page)") - 1
            else:
                id_page = content.index("pages)") - 1

            pages.append([nb_pages, int(content[id_page][1:]) + nb_pages - 1])
            nb_pages += int(content[id_page][1:])
            try:
                if "Genre:" in table.text:
                    g = []
                    for key in dico.keys():
                        if key in table.text:
                            g.append(dico.get(key))
                    if len(g) > 0 :
                        bd_genres.append(g)
                    else :
                        bd_genres.append([0])
                else:
                    bd_genres.append([0])
                # id_genre = content.index("Genre:") + 1
                # if dico.get(content[id_genre]) is None:
                #     bd_genres.append(0)
                # else:
                #     bd_genres.append(dico.get(content[id_genre]))

                j += 1
            except:
                bd_genres.append([0])
                j += 1

        temp.click()
        # TODO complete file_path with filename
        file_path = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files"
        wait_download(file_path)
        after = os.listdir(".\cbr_files")
        change = set(after) - set(before)
        if len(change) == 1:
            file_name = change.pop()
        else:
            i+=1
            del_files()
            continue
            # raise FileNotFoundError("unable to find downloaded file")
        df = extract_comic(file_name, bd_genres, pages, df)
        i += 1
    df.to_csv("labels.csv", mode = 'a', index=False, header=False)
    print("finish genre : ", id)
    print("finish id :", i)
    return df



def genres_nbpages(url, driver):
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
    print("genres : ", bd_genres)
    print("nb_pages : ", nb_pages)
    return bd_genres, nb_pages


def scrap(df):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir",
                           r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files")
    driver = webdriver.Firefox(firefox_profile=profile)
    login(driver)

    dico = get_dico_genres(driver)
    for i in range(1, 39):
        df = get_files_by_genre(i, driver, dico, df)

    driver.close()
    return df


def extract_comic(filename, bd_genres, pages, df):
    print("extract comic :", filename)
    global id
    command = '7z e ".\cbr_files\\' + filename + '" -o".\extraction" -y'
    subprocess.run(
        command,
        shell=True)
    mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\extraction'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    i = 1
    for file in onlyfiles:
        if file.endswith(".jpg"):
            source = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\extraction\%s' %file
            name = str(id)+".jpg"
            destination = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\jpg_files\%s' %name

            os.rename(source, destination)

            genre = get_genre(i, bd_genres, pages)
            if genre is None :
                genre = [0]
            new_row = pd.Series({"id_img": id, "labels": genre[0]})
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
            id += 1
            i += 1
    del_files()
    return df


def get_genre(i, bd_genres, pages):
    for j in pages:
        if j[0] <= i and i <= j[1]:
            return bd_genres[pages.index(j)]


def del_files():
    mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        os.remove(os.path.join(mypath,file))
    mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\extraction'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        os.remove(os.path.join(mypath, file))


def wait_download(directory, timeout=175):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        files = os.listdir(directory)

        for fname in files:
            if fname.endswith('.cbr') or fname.endswith('.cbz'):
                dl_wait = False
        for fname in files:
            if fname.endswith('.part'):
                dl_wait = True
        seconds += 1
        print(seconds)
    return seconds


df = scrap(df)
df.to_csv("labels.csv", mode = 'a', index=False, header=False)
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

import requests, os, time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import html
import datetime
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()


def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(options=options)

# LOGIN = os.environ["LOGIN"]

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# URL="https://cahier-de-prepa.fr/mp2i-fermat/docs"
# BASE_URL="https://cahier-de-prepa.fr/mp2i-fermat/"
print("Entrez l'url du site sous la forme: https://cahier-de-prepa.fr/<lycée>/")
BASE_URL= input("URL: ")
URL=BASE_URL + "docs"

driver  = initialize_driver()

def get_lycee():
    driver.get(BASE_URL)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    h1 = soup.find("h1")
    assert h1 != None
    return h1.get_text()

def download(url, out):
    r = requests.get(url, allow_redirects=True)
    open(nom+"/"+out, 'wb').write(r.content)


def explorer(url,page_name):

    if not os.path.exists(nom+"/"+page_name):
        os.makedirs(nom+"/"+page_name)

    print(page_name)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    for file in soup.select("p.doc"):
        link = file.find("a")
        name  = file.find_all("span")
        t = name[2].get_text()
        _type=name[0].get_text()
        ext = _type.split(",")[0][1:]
        if not t.startswith(page_name) and ext != "":
            assert link  != None
            # print(link["href"],t,ext)
            print(f"Téléchargement de {t}.{ext}...")
            download(BASE_URL+link["href"], page_name+"/"+ t+"."+ext)
    

    dirs = []
    for p in soup.select("p.rep"):
        link = p.find("a")
        name  = p.find_all("span")
        new_dir = page_name+"/"+name[2].get_text()
        mkdir(nom+"/"+new_dir)
        explorer(URL+link["href"],new_dir)
        # dirs.append((link["href"], ))
    # print(dirs)

def login():
    element = driver.find_element(By.XPATH, "/html/body/nav/div[1]/a[6]")
    element.click()
    username_input = driver.find_element(By.XPATH,"/html/body/article/form/input[1]")
    username_input.send_keys(os.environ["UTILISATEUR"])
    pass_input = driver.find_element(By.XPATH,"/html/body/article/form/input[2]")
    pass_input.send_keys(os.environ["MOT_DE_PASSE"])

    ok = driver.find_element(By.XPATH,"/html/body/article/a[2]")
    ok.click()

    time.sleep(2)


nom = get_lycee()

def main():
    driver.get(URL)

    if os.environ["LOGIN"] == "true":
        login()
        
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    dirs = []
    for p in soup.select("p.rep"):
        link = p.find("a")
        name  = p.find_all("span")
        dirs.append((link["href"], name[2].get_text()))

    mkdir(nom)

    # print(dirs)
    for dir in dirs:
        new_url = URL+dir[0]
        explorer(new_url,dir[1])

main()
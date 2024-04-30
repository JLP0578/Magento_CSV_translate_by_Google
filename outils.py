# External
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pprint
import time
import csv
import sys
import subprocess

# doenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

def dd(*args):
    for arg in args:
        pprint.pprint(arg)
        print("-" * 40)
    sys.exit()

def read_file(file_name):
    result = []
    with open(file_name, "r", newline="") as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv)
        for ligne in lecteur_csv:
            result.append(ligne)

    return result

def append_file(file_name, data_array):
    with open(file_name, "a", newline="", encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(['"' + str(item).replace('"', '\\"').replace('\n', '\\n') + '"' for item in data_array])

def create_file(file_name):
    open(file_name, "w").close()

def worker(datas):
    domain = 'https://translate.google.com/?sl=en&tl=fr&op=translate'
    name_file = './output.csv'

    try:
        print(f"Process : Wake Up")

        # Chrome
        options = ChromeOptions()

        # Firefox
        # options = FirefoxOptions()

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        # options.add_argument("--headless")

        # Chrome
        driver = webdriver.Chrome(options=options)

        # Firefox
        # driver = webdriver.Firefox(options=options)

        driver.get(domain)
        consent = driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Tout refuser\"]:first-child")
        consent.click()        
        
        for data in datas:
            text_input = driver.find_element(By.CSS_SELECTOR,"textarea.er8xn")
            text_input.clear()
            text_input.send_keys(data[0])
            text_input.send_keys(Keys.ENTER)

            time.sleep(5)

            text_output = driver.find_element(By.CSS_SELECTOR,"span.HwtZe:first-child")

            append_file(name_file, [data[0], text_output.text])

        driver.quit()
    except Exception as e:
        print(f"Process : Une erreur - {e}")
    finally:
        format_output_file = "(Get-Content output.csv) | ForEach-Object {$_ -replace '\"\"\"', '\"'} | Set-Content output.csv"
        subprocess.run(["powershell", format_output_file])
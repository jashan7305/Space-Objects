from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv(".env", override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

driver = webdriver.Chrome()
driver.get("https://www.space-track.org/auth/login")

usename_field = driver.find_element(By.ID, "identity")
password_field = driver.find_element(By.ID, "password")
login_btn = driver.find_element(By.NAME, "btnLogin")
usename_field.send_keys(username)
password_field.send_keys(password)
login_btn.click()
time.sleep(2)

driver.find_element(By.LINK_TEXT, "SATCAT").click()
time.sleep(2)
dropdown = driver.find_element(By.NAME, "satCatTable_length")
dropdown.send_keys("100") 
time.sleep(20)

norad_ids = []
sat_names = []
intldess = []
types = []
countries = []
launch_dates = []
launch_sites = []
decay_dates = []
periods = []
inclinations = []
apogees = []
perigees = []

num_pages = 0
while num_pages < 10:
    rows = driver.find_elements(By.XPATH, "//*[@id='satCatTable']/tbody/tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        norad_ids.append(cells[0].text.strip())
        sat_names.append(cells[1].text.strip())
        types.append(cells[3].text.strip())
        countries.append(cells[4].text.strip())
        launch_dates.append(cells[5].text.strip())
        launch_sites.append(cells[6].text.strip())
        decay_dates.append(cells[7].text.strip())
        periods.append(cells[8].text.strip())
        inclinations.append(cells[9].text.strip())
        apogees.append(cells[10].text.strip())
        perigees.append(cells[11].text.strip())

    
    next_button = driver.find_element(By.LINK_TEXT, "Next")
    next_button.click()
    num_pages += 1
    time.sleep(2)

driver.quit()

df = pd.DataFrame({
    "NoradID": norad_ids,
    "SatName": sat_names,
    "Country": countries,
    "LaunchSite": launch_sites,
    "Type": types,
    "LaunchDate": launch_dates,
    "DecayDate": decay_dates,
    "Period": periods,
    "Inclination": inclinations,
    "Apogee": apogees,
    "Perigee": perigees
})

df.to_excel("SpaceObjects.xlsx", index=False)
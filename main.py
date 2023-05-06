import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

s = Service('/Users/Daniel/Desktop/chromedriver_win32')
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=s, options=options)
driver.get('https://www.mtggoldfish.com/metagame/modern/full#paper')
driver.maximize_window()
print("connected...")

deckNames = driver.find_elements(By.CLASS_NAME, "archetype-tile-title")
metaPercentAndPrice = driver.find_elements(By.CLASS_NAME, "archetype-tile-statistic-value")
deckColors = driver.find_elements(By.XPATH, "//div[@class='manacost-container']")
print("raw data received...")

maxNum = 50

deckNamesTxt = []
for i in range(maxNum):
    if deckNames[i] != "":
        deckNamesTxt.append(deckNames[i].text)
print("deck names done...")

metaPercentTxt = []
deckPriceTxt = []
count = 0
for i in metaPercentAndPrice:
    if i.text != "" and not i.text.startswith('$'):
        metaPercentTxt.append(i.text.split(" ")[0])
        count += 1
    elif i.text != "":
        deckPriceTxt.append('$' + i.text.split(" ")[1])
        count += 1
    if count >= maxNum * 2:
        break
print("deck meta percents and prices done...")

deckColorsTxt = []
for i in range(maxNum):
    try:
        colors = deckColors[i].find_element(By.XPATH, ".//span[@class='manacost']").get_attribute("aria-label")
        deckColorsTxt.append(colors.split(": ")[1])
    except selenium.common.exceptions.NoSuchElementException:
        deckColorsTxt.append("colorless")
print("deck colors done..")

table = {"Deck Name": deckNamesTxt,
         "Deck Color(s)": deckColorsTxt,
         "Meta Percentage": metaPercentTxt,
         "Deck Price": deckPriceTxt}


df = pd.DataFrame(table)

print("printing dataframe...")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df)

df.to_csv('MTG_Data.csv')

driver.quit()

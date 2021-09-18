import os
import time
import datetime
import gspread as gs ##'4.0.1'
import pandas as pd  ##1.3.3
from selenium import webdriver ## '3.141.0'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from df2gspread import df2gspread as d2g ## 1.0.4
from oauth2client.service_account import ServiceAccountCredentials
import apscheduler ##3.7.0

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path='./WebDriver/bin/chromedriver', chrome_options=options)
  

COLUMNS = ['Date',
'Total Sales',
'#Orders',
'Sessions',
'Retention Rate',
'Conversion']



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gc = gs.authorize(creds)

SHEET_ID = '1D1ing_OqL0sCNPK2rXL-OheX-bGImPAnHmivfhxuhlU'
SHEET_NAME = 'e-commerce'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(SHEET_ID, SHEET_NAME)


df = pd.read_csv(SHEET_URL)
df = df[COLUMNS]

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD') 

LOGIN_PAYLOAD = {
                    "username": username,
                    "password":password
                }

EMAIL_ID = 'account_email'
PASSWORD_ID = "account_password"
LOGIN_URL = 'https://accounts.shopify.com/lookup?rid=31a7c4ab-0171-45b4-bcd5-90587a5fbe7b'
LOGIN_SUBMIT_XPATH = '//*[@id="body-content"]/div[1]/div/div/div/div/div[2]/div/form/button'
LOGIN_SUBMIT_NAME = 'commit'
SHOPIFY_PARTNER_XPATH = '//*[@id="AppFrameMain"]/div/div/div/div/form/section[3]/div/div[2]/section[2]/ul/li/div/div/a'
SHOPIFY_STORE_XPATH = '//*[@id="29920460884"]/div/div/div[3]/div[2]/a'
ACCOUNT_XPATH = '//*[@id="body-content"]/div[1]/div/div/div/div/div[2]/div/div/a[1]'
ANALYTICS_XPATH ='//*[@id="AppFrameNav"]/nav/div[2]/ul[1]/li[5]/div[1]/a/span'


SALES_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
SESSIONS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
RETENTION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
CONVERSION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
ORDERS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'

driver = webdriver.Chrome(executable_path='./WebDriver/bin/chromedriver', chrome_options=options)
driver.get(LOGIN_URL)
driver.find_element_by_id(EMAIL_ID).send_keys(LOGIN_PAYLOAD["username"])  
driver.find_element_by_name(LOGIN_SUBMIT_NAME).click()
time.sleep(1)e
driver.find_element_by_id(PASSWORD_ID).send_keys(LOGIN_PAYLOAD["password"]) 
driver.implicitly_wait(20) 
driver.find_element_by_name(LOGIN_SUBMIT_NAME).click()
time.sleep(1)
driver.find_element_by_xpath(SHOPIFY_PARTNER_XPATH).click()
time.sleep(1)
driver.switch_to.window(driver.window_handles[-1])
driver.find_element_by_xpath(ACCOUNT_XPATH).click()
driver.find_element_by_xpath(SHOPIFY_STORE_XPATH).click()
driver.switch_to.window(driver.window_handles[-1])
driver.find_element_by_xpath(ANALYTICS_XPATH).click()

date = datetime.date.today().strftime('%Y-%m-%d')
sales = driver.find_element_by_xpath(SALES_XPATH).text
orders = driver.find_element_by_xpath(ORDERS_XPATH).text
sessions = driver.find_element_by_xpath(SESSIONS_XPATH).text
retention = driver.find_element_by_xpath(RETENTION_XPATH).text
conversion = driver.find_element_by_xpath(CONVERSION_XPATH).text

driver.quit()

data_dict = {'Date':[date],
'Total Sales':[sales],
'#Orders':[orders],
'Sessions':[sessions],
'Retention Rate':[retention],
'Conversion':[conversion]}

new_row = pd.DataFrame.from_dict(data_dict)

df = pd.concat([df, new_row])
df.to_csv('history.csv', index=False)
d2g.upload(df, SHEET_ID, SHEET_NAME, credentials=creds, row_names=True)


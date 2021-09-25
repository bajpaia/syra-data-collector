import os
import time
import pandas as pd
import datetime
import gspread as gs
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



  

COLUMNS = ['Date',
'Total Sales',
'#Orders',
'Sessions',
'Retention Rate',
'Comversion']

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD') 
LOGIN_PAYLOAD = {
                    "username": username,
                    "password": password
                }

SHEET_ID = '1D1ing_OqL0sCNPK2rXL-OheX-bGImPAnHmivfhxuhlU'
SHEET_NAME = 'e-commerce'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(SHEET_ID, SHEET_NAME)
EMAIL_ID = 'account_email'
PASSWORD_ID = "account_password"
PASSWORD_XPATH = "/html/body/div[1]/div/div/div/div/div[2]/div/div/form/div[1]/div[2]/div/input"
LOGIN_URL = 'https://accounts.shopify.com/lookup?rid=6114de03-e4e2-4556-b60d-0f1d9568baab'
EMAIL_SUBMIT_XPATH = '/html/body/div[1]/div/div/div/div/div[2]/div/form/button'
EMAIL_FORM_XPATH = '//*[@id="body-content"]/div[1]/div/div/div/div/div[2]/div/form'
LOGIN_BUTTON_XPATH = '/html/body/div[1]/div/div/div/div/div[2]/div/div/form/div[2]/ul/button'
LOGIN_FORM_ID = 'login_form'
LOGIN_FORM_XPATH = '//*[@id="login_form"]'
SHOPIFY_PARTNER_XPATH = '//*[@id="AppFrameMain"]/div/div/div/div/form/section[3]/div/div[2]/section[2]/ul/li/div/div/a'
SHOPIFY_STORE_XPATH = '/html/body/div/div[2]/main/div/div/div[1]/div/div[1]/main/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/ul/li/div/div/div/div/div/div[3]/div[2]/a'
ACCOUNT_XPATH = '//*[@id="body-content"]/div[1]/div/div/div/div/div[2]/div/div/a[1]'
ANALYTICS_XPATH ='//*[@id="AppFrameNav"]/nav/div[2]/ul[1]/li[5]/div[1]/a/span'
DATE_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[1]/div[1]/div/button'
DATE_RANGE_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/select'
YESTERDAY_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/select/option[2]'
APPLY_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/div/div/div[2]/button'
SALES_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
SESSIONS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
RETENTION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
CONVERSION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
ORDERS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
CAPTCHA_CHECKBOX_XPATH = '//*[@id="recaptcha-anchor"]/div[2]'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
DATE_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[1]/div[1]/div/button'
START_DATE_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div/div/input'
END_DATE_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div/input'
APPLY_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/div/div/div[2]/button'
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)



def load_sheet(COLUMNS = ['Date', 'Total Sales', '#Orders', 'Sessions', 'Retention Rate', 'Conversion']):
    df = pd.read_csv(SHEET_URL)
    df = df[COLUMNS]
    return df

df = load_sheet()
print('Last updated value {}'.format(df['Date'].iloc[-1])) 
last_update = datetime.datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d')


yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
time_since_update = yesterday- last_update

print("Missed updates {}".format(time_since_update))


driver = webdriver.Chrome(executable_path='./WebDriver/bin/chromedriver')
driver.get(LOGIN_URL)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, EMAIL_ID))).send_keys(LOGIN_PAYLOAD["username"])  
print("added username")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, EMAIL_SUBMIT_XPATH))).click()
print("clicked next")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, PASSWORD_ID))).send_keys(LOGIN_PAYLOAD["password"])
print("added password")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))).click()
print("Logged in")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, SHOPIFY_PARTNER_XPATH))).click()
print("going to partner website")
driver.switch_to.window(driver.window_handles[-1])
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ACCOUNT_XPATH))).click()
print("logging into partner website")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, SHOPIFY_STORE_XPATH))).click()
print("going to store")
driver.switch_to.window(driver.window_handles[-1])
print("goint to analytics dashboard")
driver.find_element_by_xpath(ANALYTICS_XPATH).click()
time.sleep(2)



data_dict = {'Date':[],
'Total Sales':[],
'#Orders':[],
'Sessions':[],
'Retention Rate':[],
'Conversion':[]}



end_date = yesterday
delta = datetime.timedelta(days=1)
start_date = last_update + delta

if last_update != yesterday:
    while start_date <= end_date:
        start_date_str = start_date.strftime('%Y-%m-%d')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, DATE_XPATH))).click()
        time.sleep(1)
        driver.find_element_by_xpath(START_DATE_XPATH).send_keys(Keys.BACKSPACE*10)
        driver.find_element_by_xpath(START_DATE_XPATH).send_keys(start_date_str)
        driver.find_element_by_xpath(END_DATE_XPATH).send_keys(Keys.BACKSPACE*10)
        driver.find_element_by_xpath(END_DATE_XPATH).send_keys(start_date_str)
        driver.find_element_by_xpath(APPLY_XPATH).click()
        time.sleep(5)
        data_dict["Date"].append(start_date_str)
        data_dict["Total Sales"].append(driver.find_element_by_xpath(SALES_XPATH).text)
        data_dict["#Orders"].append(driver.find_element_by_xpath(ORDERS_XPATH).text)
        data_dict['Sessions'].append(driver.find_element_by_xpath(SESSIONS_XPATH).text)
        data_dict['Retention Rate'].append(driver.find_element_by_xpath(RETENTION_XPATH).text)
        data_dict['Conversion'].append(driver.find_element_by_xpath(CONVERSION_XPATH).text)
        start_date += delta
driver.quit()



rows = pd.DataFrame.from_dict(data_dict)
df = df.append( rows, ignore_index=True)
df.to_csv('history.csv')
d2g.upload(df, SHEET_ID, SHEET_NAME, credentials=creds, row_names=True)
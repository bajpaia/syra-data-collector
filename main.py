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
from apscheduler.schedulers.blocking import BlockingScheduler ##3.7.0


username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD') 

username = 'animesh.bajpai@protonmail.com'
password = '0BabyJ32,'

LOGIN_PAYLOAD = {
                    "username": username,
                    "password":password
                }
sched = BlockingScheduler()


SHEET_ID = '1D1ing_OqL0sCNPK2rXL-OheX-bGImPAnHmivfhxuhlU'
SHEET_NAME = 'e-commerce'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(SHEET_ID, SHEET_NAME)
EMAIL_ID = 'account_email'
PASSWORD_ID = "account_password"
LOGIN_URL = 'https://accounts.shopify.com/lookup?rid=6114de03-e4e2-4556-b60d-0f1d9568baab'
LOGIN_SUBMIT_XPATH = '//*[@id="body-content"]/div[1]/div/div/div/div/div[2]/div/form/button'
LOGIN_SUBMIT_NAME = 'commit'
SHOPIFY_PARTNER_XPATH = '//*[@id="AppFrameMain"]/div/div/div/div/form/section[3]/div/div[2]/section[2]/ul/li/div/div/a'
SHOPIFY_STORE_XPATH = '//*[@id="29920460884"]/div/div/div[3]/div[2]/a'
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
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'


creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gc = gs.authorize(creds)



def load_sheet(COLUMNS = ['Date', 'Total Sales', '#Orders', 'Sessions', 'Retention Rate', 'Conversion']):
    df = pd.read_csv(SHEET_URL)
    df = df[COLUMNS]
    return df




@sched.scheduled_job('cron', hour=7, minute=45)
# @sched.scheduled_job('cron', hour=22, minute=15)
def main():
    # options = Options()
    
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(executable_path='./WebDriver/bin/chromedriver', chrome_options=options)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(LOGIN_URL)
    driver.find_element_by_id(EMAIL_ID).send_keys(LOGIN_PAYLOAD["username"])  
    time.sleep(2)
    driver.find_element_by_name(LOGIN_SUBMIT_NAME).click()
    time.sleep(1)
    driver.find_element_by_id(PASSWORD_ID).send_keys(LOGIN_PAYLOAD["password"]) 
    time.sleep(1)
    driver.find_element_by_name(LOGIN_SUBMIT_NAME).click()
    time.sleep(1)
    driver.find_element_by_xpath(SHOPIFY_PARTNER_XPATH).click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath(ACCOUNT_XPATH).click()
    driver.find_element_by_xpath(SHOPIFY_STORE_XPATH).click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath(ANALYTICS_XPATH).click()
    time.sleep(2)
    driver.find_element_by_xpath(DATE_XPATH).click()
    driver.find_element_by_xpath(DATE_RANGE_XPATH).click()
    driver.find_element_by_xpath(YESTERDAY_XPATH).click()
    driver.find_element_by_xpath(APPLY_XPATH).click()
    time.sleep(2)
    delta = datetime.timedelta(days=1)
    date = datetime.date.today() - delta
    date= date.strftime('%Y-%m-%d')
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
    print(new_row)
    df = load_sheet()
    df = pd.concat([df, new_row])
    df.to_csv('history.csv', index=False)
    d2g.upload(df, SHEET_ID, SHEET_NAME, credentials=creds, row_names=True)


if __name__ == '__main__':
    sched.start()


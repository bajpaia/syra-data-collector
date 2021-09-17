
import time
import pandas as pd
# import df2gspread as df2g
import datetime
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
LOGIN_PAYLOAD = {
                    "username": "animesh.bajpai@protonmail.com",
                    "password": "0BabyJ32,"
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
PAGE_2_SCRAPE = 'https://syra-coffee.myshopify.com/admin/dashboards'

SALES_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
SESSIONS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
RETENTION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
CONVERSION_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'
ORDERS_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/p'



DATE_XPATH = '//*[@id="AppFrameMain"]/div/div/div[2]/div[1]/div[1]/div/button'
START_DATE_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div/div/input'
END_DATE_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div/input'
APPLY_XPATH = '/html/body/div/div/div[2]/div[4]/div/div/div[2]/div/div/div[2]/div/div/div[2]/button'


SHEET_ID = '1D1ing_OqL0sCNPK2rXL-OheX-bGImPAnHmivfhxuhlU'
SHEET_NAME = 'e-commerce'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(SHEET_ID, SHEET_NAME)



# df = pd.read_csv(SHEET_URL)
# print(df.head())


driver = webdriver.Chrome(executable_path='./WebDriver/bin/chromedriver')
driver.get(LOGIN_URL)
driver.find_element_by_id(EMAIL_ID).send_keys(LOGIN_PAYLOAD["username"])  
driver.find_element_by_name(LOGIN_SUBMIT_NAME).click()
time.sleep(1)
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
time.sleep(5)



data_dict = {'Date':[],
'Total Sales':[],
'#Orders':[],
'Sessions':[],
'Retention Rate':[],
'Conversion':[]}


start_date = datetime.date(2019,1,1)
end_date = datetime.date.today()
delta = datetime.timedelta(days=1)
while start_date <= end_date:
    start_date_str = start_date.strftime('%Y-%m-%d')
    driver.find_element_by_xpath(DATE_XPATH).click()
    time.sleep(1)
    driver.find_element_by_xpath(START_DATE_XPATH).send_keys(Keys.BACKSPACE*10)
    driver.find_element_by_xpath(START_DATE_XPATH).send_keys(start_date_str)
    driver.find_element_by_xpath(END_DATE_XPATH).send_keys(Keys.BACKSPACE*10)
    driver.find_element_by_xpath(END_DATE_XPATH).send_keys(start_date_str)
    driver.find_element_by_xpath(APPLY_XPATH).click()
    time.sleep(3)
    data_dict["Date"].append(start_date_str)
    data_dict["Total Sales"].append(driver.find_element_by_xpath(SALES_XPATH).text)
    data_dict["#Orders"].append(driver.find_element_by_xpath(ORDERS_XPATH).text)
    data_dict['Sessions'].append(driver.find_element_by_xpath(SESSIONS_XPATH).text)
    data_dict['Retention Rate'].append(driver.find_element_by_xpath(RETENTION_XPATH).text)
    data_dict['Conversion'].append(driver.find_element_by_xpath(CONVERSION_XPATH).text)


    start_date += delta


df = pd.DataFrame.from_dict(data_dict)
df.to_csv('history.csv')

driver.quit()


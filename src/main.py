from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


browser = webdriver.Chrome(
    executable_path='/home/serpant/AIAD/src/chromedriver')

browser.set_window_size(900, 900)

browser.set_window_position(0, 0)

sleep(1)
wait = WebDriverWait(browser, 10)
browser.get(
    'https://www.microsoftevents.com/profile/form/index.cfm?PKformID=0x236513835b')

wait.until(EC.presence_of_element_located((By.ID, "username")))

user_name_text_box = browser.find_element_by_id("username")

user_name_text_box.send_keys("info@seattleapplab.com")

password_textbox = browser.find_element_by_id("password")

password_textbox.send_keys("Cs240ta123")

sleep(2)

continue_button = browser.find_elements_by_css_selector(
    'input[value="Continue"]')

continue_button[0].click()

wait.until(EC.presence_of_element_located((By.ID, "pro_addr_line1")))

unique_report_id = browser.find_element_by_id("pro_addr_line1")

unique_report_id.send_keys("pkRptId=0x114908400001 & pkEvtId=0x20050900001")

sleep(2)


get_report_button = browser.find_elements_by_css_selector(
    'input[value="Get report"]')

get_report_button[0].click()

sleep(8)

another_window = list(set(browser.window_handles) -
                      {browser.current_window_handle})[0]
browser.switch_to.window(another_window)

wait.until(EC.presence_of_element_located((By.ID, "iFrameReportListDisplay")))

browser.switch_to.frame("iFrameReportListDisplay")

wait.until(EC.presence_of_element_located((By.ID, "reportResults")))

table_report_result = browser.find_elements_by_css_selector(
    "#reportResults")

headers = table_report_result[0].find_elements_by_css_selector('thead tr')

main_result = table_report_result[0].find_elements_by_css_selector('tbody')

html_header = headers[0].get_attribute('innerHTML')
html_table = main_result[0].get_attribute('innerHTML')

soup = BeautifulSoup(html_table, 'html.parser')
soupheader = BeautifulSoup(html_header, 'html.parser')

table_data_rows = soup.find_all("tr")


table_data_header = soupheader.find_all(
    "div", {'class': 'tablesorter-header-inner'})

header = []

for header_data in table_data_header:
    try:
        t = header_data.text.strip()
        header.append(t)
    except:
        continue


data = []

for row in table_data_rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append({header[count]: ele for count, ele in enumerate(cols) if ele})


for val in data:
    print(val)
    print()

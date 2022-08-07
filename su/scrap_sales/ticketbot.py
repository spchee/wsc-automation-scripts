from selenium import webdriver
import pandas
from webdriver_manager.chrome import ChromeDriverManager

import time

browser  = webdriver.Chrome(ChromeDriverManager().install())

browser.get('https://www.warwicksu.com/organisation/tickets/4273/')
input("Please login then press enter to continue...")

#change value of element id ctl00_ctl00_Main_AdminPageContent_drFilter_txtFromDate element to 01/09/2021
start_date = browser.find_element(value='ctl00_ctl00_Main_AdminPageContent_drFilter_txtFromDate')
start_date.clear()
start_date.send_keys('01/09/2021')
print(1)
time.sleep(0.1)

#click button with id ctl00_ctl00_Main_AdminPageContent_btnFilter
browser.find_element(value='ctl00_ctl00_Main_AdminPageContent_btnFilter').click()
time.sleep(0.1)
browser.find_element(value='ctl00_ctl00_Main_AdminPageContent_btnFilter').click()
time.sleep(1)

#find all elements with the msl-row class
rows = browser.find_elements_by_class_name('msl_row')
films = {}
for row in rows:
    
    title = (row.find_elements_by_tag_name('td')[1]).text
    title = title.split(' ')[3:-6]
    title = ' '.join(title)

    price = float(row.find_elements_by_tag_name('td')[3].text)

    
    try:
        sales = int(row.find_elements_by_tag_name('td')[7].text)
    except:
        print(title)
        sales = 0
    gross = price * sales
    films[title] = {}
    films[title]["gross"] = gross

    films[title]["sales"] = sales


rows = browser.find_elements_by_class_name('msl_altrow')
for row in rows:
    
    title = (row.find_elements_by_tag_name('td')[1]).text
    title = title.split(' ')[3:-6]
    title = ' '.join(title)

    price = float(row.find_elements_by_tag_name('td')[3].text)

    
    try:
        sales = int(row.find_elements_by_tag_name('td')[7].text)
    except:
        sales = 0
        print(title)
    gross = price * sales
    try:
        films[title]["gross"] += gross
        films[title]["sales"] += sales
    except:
        print(title)
        print(gross)
        print(sales)
    
#write to csv
df = pandas.DataFrame.from_dict(films, orient='index')
df.to_csv('warwick_sales.csv')

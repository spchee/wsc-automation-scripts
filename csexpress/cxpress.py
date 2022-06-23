from selenium import webdriver
import datetime
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
#browser  = webdriver.Chrome(ChromeDriverManager().install())

#open test_data.csv as dictionary
class film:
    def __init__(self, title : str, date : str, film_type : str, sub : str = ""):
        self.title = title
        self.date = date
        self.film_type = film_type
        self.sub = sub


films = []
with open('test_data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for line in csv_reader:
        films.append(film(line[0], line[1],line[2], line[3]))


browser  = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://csxpress.westworldmedia.com')
input("Please login then press enter to continue")
for film in films:
    main_window = browser.current_window_handle
    browser.get(f'https://csxpress.westworldmedia.com/a2screens.asp?function=NEW&showdate={film.date}&screen_id=1')
    
    for handle in browser.window_handles:
        if handle != main_window:
            browser.switch_to.window(handle)

#enter movie name id="moviename"
    movie_name = browser.find_element_by_id('moviename')
    movie_name.clear()
    movie_name.send_keys('"' + film.title + '"')
    time.sleep(0.1)
    #submit serach id ="submit1"
    try:
        browser.find_element_by_id('submit1').click()
    except:

        #close current window handle
        browser.close()
        time.sleep(0.05)
        browser.switch_to.window(main_window)
        print(f'{film.title} not found')
        time.sleep(0.05)
        continue

    time.sleep(0.05)
    #click first button id = "button1" (multiple with same id)
    browser.find_element_by_id('button1').click()
    time.sleep(0.03)
    browser.switch_to.window(main_window)
    time.sleep(0.03)
    #Enter Attributes id="SCREENS$COMMENT"
    comment = browser.find_element_by_id('SCREENS$COMMENT')
    comment.send_keys(film.film_type + " Presentation")
    time.sleep(0.03)
    #enter subtitle id="SCREENS$CAPTION"
    subtitle = browser.find_element_by_id('SCREENS$CAPTION')
    subtitle.send_keys(film.sub)
    time.sleep(0.03)
    #check if date is a sunday
    day = datetime.datetime.strptime(film.date, '%m/%d/%Y').weekday()
    time1 = ""
    time2 = ""
    if day == 6: #sunday
        time1 = "06:30"
    elif day == 5 or day == 4: #friday or satuday
        time1 = "06:30"
        time2 = "09:30"
    else:
         time1 = "07:30"

    #enter screen time 1 id = "SCREENS$TIME1"
    time1_input = browser.find_element_by_id('SCREENS$TIME1')
    time1_input.send_keys(time1)
    time.sleep(0.05)
    time2_input = browser.find_element_by_id('SCREENS$TIME2')
    time2_input.send_keys(time2)
    time.sleep(0.05)
    #Select checkbox Bargain1 id="SCREENS$BARGAIN1"
    bargain1 = browser.find_element_by_id('SCREENS$BARGAIN1')
    bargain1.click()
    time.sleep(0.05)
    #Select checkbox Bargain2 id="SCREENS$BARGAIN2"
    bargain2 = browser.find_element_by_id('SCREENS$BARGAIN2')
    bargain2.click()

    #click id="save"
    browser.find_element_by_id('save').click()
    time.sleep(0.5)

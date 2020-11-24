from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#specify driver path
DRIVER_PATH = '/Users/cristobalza/Desktop/chromedriver'
browser = webdriver.Chrome(executable_path = DRIVER_PATH)

browser.get('https://cristobalza.com')
print(browser.title)
browser.quit()

# initial_search_button = browser.find_element_by_xpath('//*[@id=”whatWhereFormId”]/div[3]/button')
# initial_search_button.click()
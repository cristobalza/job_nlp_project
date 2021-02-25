from selenium import webdriver
from selenium.webdriver.common.keys import Keys # access to ENTER, ESC,etc. keyboard keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = '/Users/cristobalza/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://techwithtim.net')

link = driver.find_element_by_link_text("Python Programming")
link.click()
# time.sleep(3)
# link.send_keys(Keys.ESCAPE)


try:
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
    )
    element.click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sow-button-19310003"))
    )
    element.click()
except:
    driver.quit()

time.sleep(5)
driver.quit()
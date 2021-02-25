from selenium import webdriver
from selenium.webdriver.common.keys import Keys # access to ENTER, ESC,etc. keyboard keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = '/Users/cristobalza/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://techwithtim.net')


# Always search by id, class, name. In that order of preference.
# If id is not bueno, then try the classm and so on.
# Here I accessed the search bar then search for the keyword 'test'
search = driver.find_element_by_name('s')
search.send_keys('test')
search.send_keys(Keys.RETURN)

# print(driver.page_source)

# Redirect until goinf to the next page. Find all elements withhin id "main"
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    # print(main.text)
    # Loop through the summary of all entries and print them 
    articles = main.find_elements_by_tag_name("article")
    for artcl in articles:
        header = artcl.find_element_by_class_name("entry-summary")
        print(header.text)

finally:
    driver.quit()



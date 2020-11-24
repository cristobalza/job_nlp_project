from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#specify driver path
DRIVER_PATH = '/Users/cristobalza/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

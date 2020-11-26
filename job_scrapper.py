from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
#specify driver path
DRIVER_PATH = '/Users/cristobalza/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

df = pd.DataFrame(columns =
 ['Title',
 'Location',
 'Company',
 'Salary',
 'Sponsored',
 'Description'])




df = pd.DataFrame(columns=["Title","Location","Company","Salary","Sponsored","Description"])

for i in range(0,500,10):
	driver.get("https://www.indeed.com/jobs?q=data+scientist&l=San+Francisco%2C+CA&start="+str(i))
	jobs = []
	driver.implicitly_wait(4)
	

	for job in driver.find_elements_by_class_name('result'):

		soup = BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
		
		try:
			title = soup.find("a",class_="jobtitle").text.replace("\n","").strip()
			
		except:
			title = 'None'

		try:
			location = soup.find(class_="location").text
		except:
			location = 'None'

		try:
			company = soup.find(class_="company").text.replace("\n","").strip()
		except:
			company = 'None'

		try:
			salary = soup.find(class_="salary").text.replace("\n","").strip()
		except:
			salary = 'None'

		try:
			sponsored = soup.find(class_="sponsoredGray").text
			sponsored = "Sponsored"
		except:
			sponsored = "Organic"				

		
		sum_div = job.find_element_by_xpath('./div[3]')
		try:
			sum_div.click()
		except:
			close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
			close_button.click()
			sum_div.click()	


		job_desc = driver.find_element_by_id('jobDescriptionText').text

		df = df.append({'Title':title,'Location':location,"Company":company,"Salary":salary,
						"Sponsored":sponsored,"Description":job_desc},ignore_index=True)

		print("Got these many results:",df.shape)


df.to_csv("ai.csv",index=False)	



# # print(browser.title)

# # search = browser.find_element_by_name("s")
# # search.send_keys("test")
# # search.send_keys(Keys.RETURN)

# # # print(browser.page_source)

# # time.sleep(5)
# # browser.quit()

# # initial_search_button = browser.find_element_by_xpath('//*[@id=”whatWhereFormId”]/div[3]/button')
# # initial_search_button.click()

# login_element = driver.find_element_by_xpath('//span[@class="gnav-LoggedOutAccountLink-text"]')
# #look for the a tag that contains text Log In

# login_element.click()

# email = 'bonnie.majie@gmail.com'
# password = '55686068'

# email_element = driver.find_element_by_xpath('//input[@type="email"]')
# password_element = driver.find_element_by_xpath('//input[@type="password"]')
# log_in_element = driver.find_element_by_xpath('//button[@type="submit"]')

# email_element.send_keys(email)

# password_element.send_keys(password)

# log_in_element.click()

# initial_search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
# initial_search_button.click()

# advanced_search = driver.find_element_by_xpath('//*[@id="jobsearch"]/table/tbody/tr/td[4]/div/a')

# advanced_search.click()

# search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
# search_job.send_keys(['data science'])

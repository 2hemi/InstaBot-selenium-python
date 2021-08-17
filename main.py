import random
import argparse
import config
from bs4 import BeautifulSoup as bs
from selenium import webdriver
# remove the comment if ypu use chrome selenium extantion
#from webdriver_manager.chrome import ChromeDriverManager as CM
from time import sleep
from selenium.common.exceptions import NoSuchElementException



class InstaBot:

	def __init__(self,username,pw):
		
		# remove the comment if ypu use chrome selenium extantion
		
		#self.options = webdriver.ChromeOptions() 
        #self.driver = webdriver.Chrome(executable_path=CM().install(), options=self.options)
        
        
		self.driver = webdriver.Firefox()

		self.driver.get("https://www.instagram.com")

		sleep(random.randint(2,4)+random.random())

		self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
		.send_keys(username)
		
		self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
		.send_keys(pw)
		
		self.driver.find_element_by_xpath('//button[@type="submit"]')\
		.click()
		
		sleep(random.randint(4,6)+random.random())
		
		self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
		.click()
		
		sleep(random.randint(2,4)+random.random())


	def sershHashtag(self,hashtag):

		self.driver.get("https://www.instagram.com/explore/tags/"+hashtag)
		sleep(random.randint(2,4)+random.random())
		string = ''
		l= self.driver.find_elements_by_css_selector("h2")
		for val in l:
			string += val.text
		if string =="Sorry, this page isn't available.":
			return False
		else :
			return True


	def giveLikes(self,amount):

		self.driver.find_element_by_class_name('v1Nh3')\
		.click()

		sleep(random.randint(2,4)+random.random())
		
		like = self.driver.find_element_by_class_name('fr66n')
		soup = bs(like.get_attribute('innerHTML'),'html.parser')
		if(soup.find('svg')['aria-label'] == 'Like'):
			like.click()
			
			
		for i in range(amount):

			sleep(random.randint(2,4)+random.random())
			try :
				like = self.driver.find_element_by_class_name('fr66n')
			
			except NoSuchElementException :
				continue

			soup = bs(like.get_attribute('innerHTML'),'html.parser')
			if(soup.find('svg')['aria-label'] == 'Like'):
				like.click()
				
			sleep(random.randint(2,4)+random.random())

			self.driver.find_element_by_class_name('coreSpriteRightPaginationArrow')\
			.click()

			print('Amount of likes : ' + str(i+1))					
		
				

			

def confirm(question):

	choice = input(question+' [Y/n] ').lower()

	if choice == '' or choice == 'y' or choice == 'yes':
		return True
	elif choice == 'n' or choice == 'no':
		return False
	else:
		print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').")
		return False




#-----------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-a',type=int, required=True,help="Like amount for every hashtag")
parser.add_argument('-l',type=str, required=True, nargs='+',  help="hashtag list")
parser.add_argument('-t',action='store_true',help="skip the confirmation")

args = parser.parse_args()

confirmation = True

if args.t == False:
	
	print('Amount '+str(args.a)+'\nHashtag list '+str(args.l))
	confirmation = confirm('Do you confirm all these information?')

if confirmation == True:
	
	a = InstaBot(config.name,config.pw)

	for i in args.l:
		sleep(random.randint(2,6)+random.random())
		print('Current liking hashtag : '+i)
		if a.sershHashtag(i):
			a.giveLikes(args.a)

	a.driver.quit()




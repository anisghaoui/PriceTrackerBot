from bs4 import BeautifulSoup as bs
import json
import requests
import smtplib
import time


class PriceTrackerBot(object):
	"""
		This class Builds bots that can track items' price on Amazon.com website
	"""
	class AmazonItem(object):
		"""
			This class represent an amazon item by its link and can a threshold as a desired price and name
		"""
		def __init__(self, url : str, desired_price: float = 0):
			self.url = url
			self.desired_price = desired_price


	#################################################
	def __init__(self):
		"""
			build a bot from the "config.json" and add items from "items list.json"
		"""
		try:
			json_data_file = open('config.json')
			config_data = json.load(json_data_file)
			self.fromEmail = config_data["from email"]
			self.toEmail = config_data["to email"]
			self.password = config_data["password"]
			self.headers = config_data["headers"] 
			# by default : 86400 s
			self.check_period = int(config_data["check period"])
			if (self.check_period < 60):
				print("Check period is below 60 s, I can't afford to be blocked by the website")
				quit()
			self._login()
			self.items_list =[]
		except Exception as e:
			print("No config.json file found")
		try:	
			json_data_file = open('items list.json')
			list_data = json.load(json_data_file)
			for item in list_data:
				url = list_data[item]["url"]
				desired_price = float(list_data[item]["desired price"])
				self.add_item(self.AmazonItem(url, desired_price = desired_price))
		except Exception as e:
			print('No "items list.json" file found')

	def _login (self):
		""" logs into the gmail account with the given credential"""
		self.server = smtplib.SMTP('smtp.gmail.com', 587) # for gmail
		self.server.ehlo()
		self.server.starttls()
		self.server.ehlo()
		try:
			self.server.login(self.fromEmail, self.password)
		except :
			print("Login error")
			self.server.quit()

	def send_email(	self, 
					message : str,
					subject : str = "Automatic Amazon price tracker"):
		"""	Sends a message toEmail with a subject """
		msg = 'Subject: {}\n\n{}'.format(subject, message)
		self.server.sendmail(self.fromEmail, self.toEmail, msg)

	def add_item(self,amazon_item : AmazonItem):
		self.items_list.append(amazon_item)

	def check_price_is_low(self, amazon_item : AmazonItem):
		""" seeks a web page from the given URL (Amazon) and checks if the price is below the given threshold, this function needs to be modified accordingly to the webpage's html/js

		returns : false if higher than threshold
		"""
		
		# headers can be obtained from the search engine
		page = requests.get(amazon_item.url, headers = self.headers) 

		# to overcome the js on Amazon.com website
		soup_bis = bs(page.content, "html.parser") 
		soup = bs(soup_bis.prettify(), "html.parser")
		del soup_bis

		amazon_item.name = soup.find(id = 'productTitle').get_text().strip()

		#this part changes depending on Amazon
		parsed_price = soup.find(id = 'price').get_text().strip().split('$')
		parsed_price = parsed_price[1].strip().split(' ')[0] #in $

		amazon_item.price = float(parsed_price)

		if amazon_item.price < amazon_item.desired_price :
			return True
		return False

	def _check_all_prices(self):
		""" check all the prices and send emails about those which are below the desired price"""
		for item in self.items_list:
			if self.check_price_is_low(item):
				self.send_email(
					item.name 
					+ "s's price is below " 
					+ str(item.desired_price)
					+ '$.\nClick on this link to view the item : ' 
					+ item.url,
					)
			time.sleep(5)

	def run(self, tracking_days: int = 0):
		""" 
			Serves as a main loop when given no arguments

			Note: that you will have to kill the process by yourself if you do this
		"""
		if tracking_days < 0:
			raise TypeError("days can't be negative")
		counter = 0
		while True:	
			self._check_all_prices()
			counter += self.check_period
			print(counter,tracking_days)
			if counter > tracking_days*86400 and tracking_days != 0 :
				break
			time.sleep(self.check_period)
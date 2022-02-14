# -*- coding: utf-8 -*-
import shutil

import StandartMethod
import re
import random
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json
class twitter_checker():
	@staticmethod
	def create_file(create_path: str,cook: str, path: str, nick: str, id: str, followers_count: str, friends_count: str, blocking: bool, verified: bool, created_at: bool, allow_ads_personalization: bool, file:str):
		valid_path = StandartMethod.StandartMetod.validate_path_log(path)
		nick = StandartMethod.StandartMetod.validate(nick)
		followers_count = StandartMethod.StandartMetod.validate(followers_count)
		dir_path = create_path + f"\\{nick} - Followers({followers_count}) - Friends({friends_count})"
		try:
			os.mkdir(dir_path)
		except OSError as error:
			pass

		data = {
			'Path': path,
			'Cookie': cook,
			'Account Info': {
				'Nick': nick ,
				'User_id': id,
				'Followers-count': followers_count ,
				'Friends-count': friends_count,
				'Blocking': blocking,
				'Verified': verified,
				'Created_at': created_at,
				'Allow-ads-personalization': allow_ads_personalization
			}
		}
		with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=4, ensure_ascii=False)
		shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

		settings = StandartMethod.headless.get_settings()['Filter_settings']['Twitter']

		try:
			os.mkdir(f'{create_path}\\{settings["Full_log"]}')
		except:
			pass
		try:
			os.mkdir(f'{create_path}\\{settings["Followers_path"]}')
		except:
			pass

		path_premium_log = f'{create_path}\\{settings["Followers_path"]}\\{nick} - Followers({followers_count}) - Friends({friends_count})'
		if int(settings['Filter_followers']) <= int(followers_count):
			try:
				os.mkdir(path_premium_log)
			except:
				pass
			with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
				json.dump(data, outfile, indent=4, ensure_ascii=False)
			shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')


		try:
			os.mkdir(f'{create_path}\\{settings["Verified_path"]}')
		except:
			pass

		path_premium_log = f'{create_path}\\{settings["Verified_path"]}\\{nick} - Followers({followers_count}) - Friends({friends_count})'
		if str(settings['Filter_verified']).lower() == str(verified).lower():
			try:
				os.mkdir(path_premium_log)
			except:
				pass
			with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
				json.dump(data, outfile, indent=4, ensure_ascii=False)
			shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')

	@staticmethod
	def checker(dict, account, path_log, file):
		headers = StandartMethod.StandartMetod.get_headers()
		cook = {
			"auth_token": account['auth_token'],
		}
		req = requests.get('https://twitter.com/home', cookies=cook)
		try:
			nick = re.findall(r"name\":\"(.*?)\"", req.text)[0].strip()
			id = re.findall(r"screen_name\":\"(.*?)\"", req.text)[0].strip()
			followers_count = re.findall(r"followers_count\":(.*?),", req.text)[0].strip()
			friends_count = re.findall(r"friends_count\":(.*?),", req.text)[0].strip()
			blocking = re.findall(r"blocking\":(.*?),", req.text)[0].strip()
			verified = re.findall(r"verified\":(.*?),", req.text)[0].strip()
			created_at = re.findall(r"created_at\":\"(.*?)\"", req.text)[0].strip()
			allow_ads_personalization = re.findall(r"allow_ads_personalization\":(.*?),", req.text)[0].strip()

			twitter_checker.create_file(f'{dict}', account['auth_token'], path_log, nick, id, followers_count, friends_count, blocking, verified, created_at, allow_ads_personalization,file)

		except Exception as ex:
			pass
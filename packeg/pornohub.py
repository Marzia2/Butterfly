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
class pornohub_checker():


	@staticmethod
	def create_file(create_path: str,cook: str, path: str, nick: str, link: str, meta:list, prem: bool, file: str):
		nick = StandartMethod.StandartMetod.validate(nick)
		dir_path = create_path + f"\\{nick} - Premium({str(prem)})"
		try:
			os.mkdir(dir_path)
		except OSError as error:
			pass
		data = {
			'Path': path,
			'Cookie': cook,
			'Account Info': {
				'Nick': nick ,
				'Link': 'https://rt.pornhub.com'+link,
				'Meta': meta,
				'Premium': prem
			}
		}
		with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=4, ensure_ascii=False)
		shutil.copy(f'{file}\\{path}', f'{dir_path}\\{path}')

		settings = StandartMethod.headless.get_settings()['Filter_settings']['PornoHub']

		try:
			os.mkdir(f'{create_path}\\{settings["Full_log"]}')
		except:
			pass
		try:
			os.mkdir(f'{create_path}\\{settings["Premium_path"]}')
		except:
			pass

		path_premium_log = f'{create_path}\\{settings["Premium_path"]}\\{nick} - Premium({str(prem)})'
		if str(settings['Filter_premium']) == str(prem):
			try:
				os.mkdir(path_premium_log)
			except:
				pass
			with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
				json.dump(data, outfile, indent=4, ensure_ascii=False)
			shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{path}')
		shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{path}')
	@staticmethod
	def checker(dict, account, path_log, file):
		headers = StandartMethod.StandartMetod.get_headers()
		cook = {
			"il": account['il'],
		}
		req = requests.get('https://rt.pornhub.com/', cookies=cook, headers=headers)
		try:
			soup = BeautifulSoup(req.text, 'lxml')
			data_link_nick = soup.find('ul', id='profileMenuDropdown').find('li').find('a')
			nick = data_link_nick.text
			link = data_link_nick.get('href')
			req = requests.get(f'https://rt.pornhub.com{link}', cookies=cook, headers=headers)
			soup = BeautifulSoup(req.text, 'lxml')
			data = soup.find('ul', class_='subViewsInfoContainer onlineListItem').find_all('li')
			meta = [i.text.strip().replace(' ', '').replace('\n', ' ') for i in data]
			prem = False
			try:
				premium = soup.find('span', class_='premium-icon flag tooltipTrig').get('data-title')
				prem = True
			except:
				pass
			pornohub_checker.create_file(f'{dict}', account['il'], path_log, nick, link, meta, prem, file)
		except Exception as ex:
			pass

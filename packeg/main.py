# -*- coding: utf-8 -*-
import ctypes
import random

from StandartMethod import *
import threading
logo = '[Butterfly] '
settings = headless.get_settings()
def get_main_info():
    print()
    type_scan = 'TXT'
    path_log = f'{settings["File_scan"]}\\File.txt'
    if settings['type_data'] == 'log':
        type_scan = 'Лог'
        path_log = f'{settings["File_scan"]}\\File.txt\\{settings["Name_file_log"]}'
    print(f"[Settings] Путь к логам: {path_log} | Тип данных: {type_scan} | Количество потоков: {settings['Flow_count']}")
    allow_services = dict(settings['Services'])
    services_dict = {}
    for key,value in allow_services.items():
        if value:
            services_dict[key] = True
        else:
            services_dict[key] = False
    print(f"[Services] Crex24: {services_dict['Crex24']} | FreeBitco: {services_dict['FreeBitco']} | HumbleBundle: {services_dict['HumbleBundle']} | Instagram: {services_dict['Instagram']}"
               f"Kryptex: {services_dict['Kryptex']} | Mail: {services_dict['Mail']}\n"
               f"[Services] PornoHub: {services_dict['PornoHub']} | Roblox: {services_dict['Roblox']} | Steam: {services_dict['Steam']} | Twitter: {services_dict['Twitter']} | Vk: {services_dict['Vk']}"
               f"TikTok: {services_dict['TikTok']}")
def thr_count():
    count_log = len(start_work.full_logi) - 1
    status = 'Мы только начали'
    random_status = ['Пожалуйста подождите минутку', 'Лох не мамонт не вымрет', 'Мы скоро закончим', 'Наберитесь терпения',
                     'Ещу чуть-чуть', 'Анализируем скрытые базы данных', 'Взламываем роблокс']
    counter = 0
    while True:
        count_checker_log = start_work.count_checked_log
        if counter >= 3:
            status = random.choice(random_status)
            counter = 0
        ctypes.windll.kernel32.SetConsoleTitleW(f"Butterfly v0.1 | thr: {threading.active_count() - 2} | {count_checker_log}/{count_log} | {status}")
        time.sleep(3)
        counter += 1
        if (count_checker_log >= count_log): break
    ctypes.windll.kernel32.SetConsoleTitleW(f"Butterfly v0.1 | thr: {threading.active_count() - 2} | {count_checker_log}/{count_log} | Мы закончили")
if __name__ == "__main__":
    print(logo + f'key: {headless.get_hwid_hash()}')
    User = connetcion_database(headless.get_hwid(), headless.get_hwid_hash())
    user_succes = User.check_activity()
    if user_succes[0]:
        print(logo + f'Лицензия активна до: {str(user_succes[1])}')
        get_main_info()
        thread_count = threading.Thread(target=thr_count)
        thread_count.start()
        count_streams = settings['Flow_count']
        print("\n"+logo+"Начинаем через пару секунд")
        time.sleep(3)
        for flow in range(count_streams):
            stream = threading.Thread(target=start_work.start, name=f'thr-{flow}')
            stream.start()
        while threading.active_count() > 2:
            time.sleep(5)
        print(logo+'\n>> Проверка завершена <<')
        time.sleep(100000)
    else:
        print(logo + 'Срок вашей лицензии истек')
        time.sleep(100000)
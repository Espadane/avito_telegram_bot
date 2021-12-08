import random
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def get_data_from_html(url):
    """Получение кода html по url"""
    with open('proxies') as file:
        proxy_base = ''.join(file.readlines()).strip().split('\n')
        proxy_adr = random.choice(proxy_base)
        proxy = {'https' : f'https://{proxy_adr}',
                'http' : f'http://f{proxy_adr}'}
    header = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control':'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    try:
        print('Пробуем подключиться через прокси')
        r = requests.get(url=url, headers=header,proxies=proxy, timeout=25)
        check_ip(header, proxy)
    except:
        print(Fore.YELLOW + 'Не удалось подключиться к прокси, пробуем подключиться без прокси')
        r = requests.get(url=url, headers=header, timeout=2)
        check_ip(header)
        print(r.status_code)
        if r.status_code == 429:

            return '429'
        else:
            soup = BeautifulSoup(r.text, 'lxml')
            ads = soup.find_all('div', class_='iva-item-root-Nj_hb')
            page_title = soup.title.text
            
            return ads, page_title

def check_ip(header, proxy=None):
    '''Проверка ip через который идет подключение'''
    ip_cheker_url = 'https://2ip.ru/'
    r_ip = requests.get(url=ip_cheker_url, headers=header,proxies=proxy,timeout=2)
    soup = BeautifulSoup(r_ip.text, 'lxml')
    ip = soup.find('div', class_='ip').find('span').text
    print('')
    print(Fore.GREEN + "Соединение успешно установлено, ваш IP-адрес : " + ip)
    print(Style.RESET_ALL)


def get_ad_data(url):
    """Получение данных последнего объявления"""
    ads, page_title = get_data_from_html(url)
    if ads == '429':
        return ads
    else:
        for ad in ads:
            ad_url = 'https://avito.ru'+str(ad.find('div', class_='iva-item-titleStep-_CxvN').find('a')).split('"')[5]
            ad_title = page_title
            ad_price = ad.find('span', class_='price-text-E1Y7h').text.strip()
            ad_content = str(ad.find('meta')).split('"')[1]
            ad_location = ad.find('div', class_ = 'geo-root-H3eWU').find('span').text.strip()

            ad_data = [ad_title, ad_price, ad_content, ad_location, ad_url]

            return ad_data
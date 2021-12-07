import random
import requests
from os import getenv
from sys import exit
from bs4 import BeautifulSoup


proxy_login = getenv("PROXY_LOGIN")
if not proxy_login:
    exit("Error: no proxy_login provided")

proxy_pass = getenv("PROXY_PASS")
if not proxy_login:
    exit("Error: no proxy_pass provided")

def get_data_from_html(url):
    """Получение кода html по url"""
    try:
        with open('proxies') as file:
            proxy_base = ''.join(file.readlines()).strip().split('\n')
            proxy_adr = random.choice(proxy_base)
            proxy = {'https' : f'https://{proxy_login}:{proxy_pass}@{proxy_adr}',
                    'http' : f'http://{proxy_login}:{proxy_pass}@{proxy_adr}'}
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
            r = requests.get(url=url, headers=header,proxies=proxy)
        except Exception as ex:
            print(ex)
        print(r.status_code)
        if r.status_code == 429:
            
            return '429'
        else:
            soup = BeautifulSoup(r.text, 'lxml')
            ads = soup.find_all('div', class_='iva-item-root-Nj_hb')
            return ads
    except:
        print(Exception)

def get_ad_data(url):
    """Получение данных последнего объявления"""
    ads = get_data_from_html(url)
    if ads == '429':
        return ads
    else:
        try:
            for ad in ads:
                ad_url = 'https://avito.ru'+str(ad.find('div', class_='iva-item-titleStep-_CxvN').find('a')).split('"')[5]
                ad_title = ad.find('h3').text.strip()
                ad_price = ad.find('span', class_='price-text-E1Y7h').text.strip()
                ad_content = str(ad.find('meta')).split('"')[1]
                ad_location = ad.find('div', class_ = 'geo-root-H3eWU').find('span').text.strip()

                ad_data = [ad_title, ad_price, ad_content, ad_location, ad_url]

                return ad_data
        except:
                print(Exception)

def get_requested_page_title(url):
    """Получение Title поискового запроса"""
    try:
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        page_title = soup.title.text
        page_title = page_title.split('|')[0]

        return page_title
    except:
        print(Exception)
import requests
from bs4 import BeautifulSoup
import fake_useragent

def get_data_from_html(url):
    """Получение кода html по url"""
    try:
        ua = fake_useragent.UserAgent()
        user = ua.random
        header = {'User-Agent': str(user)}
        r = requests.get(url=url, headers=header)
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
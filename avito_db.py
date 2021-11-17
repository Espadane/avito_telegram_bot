import sqlite3


conn = sqlite3.connect('avito_ads.db')

def create_table_ad(conn):
    """Созадние базы данных если она еще не существует"""
    cursor = conn.cursor()
    cursor.execute('create table if not exists avito_tracked_ads(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, tracked_url text NOT NULL,last_ad_url text NOT NULL, tracked_url_title text NOT NULL)')
    conn.commit()

def get_data_from_db(user_id, tracked_url):
    """Получение данных об отслеживаемых объявлениях из базы данных, по user_id"""
    cursor = conn.cursor()
    sql = 'SELECT user_id, tracked_url, last_ad_url FROM avito_tracked_ads WHERE user_id = ? and tracked_url = ?'
    query = (user_id, tracked_url)
    data = cursor.execute(sql, query)
    for element in data:
        return element
    conn.commit()

def check_data(user_id, tracked_url, last_ad_url):
    """Проверка наличия отслеживаемых объявлений в базе данных"""
    new_ad = (user_id, tracked_url, last_ad_url)
    last_ad_url = get_data_from_db(user_id, tracked_url)
    if last_ad_url == None:
        return 'no data'
    elif new_ad == last_ad_url:
        return 'delete data'

def write_url_on_db(data):
    """Запись запрос об объявлениях в базу данных"""
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO avito_tracked_ads (user_id, tracked_url, last_ad_url,tracked_url_title) VALUES (?, ?, ?, ?)', data)
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка", error)

def delete_old_data(user_id, tracked_url):
    """Удаление запроса из базы данных """
    cursor = conn.cursor()
    try:
        sql = 'DELETE FROM avito_tracked_ads WHERE user_id = ? and tracked_url = ?'
        cursor.execute(sql, [user_id, tracked_url])
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка", error)

def get_all_users_ads(user_id):
    '''Получение всех объявлений пользователя'''
    ads_list = []
    cursor = conn.cursor()
    sql = 'SELECT tracked_url,tracked_url_title FROM avito_tracked_ads where user_id = ?'
    data = cursor.execute(sql, (user_id,))
    for d in data:
        ads_list.append(d)

    return ads_list

def get_old_ad_from_db(user_id, tracked_url):
    """Удаление отслеживаемого запроса пользователя из базы данных"""
    cursor = conn.cursor()
    sql = 'SELECT last_ad_url from avito_tracked_ads WHERE user_id = ? and tracked_url = ?'
    query = (user_id, tracked_url)
    old_ad = cursor.execute(sql, query)
    for element in old_ad:

        return str(element)



create_table_ad(conn)
import sqlite3
import json

def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_list (
            name,
            number
            ) """)
    db.commit()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_ref
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
                chanel,
                name,
                link,
                person
                ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel1', '@tvoe_tb', 'https://t.me/tvoe_tb', 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel2', '@filmy_to', 'https://t.me/filmy_to', 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel3', '@novoetg', 'https://t.me/novoetg', 100))
        db.commit()



    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()

        # Создание таблицы для постинга
    sql.execute(""" CREATE TABLE IF NOT EXISTS posting_list (
            number_day,
            status_post,
            message_id,
            keyboard
            ) """)
    db.commit()
    sql.execute(f"SELECT number_day FROM posting_list WHERE number_day ='1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('1', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('2', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('3', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('4', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('5', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('6', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('7', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('8', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('9', '0', '0', 'null'))
        sql.execute(f"INSERT INTO posting_list VALUES (?,?,?,?)", ('10', '0', '0', 'null'))
        db.commit()
    # Таблица для постинга


# Cоздание отслеживания подписчиков
    sql.execute(""" CREATE TABLE IF NOT EXISTS stata_parthers ( 
            id BIGINT,
            channel_ref
            ) """)
    db.commit()

    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (0,0))
        db.commit()

# ИНФО О ПАРТНЕРАХ ЧТО БЫ ПРИКРУТИТЬ ИМ СЧЕТЧИК
    sql.execute(""" CREATE TABLE IF NOT EXISTS parthers( 
                id_partn,
                name_channel,
                schet
                ) """)
    db.commit()

    # СЧЕТЧИК ТРАФИКА ОТ КОНКРЕТНОГО ПАРТНЕРА
    sql.execute(""" CREATE TABLE IF NOT EXISTS list_support( 
                    id,
                    name_channel,
                    status
                    ) """)
    db.commit()

    # СОЗДАНИЕ РАЗРЕШЕННЫХ support
    sql.execute(""" CREATE TABLE IF NOT EXISTS utm_support (
                           name,
                           info,
                           info_pay,
                           status
                           ) """)

    # АРХИВ ВЫПЛАТ
    sql.execute(""" CREATE TABLE IF NOT EXISTS listpay( 
                        data,
                        schetchik
                        ) """)
    db.commit()

def obnova_posting_message_id(day,m_id,keyboard):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    k = str(json.dumps(keyboard))
    sql.execute("UPDATE posting_list SET keyboard=? WHERE number_day=?", (k,day))

    sql.execute(f"UPDATE posting_list SET message_id = '{m_id}' WHERE number_day = '{day}'")
    db.commit()

def obnova_status_postinga(day):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    c = int((sql.execute(f"SELECT status_post FROM posting_list WHERE number_day = '{day}'").fetchall())[0][0])
    if c ==1:
        c = 0
    else:
        c = 1

    sql.execute(f"UPDATE posting_list SET status_post = '{c}' WHERE number_day = '{day}'")
    db.commit()

def cheack_mes_id_postinga(day):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    m = int((sql.execute(f"SELECT message_id FROM posting_list WHERE number_day = '{day}'").fetchall())[0][0])
    return m

def cheack_keyboard_postinga(day):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    k = (sql.execute(f"SELECT keyboard FROM posting_list WHERE number_day = '{day}'").fetchall())[0][0]
    if k != 'null':
        new_k = json.loads(k)
        return new_k
    else:
        return 1

def cheack_status_postinga(day):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    s = int((sql.execute(f"SELECT status_post FROM posting_list WHERE number_day = '{day}'").fetchall())[0][0])
    return s

def regviplata(data): # Регистрация выплатны
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sum = 0
    y = sql.execute(f"SELECT * FROM parthers").fetchall()
    for i in y:
        a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{i[1]}'").fetchone()[0]
        sum+=int(a)

    sql.execute(f"INSERT INTO listpay VALUES (?,?)", (data,sum)) # РЕГИСТРИРУЕМ ДАТУ И КОЛИЧЕСТВО ОПЛАЧЕННОГО ТРАФИКА
    db.commit()

def cheak_viplats():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    y = sql.execute(f"SELECT * FROM listpay").fetchall()
    return y


def reg_utm_support(utm, info, pay_info): # Регистрация РАЗРЕШЕННЫХ support
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT name FROM utm_support WHERE name = '{utm}'")
    if sql.fetchone() is None: #Проверка на наличие канала
        #print('Канал не найден! (То что нам нужно)')
        sql.execute(f"SELECT info FROM utm_support WHERE info = '{info}'")
        if sql.fetchone() is None : #Если чела еще нету с таким id, то  регаем
            #print('Сработала операция (Человек не найден), регистрируем')
            sql.execute(f"INSERT INTO utm_support VALUES (?,?,?,?)", (utm, info, pay_info, '1'))
            db.commit()
        else:
            pass #print('Сработала операция (Человек найден, не регистрируем)')


    else: #Канал найден
        #print('Канал найден! (То что нам не нужно)')
        try:
            int(info)
            sql.execute(f"SELECT info FROM utm_support WHERE name ='{utm}'")
            try:
                int((sql.fetchone())[0][0])
            except:  # У человека Id не в интеджер
                sql.execute(f"UPDATE utm_support SET info = '{info}' WHERE name = '{utm}'")
                sql.execute(f"UPDATE utm_support SET info_pay = '{pay_info}' WHERE name = '{utm}'")
                db.commit()

        except:
            pass
    db.commit()

# РЕГИСТРАЦИЯ ЧЕЛОВЕКА ОТ САППОРТА
def reg_traf_support(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM list_support WHERE id ={id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO list_support VALUES (?,?,?)", (id, f'@{channel}', 0))
        db.commit()


#УДАЛЕНИЕ САППОРТА
def changee_support_tochka(channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE utm_support SET status = 0 WHERE name = '{channel}'")
    db.commit()

def cheak_support(): # Возваращет ютм метку - Количество чел - Инфо об админе
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c = sql.execute(f"SELECT * FROM utm_support").fetchall()
    ansver = []
    for i in c: #ГЕНЕРИРУЕМ ОТВЕТ ИЗ РУЧНОЙ РЕГИСТРАЦИИ
        if i[3] == '1':
            a = sql.execute(f"SELECT COUNT(*) FROM list_support WHERE name_channel ='{i[0]}' ").fetchone()[0]  # Количество всех пользователей
            b1 = sql.execute(f"SELECT COUNT(*) FROM list_support WHERE name_channel ='{i[0]}' and status = 0").fetchone()[0]  # Количество неоплаченных пользователей
            ansver.append([i[0],i[1],a,b1,i[2]])

    return ansver

# СОЗДАНИЕ ВЫПЛАТЫ = ИЗМЕНЕНИЕ СТАТУСА
def changee_support():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE list_support SET status = 1")
    db.commit()

## НОВОЕ
def cheach_channel_par(id): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers WHERE id_partn ={id}").fetchall()
    return r

def cheach_all_par(): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers").fetchall()
    return r

def info(channel): #Возвращает количество подписок на канал
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{channel}'").fetchone()[0]
    return a


def reg_partners_schet(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id_partn FROM parthers WHERE name_channel ='{channel}' and id_partn ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO parthers VALUES (?,?,?)", (id, channel, 0))
        db.commit()

## КОНЕЦ НОВОГО


###### Количество подписок на каналы партнеров
def reg_pod(id,channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{id}' and channel_ref ='{channel}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (id, channel))
        db.commit()


#Просмотр трафика
def info_chyornaya_vdova(): # Трафик Дена
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'chyornaya_vdova'").fetchone()[0]
    return a

def info_good_film1(): # Трафик Алексея
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'good_film1'").fetchone()[0]
    return a

def info_films_online_everyday(): # Трафик ЮЛИ
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'films_online_everyday'").fetchone()[0]
    return a


def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (name, 1))
        db.commit()
    db.commit()

def reg_channels(text): #Регистрация списка каналов
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    text = text.split()
    for i in text:
        i = i[1:]
        sql.execute(f"SELECT name FROM channel_list WHERE name ='{i}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (i, 1))
            db.commit()
        db.commit()

def proverka_channel(channel_name):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT name FROM channel_list WHERE name ='{channel_name}'").fetchone()
    if a is None:
        return 0
    else:
        return 1

def del_one_channel(name): #Удаление одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        pass
    else:
        sql.execute(f'DELETE FROM channel_list WHERE name ="{name}"')
        db.commit()


def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    c1_name = sql.execute(f"SELECT name FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c1_link = sql.execute(f"SELECT link FROM trafik WHERE chanel = 'channel1'").fetchone()[0]

    c2_name = sql.execute(f"SELECT name FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c2_link = sql.execute(f"SELECT link FROM trafik WHERE chanel = 'channel2'").fetchone()[0]

    c3_name = sql.execute(f"SELECT name FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    c3_link = sql.execute(f"SELECT link FROM trafik WHERE chanel = 'channel3'").fetchone()[0]

    list = [[c1_name, c1_link], [c2_name, c2_link], [c3_name, c3_link]]
    return list


def obnovatrafika(channel1,channel2,channel3):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    channel1_name = channel1[0]
    channel1_link = channel1[1]

    channel2_name = channel2[0]
    channel2_link = channel2[1]

    channel3_name = channel3[0]
    channel3_link = channel3[1]

    sql.execute(f"UPDATE trafik SET name= '{channel1_name}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET link= '{channel1_link}' WHERE chanel = 'channel1'")

    sql.execute(f"UPDATE trafik SET name= '{channel2_name}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET link= '{channel2_link}' WHERE chanel = 'channel2'")

    sql.execute(f"UPDATE trafik SET name= '{channel3_name}' WHERE chanel = 'channel3'")
    sql.execute(f"UPDATE trafik SET link= '{channel3_link}' WHERE chanel = 'channel3'")


    db.commit()
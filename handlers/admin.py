from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, reg_one_channel, reg_channels,del_one_channel,cheak_traf,obnovatrafika,info_chyornaya_vdova,info_good_film1,info_films_online_everyday,reg_partners_schet,cheach_all_par,info,reg_utm_support,cheak_support,changee_support,regviplata,cheak_viplats,changee_support_tochka
from .callbak_data import obnovlenie
import asyncio
from datetime import timedelta,datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон
ADMIN_ID_5 = 2116984782 #Пабло

MODERN_ID_5 = 807911349 #Байзат


PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
#ФАИН PARTNERS3 = 519072406
PARTNERS4 = 921818240 #Юля
PARTNERS5 = 1013231983 # АЛЕКС

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2, ADMIN_ID_4,ADMIN_ID_3,MODERN_ID_5,ADMIN_ID_5]

class reg(StatesGroup):
    name = State()
    fname = State()

class reg_support(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()

class del_support(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()


class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class partners12(StatesGroup):
    step1 = State()
    step2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_vie_support = types.InlineKeyboardButton(text='👁Просмотр саппортов', callback_data='bat_vie_support')
        bat_reg_support = types.InlineKeyboardButton(text='🆕Регистрация саппорта', callback_data='bat_reg_support')
        bat_pye_support = types.InlineKeyboardButton(text='💰Выплатить саппортам', callback_data='bat_pye_support')
        bat_history_pye = types.InlineKeyboardButton(text='⏱История выплат', callback_data='bat_history_pye')


        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='NEW канал', callback_data='new_channel')# Добавляет 1 канал
        bat_c = types.InlineKeyboardButton(text='NEW Список', callback_data='new_channels') # Добавляет список каналов через пробел
        bat_d = types.InlineKeyboardButton(text='Удалить канал', callback_data='delite_channel')# Удаляет канал из списка
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_setin = types.InlineKeyboardButton(text='Настройка трафика', callback_data='settings')
        den_but = types.InlineKeyboardButton(text='Ден', callback_data='chyornaya_vdova')
        alex_but = types.InlineKeyboardButton(text='Алекс', callback_data='good_film1')
        yulya_but = types.InlineKeyboardButton(text='Юля', callback_data='films_online_everyday')
        sbros_but = types.InlineKeyboardButton(text='Сбросить статистику', callback_data='sbros')
        reg_new_partners = types.InlineKeyboardButton(text='РЕГИСТРАЦИЯ НОВОГО ПАРТНЕРА',callback_data='reg_new_partners')
        vienw_partners = types.InlineKeyboardButton(text='СТАТИСТИКА ВСЕХ ПАРТНЕРОВ', callback_data='vienw_partners')

        markup.add(bat_vie_support)
        markup.add(bat_reg_support)
        markup.add(bat_pye_support)
        markup.add(bat_history_pye)

        markup.add(bat_a, bat_b, bat_c, bat_d,bat_e,bat_j)
        markup.add(den_but, alex_but, yulya_but)  # Инфо о партнерах
        markup.add(bat_setin)
        markup.add(reg_new_partners)
        markup.add(vienw_partners)

        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)

    if id == MODERN_ID_5: #Админка для модераторов
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        markup.add(bat_a)
        await bot.send_message(message.chat.id, 'Выполнен вход в админ панель', reply_markup=markup)

@dp.callback_query_handler(text='bat_vie_support')  #Просмотр всей статистики Support
async def bat_vie_support(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        answer = cheak_support()
        await bot.send_message(chat_id=call.message.chat.id, text='⭐️Статистика по саппортам👇',parse_mode='html')

        for i in answer:
            markup = types.InlineKeyboardMarkup()
            try:
                bat_a = types.InlineKeyboardButton(text='Изменить реквезиты', callback_data=f'change_payinfo{i[0]}')
                markup.add(bat_a)
                bat_b = types.InlineKeyboardButton(text='Удалить этого чела', callback_data=f'toch_obnal_{i[0]}') #УДАЛЕНИЕ ЧЕЛА
                markup.add(bat_b)
            except:
                pass

            try:
                int(i[1])
                await bot.send_message(chat_id=call.message.chat.id, text=f'<b>Канал:</b> {i[0]}\n'
                                                                          f'<b>Админ:</b> tg://user?id={i[1]}\n'
                                                                          f'<b>Неоплаченный трафик:</b> {i[3]}\n'
                                                                          f'<b>Трафика всего:</b> {i[2]}\n'
                                                                          f'<b>Реквезиты партнера:</b> {i[4]}',
                                       parse_mode='html', reply_markup=markup)
            except:
                await bot.send_message(chat_id=call.message.chat.id, text=f'<b>Канал:</b> {i[0]}\n'
                                                                          f'<b>Админ:</b> {i[1]}\n'
                                                                          f'<b>Неоплаченный трафик:</b> {i[3]}\n'
                                                                          f'<b>Трафика всего:</b> {i[2]}\n'
                                                                          f'<b>Реквезиты партнера:</b> {i[4]}',parse_mode='html',reply_markup=markup)
            await asyncio.sleep(0.3)


@dp.callback_query_handler(text_startswith='toch_obnal_')  #УДАЛЯЕМ САППОРТА
async def fdsfdsfsdfds(call: types.callback_query,state: FSMContext):
    channel = (call.data[11:])
    await call.message.answer(text= f'Для удаления {channel} введите пароль')
    await del_support.step1.set()
    await state.update_data(channel = channel)

    # try:
    #     channel = (call.data[11:])
    #     changee_support_tochka(channel)  # Удаляем чела с каналом channel
    #     await call.message.answer(text=f'Удаление канала {channel} Успешно')
    # except:
    #     await call.message.answer(text='Удаление почему-то не удалось')


@dp.message_handler(state=del_support.step1, content_types='text')
async def delite12_support(message: types.Message, state: FSMContext):
    if int(message.text) == 1111:
        try:
            channel = (await state.get_data())['channel']
            changee_support_tochka(channel)  # Удаляем чела с каналом channel
            await message.answer(text=f'Удаление канала {channel} Успешно')
        except:
            await message.answer(text='Удаление почему-то не удалось')
        await state.finish()
    else:
        await message.answer(text='Отменено. Пароль неверный')
        await state.finish()






@dp.callback_query_handler(text='bat_reg_support')  #Регистрация Support
async def bat_reg_support(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(chat_id=call.message.chat.id,text='Введите основной канал Саппорта в формате @name_channel')
        await reg_support.step1.set()

@dp.message_handler(state=reg_support.step1, content_types='text')
async def get_reg_support(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        try:
            await state.update_data(channel = message.text)
            await bot.send_message(chat_id=message.chat.id,text= 'Введите информацию об админе (Юзер - Имя)')
            await reg_support.step2.set() # СОСТОЯНИЕ ИНФОРМАЦИИ ОБ АДМИНЕ
        except:
            await bot.send_message(chat_id=message.chat.id,text='Неудача')
            await state.finish()

@dp.message_handler(state=reg_support.step2, content_types='text')
async def get_reg_support2(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        try:
            await state.update_data(user_name = message.text)
            await bot.send_message(chat_id=message.chat.id,text='Отлично! Теперь можете ввести реквезиты партнера, и название его платежной системы')
            await reg_support.step3.set()
        except:
            await bot.send_message(chat_id=message.chat.id, text='Неудача')
            await state.finish()

@dp.message_handler(state=reg_support.step3, content_types='text')
async def get_reg_support33(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        number_support = message.text # Реквезиты саппорта

        info_about_parthers = await state.get_data()
        channel_support = info_about_parthers['channel'] #Канал
        username_support = info_about_parthers['user_name'] #Юзернейм саппортов

        try:
            reg_utm_support(utm = channel_support ,info = username_support, pay_info = number_support)  #Регистрация партнера
            reg_one_channel(channel_support)
            await bot.send_message(message.chat.id,text='Успешно')
        except:
            await bot.send_message(message.chat.id, text='Неудача!')

        await state.finish()


#ВЫПЛАТА САППОРТАМ
@dp.callback_query_handler(text='bat_pye_support')  #Выплата пратнерам
async def bat_pye_support(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        but_pye_yes = types.InlineKeyboardButton(text='✅ДА', callback_data='but_pye_yes')
        but_pye_no = types.InlineKeyboardButton(text='❌НЕТ', callback_data='but_pye_no')

        markup.add(but_pye_yes,but_pye_no)

        await bot.send_message(chat_id=call.message.chat.id,text='<b>Вы действительно хотите анулировать у всех саппортов счетчик неоплаченного трафика?</b>',reply_markup=markup,parse_mode='html')


@dp.callback_query_handler(text='but_pye_no')  #ОТМЕНА Выплаты пратнерам
async def bat_pye_no_support(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)


@dp.callback_query_handler(text='but_pye_yes')  #Подтверждение выплаты пратнерам
async def bat_pye_yes_support(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        data = (call.message.date)
        data_v = (data + timedelta(hours=2))  # Оренбуржское время выплаты
        regviplata(data_v)
        try:
            changee_support()
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(call.message.chat.id,text='Успешно')
        except:
            await bot.send_message(call.message.chat.id, text='Неудача')

@dp.callback_query_handler(text='bat_history_pye')  #ПРОСМОТР ВЫПЛАТ
async def bat_history_pye(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = cheak_viplats()
        await bot.send_message(chat_id=call.message.chat.id, text='Последнии 5 выплат партнерам')
        for i in range(-1,-6,-1):
            dannie = (a[i])
            await bot.send_message(chat_id=call.message.chat.id,text=f'Дата:{dannie[0]}\n'
                                                                 f'Проплачено по счетчикам до: {dannie[1]}')

#ПРОСМОТР ВСЕХ ПАРТНЕРОВ
@dp.callback_query_handler(text='vienw_partners')  #ПРОСМОТР ВСЕХ ПАРТНЕРОВ
async def vienw_partners(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        q = cheach_all_par()
        sim = 0
        if q != []:  # Если зарегистрирован в базе для просмотра
            for i in q:
                s = (info(i[0]))
                sim+= int(s)
                await bot.send_message(call.message.chat.id, f'Счетчик @{i[0]}: {s}')
        await bot.send_message(call.message.chat.id, f'Сумма всех счетчиков: {sim}')


#МЕНЮ НОВЫХ ПАРТНЕРОВ
@dp.callback_query_handler(text='reg_new_partners')  #МЕНЮ
async def check_all_partners(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        markup.add(bat_a)

        await bot.send_message(chat_id=call.message.chat.id,text = 'Перешлите сообщение от партнера',reply_markup=markup)
        await partners12.step1.set()


@dp.message_handler(state=partners12.step1, content_types='text')
async def get_id_partners(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        try:
            id = message.forward_from.id
            await state.update_data(id_partners = id)
            await bot.send_message(chat_id=message.chat.id, text='ID получен! \n'
                                                                 'Введите имя канала слитно без пробелов, через @')
            await partners12.step2.set()

        except:
            await bot.send_message(chat_id=message.chat.id, text='У партнера скрытый аккаунт!\n'
                                                             'Повторите попытку')


@dp.message_handler(state=partners12.step2, content_types='text')
async def get_channel_partners(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        chennel = message.text
        if chennel[0] == '@':
            await bot.send_message(chat_id=message.chat.id, text='Канал зарегистрирован')
            text_id = (await state.get_data())['id_partners']
            reg_partners_schet(channel=chennel[1:],id = text_id)
            await state.finish()

        else:
            await bot.send_message(chat_id=message.chat.id, text='Повторите попытку')


@dp.message_handler(commands=['traf'])
async def cheak_traaf(message: types.Message):
    if message.chat.id in ADMIN_ID:
        if message.chat.id == PARTNERS1 or message.chat.id == PARTNERS2: #ДЕНИС
            a = info_chyornaya_vdova()  # Вызов функции из файла sqlit
            await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                         f'Канал : @chyornaya_vdova')

        if message.chat.id == PARTNERS5: #АЛЕКС
            a = info_good_film1()  # Вызов функции из файла sqlit
            await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                         f'Канал : @good_film1')

        if message.chat.id == PARTNERS4: #ЮЛЯ
            a = info_films_online_everyday()  # Вызов функции из файла sqlit
            await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                         f'Канал : @films_online_everyday')

# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        markup_traf = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ КАНАЛЫ⚙️', callback_data='change_trafik')
        markup_traf.add(bat_a)
        list = cheak_traf()
        await bot.send_message(call.message.chat.id, text=f'Список активный каналов на данный момент:\n\n'
                                                          f'1. {list[0][0]} - {list[0][1]}\n\n'
                                                          f'2. {list[1][0]} - {list[1][1]}\n\n'
                                                          f'3. {list[2][0]} - {list[2][1]}\n\n\n'
                                                          f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                          f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf,disable_web_page_preview=True)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        markup.add(bat_a)

        await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                          'Список каналов вводи по примеру:\n\n'
                                                          '@channel1 - https://t.me/joinchat/gQuo4v3mmUllNTJi\n'
                                                          '@channel2 - https://t.me/joinchat/gQuo4v3mmUllNTJi\n'
                                                          '@channel3 - https://t.me/joinchat/gQuo4v3mmUllNTJi\n\n'
                                                          '<pre>Сначала вводи имя которое будет отобращаться в боте, через тире саму ссылку!</pre>',parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        try:
            mas = message.text.split('\n') # Массив с данными о каждом канале

            info_1 = (mas[0]).split('-') #Инфо о первом канале
            info_2 = (mas[1]).split('-') #Инфо о втором канале
            info_3 = (mas[2]).split('-') #Инфо о третьем канале

            channe1_name = info_1[0][:-1]
            channel1_link = info_1[1][1:]

            channe2_name = info_2[0][:-1]
            channel2_link = info_2[1][1:]

            channe3_name = info_3[0][:-1]
            channel3_link = info_3[1][1:]


            obnovatrafika([channe1_name,channel1_link],[channe2_name,channel2_link],[channe3_name,channel3_link]) # Внесение новых каналов в базу данных
            obnovlenie()
            await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
            await state.finish()

        except:
            await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                                'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
            await state.finish()


@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = open('server.db','rb')
        await bot.send_document(chat_id=call.message.chat.id, document=a)


############################  DELITE CHANNEL  ###################################
@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                     '@name_channel')
        await del_user.del_name.set()



@dp.message_handler(state=del_user.del_name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        check_dog = message.text[:1]
        if check_dog != '@':
            await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
        else:
            await state.finish()
            del_one_channel(message.text)
            await bot.send_message(message.chat.id, 'Удаление завершено')


############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                     '@name_channel')
        await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        check_dog = message.text[:1]
        if check_dog != '@':
            await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
        else:
            reg_one_channel(message.text)
            await bot.send_message(message.chat.id, 'Регистрация успешна')
            await state.finish()


################################    REG MANY CHANNELS    ###########################
@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                     '@name1 @name2 @name3 ')
        await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
        reg_channels(message.text)
        await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = info_members() # Вызов функции из файла sqlit
        await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')



########################  Рассылка  ################################
@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note','voice']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr3 = message.text.split('\n')
    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    massiv_text = []
    massiv_url = []

    for but in arr3:
        new_but = but.split('-')
        massiv_text.append(new_but[0][:-1])
        massiv_url.append(new_but[1][1:])
        bat9 = types.InlineKeyboardButton(text=new_but[0][:-1],url=new_but[1][1:])
        murkap.add(bat9)



    try:
        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but = massiv_text ) # Обновление Сета
        await state.update_data(url_but = massiv_url)  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками
    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_massiv = data['text_but']
        url_massiv = data['url_but']
        for t in text_massiv:
            for u in url_massiv:
                bat = types.InlineKeyboardButton(text=t, url=u)
                murkap.add(bat)
                break

    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(0.03)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################
from aiogram import types
from misc import dp, bot
import sqlite3
import asyncio
from datetime import timedelta,datetime
from .admin import ADMIN_ID
from .sqlit import obnova_posting_message_id, obnova_status_postinga,cheack_status_postinga,cheack_keyboard_postinga

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

channel_posts = -1001525589284

class number_day(StatesGroup):
    number = State()
    another_value = State()


@dp.message_handler(commands=['posting'])
async def Posting(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat1 = types.InlineKeyboardButton(text='День 1 (24 часа)', callback_data='day1')
        bat2 = types.InlineKeyboardButton(text='День 2 (48 часов)', callback_data='day2')
        bat3 = types.InlineKeyboardButton(text='День 3 (72 часа)', callback_data='day3')
        bat4 = types.InlineKeyboardButton(text='День 4 (96 часа)', callback_data='day4')
        bat5 = types.InlineKeyboardButton(text='День 5 (120 часа)', callback_data='day5')
        bat6 = types.InlineKeyboardButton(text='День 6 (144 часа)', callback_data='day6')
        bat7 = types.InlineKeyboardButton(text='День 7 (168 часа)', callback_data='day7')
        bat8 = types.InlineKeyboardButton(text='День 8 (192 часа)', callback_data='day8')
        bat9 = types.InlineKeyboardButton(text='День 9 (216 часа)', callback_data='day9')
        bat10 = types.InlineKeyboardButton(text='День 10 (240 часа)', callback_data='day10')

        markup.add(bat1)
        markup.add(bat2)
        markup.add(bat3)
        markup.add(bat4)
        markup.add(bat5)
        markup.add(bat6)
        markup.add(bat7)
        markup.add(bat8)
        markup.add(bat9)
        markup.add(bat10)
        #Тут настроили клавиатуру markup
        await message.answer(text='Настройка отложенного постинга ⏰', reply_markup=markup)


#Изменение реквезитов у канала
@dp.callback_query_handler(text_startswith='day')
async def infopost_day(call: types.callback_query,state: FSMContext):
    day = int(call.data[3:]) #Номер дня
    print(day)
    status = int(cheack_status_postinga(day))
    if status == 0:
        status = '❌'
    else:
        status = '✅'

    markup = types.InlineKeyboardMarkup()
    post_v_posting_ = types.InlineKeyboardButton(text='Изменить пост', callback_data=f'post_v_posting_{day}')
    markup.add(post_v_posting_)
    if status == '❌':
        status_posting_ = types.InlineKeyboardButton(text=f'Включить постинг {day} дня ✅', callback_data=f'stat_posting_{day}')
        markup.add(status_posting_)
    else:
        status_posting_ = types.InlineKeyboardButton(text=f'Выключить постинг {day} дня ❌',callback_data=f'stat_posting_{day}')
        markup.add(status_posting_)


    await call.message.answer (text=f'Статус {day} дня : {status}',reply_markup=markup)


#Изменение поста в заготовленной рассылке
@dp.callback_query_handler(text_startswith='post_v_posting_')
async def send_post__day(call: types.callback_query,state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat0)

    if len(call.data) == 16:
        data = call.data[-1]
    else:
        data = call.data[-2:]

    await call.message.answer(text=f'Перешли уже готовый пост для заготовленной рассылки {data} дня',reply_markup=markup)

    await number_day.number.set() #Устанавливаем сет
    await state.update_data(NumberDay = data) #Записывает в сет номер дня для редактирования


#Изменение поста в канале
@dp.message_handler(state = number_day.number, content_types=['text','video','voice','photo','document','video_note'])
async def get_post_rassilka12321(message: types.Message, state: FSMContext):
    try:
        data_answer = (await state.get_data())['NumberDay']
        markup = message.reply_markup
        mes_id = await bot.copy_message(chat_id=channel_posts, message_id=message.message_id, from_chat_id=message.chat.id,reply_markup=markup)#Копируем в канал сообщение
        try:
            t = types.Message.to_python(message.reply_markup)
        except:
            t = None
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
    except:
        await message.answer(text='Ошибка номер 4138908')
    obnova_posting_message_id(day=data_answer, m_id=mes_id.message_id, keyboard=t)




#Изменение статуса в заготовленной рассылке
@dp.callback_query_handler(text_startswith='stat_posting_')
async def status_post__day(call: types.callback_query,state: FSMContext):
    try:
        data = (call.data[13:]) #Номер дня
        obnova_status_postinga(day=data)
        await call.message.answer(text=f'Успешно обновлен статус {data} дня')
    except:
        await call.message.answer(text='Код ошибки 19340932')




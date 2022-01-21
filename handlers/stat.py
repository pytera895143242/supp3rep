from aiogram import types
from misc import dp, bot

import asyncio

from .sqlit import reg_utm_support,cheak_support,reg_one_channel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg_stat_sup(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()

#Вывод работнику его статистики
@dp.message_handler(commands=['stat'])
async def statistika(message: types.Message):
    chat_id = message.chat.id
    answer = cheak_support()
    for i in answer:
        try:
            if int(i[1]) == chat_id:
                await bot.send_message(chat_id=message.chat.id, text= f'<b>Канал:</b> {i[0]}\n'
                                                                          f'<b>Неоплаченный трафик:</b> {i[3]}\n'
                                                                          f'<b>Трафика всего:</b> {i[2]}\n'
                                                                          f'<b>Реквезиты партнера:</b> {i[4]}',parse_mode='html')
        except:
            pass



# Регистрация работника для показа статистики
@dp.message_handler(commands=['reg'])
async def bat_reg_support123321(message: types.Message):
    await message.answer(text='Введите свой канал в формате @name_channel')
    await reg_stat_sup.step1.set()

@dp.message_handler(state=reg_stat_sup.step1, content_types='text')
async def get_reg_support123(message: types.Message, state: FSMContext):
    try:
        if message.text[0] == '@':
            await state.update_data(channel = message.text)
            reg_one_channel(message.text)
            await bot.send_message(chat_id=message.chat.id,text='Введите свои реквезиты. Например:\n'
                                                                'Киви: +78005553535')
            await reg_stat_sup.step2.set() # СОСТОЯНИЕ ИНФОРМАЦИИ ОБ АДМИНЕ
        else:
            await message.answer(text='Отменено. Введите /reg снова и повторите попытку. Вы ввели название своего канала не через @')
            await state.finish()
    except:
        await bot.send_message(chat_id=message.chat.id,text='Неудача')
        await state.finish()

@dp.message_handler(state=reg_stat_sup.step2, content_types='text')
async def get_reg_support3123(message: types.Message, state: FSMContext):
    info_about_parthers = await state.get_data()

    channel_support = info_about_parthers['channel'] #Канал Саппорта
    number_support = message.text  # Реквезиты саппорта
    id_support = message.chat.id #id Саппорта
    try:
        reg_utm_support(utm=channel_support, info=id_support, pay_info=number_support)  # Вносим в список кому показывается статистика
        await bot.send_message(message.chat.id,text='Успешно. Для просмотра статистики /stat')
        await state.finish()
    except:
        await bot.send_message(message.chat.id, text='Неудача!')
        await state.finish()
# Конец регистрация работника для показа статистики

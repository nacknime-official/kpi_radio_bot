""" Хендлеры бота """
from contextlib import suppress

from aiogram import Dispatcher, types, executor, exceptions
from aiogram.dispatcher.handler import SkipHandler

import core
from config import BOT
from consts import keyboards, texts
from utils import bot_filters

DP = Dispatcher(BOT)
bot_filters.bind_filters(DP)


@DP.message_handler(commands=['start'], pm=True)
async def start_handler(message: types.Message):
    await core.users.add_in_db(message)
    await message.answer(texts.START)
    await core.users.menu(message)


@DP.message_handler(commands=['cancel'], pm=True)
async def cancel(message: types.Message):
    await core.users.menu(message)


@DP.message_handler(commands=['notify'], pm=True)
async def notify_handler(message: types.Message):
    await core.users.notify_switch(message)


@DP.message_handler(content_types=['text', 'audio', 'photo', 'sticker'], reply_to_bot=True, pm=True)
async def user_reply_message_handler(message: types.Message):
    reply_to = message.reply_to_message

    # Реплай на сообщение обратной связи или сообщение от модера
    if reply_to.text == texts.FEEDBACK or core.communication.cache_is_set(reply_to.message_id):
        await core.communication.user_message(message)
        return await message.answer(texts.FEEDBACK_THANKS, reply_markup=keyboards.START)

    # Ввод названия песни
    if reply_to.text == texts.ORDER_CHOOSE_SONG and not message.audio:
        return await core.search.search_audio(message)

    raise SkipHandler


@DP.message_handler(content_types=['audio'], pm=True)
async def user_audio_handler(message: types.Message):
    # Пользователь скинул аудио
    return await core.users.send_audio(message.chat.id, tg_audio=message.audio)


@DP.message_handler(pm=True)
async def user_buttons_handler(message: types.Message):
    # Кнопка 'Что играет?'
    if message.text == keyboards.MAIN_MENU['what_playing']:
        await core.users.playlist_now(message)

    # Кнопка 'Заказать песню'
    elif message.text == keyboards.MAIN_MENU['order']:
        await message.answer(texts.ORDER_CHOOSE_SONG, reply_markup=types.ForceReply())
        await message.answer(texts.ORDER_INLINE_SEARCH, reply_markup=keyboards.ORDER_INLINE)

    # Кнопка 'Обратная связь'
    elif message.text == keyboards.MAIN_MENU['feedback']:
        await message.answer(texts.FEEDBACK, reply_markup=types.ForceReply())

    # Кнопка 'Помощь'
    elif message.text == keyboards.MAIN_MENU['help'] or message.text == '/help':
        await message.answer(texts.HELP['start'], reply_markup=keyboards.CHOICE_HELP)

    # Кнопка 'Расписание'
    elif message.text == keyboards.MAIN_MENU['timetable']:
        await core.users.timetable(message)

    else:
        raise SkipHandler


@DP.message_handler(pm=True)
async def user_other_handler(message: types.Message):
    # Говорим пользователю что он дурак
    await message.answer_document("BQADAgADlgQAAsedmEuFDrds0XauthYE", texts.UNKNOWN_CMD, reply_markup=keyboards.START)


# region admins

@DP.message_handler(commands=['next'], admins_chat=True)
async def next_handler(message: types.Message):
    await core.admins.next_track(message)


@DP.message_handler(commands=['update'], admins_chat=True)
async def update_handler(message: types.Message):
    await core.admins.update(message)


@DP.message_handler(commands=['ban'], admins_chat=True)
async def ban_handler(message: types.Message):
    await core.admins.ban(message)


@DP.message_handler(commands=['vol', 'volume'], admins_chat=True)
async def volume_handler(message: types.Message):
    await core.admins.set_volume(message)


@DP.message_handler(commands=['stats'], admins_chat=True)
async def stats_handler(message: types.Message):
    await core.admins.get_stats(message)


@DP.message_handler(commands=['log'], admins_chat=True)
async def log_handler(message: types.Message):
    await core.admins.get_log(message)


@DP.message_handler(commands=['playlist'], admins_chat=True)
async def playlist_handler(message: types.Message):
    await core.admins.show_playlist_control(message)


@DP.message_handler(content_types=['text', 'audio', 'photo', 'sticker'], reply_to_bot=True, admins_chat=True)
async def admins_reply_message_handler(message: types.Message):
    return await core.communication.admin_message(message)


# endregion


@DP.callback_query_handler()
async def callback_query_handler(query: types.CallbackQuery):
    cmd = query.data.split('-|-')

    #
    # Выбрали день
    if cmd[0] == 'order_day':
        await core.order.order_choose_time(query, int(cmd[1]))

    # Выбрали время
    elif cmd[0] == 'order_time':
        await core.order.order_make(query, int(cmd[1]), int(cmd[2]))

    # Кнопка назад при выборе времени
    elif cmd[0] == 'order_back_day' or cmd[0] == 'bad_order_but_ok':
        await core.order.order_choose_day(query)

    # Кнопка отмены при выборе дня
    elif cmd[0] == 'order_cancel':
        await core.order.order_cancel(query)

    # Выбрал время но туда не влезет
    elif cmd[0] == 'order_notime':
        await core.order.order_no_time(query, int(cmd[1]), int(cmd[2]))

    #
    # Принять / отклонить
    elif cmd[0] == 'admin_choice':
        await core.order.admin_choice(query, int(cmd[1]), int(cmd[2]), cmd[3])

    # Отменить выбор
    elif cmd[0] == 'admin_unchoice':
        await core.order.admin_unchoice(query, int(cmd[1]), int(cmd[2]), cmd[3])

    #
    # Кнопка "что будет играть" в сообщении "что играет"
    elif cmd[0] == 'playlist_next':
        await core.users.playlist_next(query)

    # Выбор дня
    elif cmd[0] == 'playlist_day':
        await core.users.playlist_choose_time(query, int(cmd[1]))

    # Выбор времени
    elif cmd[0] == 'playlist_time':
        await core.users.playlist_show(query, int(cmd[1]), int(cmd[2]))

    # Выбор времени
    elif cmd[0] == 'playlist_back':
        await core.users.playlist_choose_day(query)

    #
    # Кнопка в сообщении с инструкцией
    elif cmd[0] == 'help':
        await core.users.help_change(query, cmd[1])

    # Админская кнопка перемещения трека в плейлисте
    elif cmd[0] == 'admin_playlist_move':
        await core.admins.playlist_move(query, int(cmd[1]), int(cmd[2]))

    with suppress(exceptions.InvalidQueryID):
        await query.answer()


@DP.inline_handler()
async def query_text_handler(inline_query: types.InlineQuery):
    await core.search.inline_search(inline_query)


if __name__ == '__main__':
    executor.start_polling(DP, skip_updates=True)

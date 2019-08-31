from pathlib import Path


class TextConstants:
    START = 'Привет, это бот РадиоКПИ.\n'\
        'Ты можешь:\n'\
        ' - Заказать песню\n'\
        ' - Задать любой вопрос\n'\
        ' - Узнать, что играет сейчас, играло или будет играть\n'\
        ' - Узнать, как стать частью ламповой команды РадиоКПИ.\n'\
        '\n\n'\
        '⁉️Советуем первым делом прочитать инструкцию /help'
    MENU = 'Выбери, что хочешь сделать 😜'
    FEEDBACK = 'Ты можешь оставить отзыв о работе РадиоКПИ или предложить свою кандидатуру для вступления в наши ряды!'\
        '\nНапиши сообщение и админы ответят тебе! \n Или можешь написать в наш чат @rhub_kpi \n(⛔️/cancel)'
    FEEDBACK_THANKS = 'Спасибо за заявку, мы обязательно рассмотрим ее!'
    ORDER_CHOOSE_SONG = 'Что ты хочешь услышать? Напиши название или скинь свою песню\n(⛔️/cancel)'
    ORDER_INLINE_SEARCH = 'Нажми на кнопку для инлайн-поиска в нашем боте 👀 \n'\
        'По желанию можно использовать сторонних ботов, например @vkm4bot 🤷‍♀️'
    ORDER_CHOOSE_DAY = 'Теперь выбери день'
    ORDER_CHOOSE_TIME = '{0}, отлично. Теперь выбери время'
    ORDER_ON_MODERATION = 'Спасибо за заказ ({0}), ожидайте модерации!'
    ORDER_ACCEPTED = 'Ваш заказ ({0}) принят!'
    ORDER_ACCEPTED_UPNEXT = 'Ваш заказ ({0}) принят и заиграет {1}'
    ORDER_ERR_DENIED = 'Ваш заказ ({0}) отклонен('
    ORDER_ERR_TOOLATE = 'На это время уже точно не успеет'
    ORDER_ERR_ACCEPTED_TOOLATE = 'Мы хотели принять ваш заказ {0}, но он уже не влезет в эфир(('
    WHAT_PLAYING = '⏮ <b>Предыдущий трек: </b> {0}\n'\
        '▶ <b>Сейчас играет: </b> {1}\n'\
        '⏭ <b>Следующий трек: </b> {2}'
    SONG_NO_PREV = 'Не знаю( Используй историю 🤷‍♀️'
    SONG_NO_NEXT = 'Доступно только во время эфира'
    ERROR = 'Не получилось('
    UNKNOWN_CMD = 'Шо ты хош? Для заказа песни не забывай нажимать на кнопку "Заказать песню". Помощь тут /help'


class HelpConstants:
    ORDERS = '''
📝Есть 3 способа <b>заказать песню:</b>
- Нажать на кнопку <code>Заказать песню</code> и ввести название, бот выберет наиболее вероятный вариант
- Использовать инлайн режим поиска (ввести <code>@kpiradio_bot</code> или нажать на соответствующую кнопку). 
    В этом случае ты можешь выбрать из 50 найденных вариантов, с возможностью сначала послушать
- Загрузить или переслать боту желаемую песню
После этого необходимо выбрать день и время для заказа.'''
    CRITERIA = '''
 <b>❗️Советы:</b>
- Не отправляйте слишком много песен сразу, их все еще принимают люди, а не нейросети
- Учтите, что у песен с нехорошими словами или смыслом высокий шанс не пройти модерацию.
- Приветствуются песни на украинском <i>(гугл "квоты на радио")</i>
- Не приветствуется Корж и подобные ему.
- Приветствуются нейтральные, спокойные песни, которые не будут отвлекать от учебного процесса '''
    PLAYLIST = '''
<b>⏭Плейлист радио:</b>
- Узнать что играет сейчас, играло до этого или будет играть можно нажав на кнопку <code>Что играет</code>
- Помните дату и время когда играла песня и хотите ее найти? Можете найти ее там же <code>История</code>
- Если вы заказываете песню во время эфира, мы постараемся сделать так, что бы она заиграла следующей
- Заказ <b>одноразовый</b>. Если ваша песня не успела войти в эфир - закажите <b>на следующий раз</b>.'''
    FEEDBACK = '''
  <b>🖌Обратная связь:</b>
- Вы всегда можете написать команде админов что вы думаете о них и о радио
- Если хотите стать частью радио - пишите об этом и готовьтесь к анкетам
- Считаете что то неудобным? Есть предложения по улучшению? Не задумываясь пиши нам.
- У нас есть чат @rhub_kpi'''
    BTNS = {
        'orders': '📝Заказ песни',
        'criteria': '❗Модерация',
        'playlist': '⏭Тонкости плейлиста',
        'feedback': '🖌Обратная связь'
    }
    FIRST_MSG = 'Выберите интересующую вас тему. (Советуем прочитать все)'


bad_words = [
    'пизд',
    'бля',
    'хуй', 'хуя', 'хуи', 'хуе',
    'ебать', 'еби', 'ебло', 'ебля', 'ебуч',
    'долбо',
    'дрочит',
    'мудак', 'мудило',
    'пидор', 'пидар',
    'сука', 'суку',
    'гандон',
    'fuck', 'bitch', 'shit', 'dick', 'cunt'
]

times_name = {
    'week_days': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
    'next_days': ['Сегодня', 'Завтра', 'Послезавтра', 'Сейчас'],
    'times': ['Утренний эфир', 'Первый перерыв', 'Второй перерыв', 'Третий перерыв', 'Четвертый перерыв',
              'Вечерний эфир'],
}

broadcast_times = {
    #  day:
    #       num:  start, stop

    **dict.fromkeys(          # same value for many keys
        [0, 1, 2, 3, 4, 5, 6],
        {
            0: ('12:00', '18:00'),
            5: ('18:00', '22:00')
        }),

    'return_when_summer_end': {  # todo
            0: ('8:00', '8:30'),
            1: ('10:05', '10:25'),
            2: ('12:00', '12:20'),
            3: ('13:55', '14:15'),
            4: ('15:50', '16:10'),
            5: ('17:50', '22:00'),
        }
}

# paths = {
#     'orders': Path('D:/Вещание Радио/Заказы'),    # сюда бот кидает заказанные песни
#     'archive': Path('D:/Вещание Радио/Архив'),    # сюда песни перемещаются каждую ночь с папки заказов
#     'ether': Path('D:/Вещание Радио/Эфир'),       # тут песни выбранные радистами, не используется
# }

# todo летние пути, убрать потом
paths = {
    'orders': Path('D:/Вещание Радио/Летний эфир/Заказы'),
    'archive': Path('D:/Вещание Радио/Летний эфир/Архив'),
    'ether': Path('D:/Вещание Радио/Летний эфир/Эфир'),
}


def _time(s):
    h, m = s.split(':')
    return int(h)*60 + int(m)


broadcast_times_ = {
    day_k: {
        num_k: tuple(_time(time) for time in num_v)
        for num_k, num_v in day_v.items()
    } for day_k, day_v in broadcast_times.items()
}

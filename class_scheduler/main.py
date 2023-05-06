import telebot
from telebot import types
from weeknow import curr_week_for_bd, curr_week
from execute import get_day_formatting, get_week_formatting

token = "Your token"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}. ' \
           f'Команда /help покажет краткую информацию по командам данного бота.'
    bot.send_message(message.chat.id, mess, reply_markup=schedule_markup())


def schedule_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/monday", "/tuesday", "/wednesday", "/thursday", "/friday", "/saturday",
               "/currentweek", "/nextweek"]
    for button in buttons:
        markup.add(button)
    return markup

@bot.message_handler(commands=['help'])
def help_func(message):
    help_text = "Доступные команды:\n\n" \
                "/start - Начать работу с ботом и получить список доступных команд\n\n" \
                "/help - Получить список доступных команд\n\n" \
                "/mtuci - Получить ссылку на официальный сайт МТУСИ\n\n" \
                "/week - Получить информацию о текущей неделе\n\n" \
                "/monday, /tuesday, /wednesday, /thursday, /friday, /saturday- Получить расписание на конкретный день недели\n\n" \
                "/currentweek - Получить расписание на текущую неделю\n\n" \
                "/nextweek - Получить расписание на следующую неделю\n"
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['week'])
def help_bot(message):
    bot.send_message(message.chat.id, text=f'На данный момент {curr_week()} неделя')


@bot.message_handler(commands=['mtuci'])
def help_bot(message):
    bot.send_message(message.chat.id, text='Официальный сайт МТУСИ - https://mtuci.ru')


@bot.message_handler(commands=['monday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 1))}', parse_mode='HTML')


@bot.message_handler(commands=['tuesday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 2))}', parse_mode='HTML')


@bot.message_handler(commands=['wednesday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 3))}', parse_mode='HTML')


@bot.message_handler(commands=['thursday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 4))}', parse_mode='HTML')


@bot.message_handler(commands=['friday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 5))}', parse_mode='HTML')


@bot.message_handler(commands=['saturday'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 6))}', parse_mode='HTML')


@bot.message_handler(commands=['currentweek'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_week_formatting(curr_week_for_bd(0)))}', parse_mode='HTML')


@bot.message_handler(commands=['nextweek'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_week_formatting(curr_week_for_bd(1)))}', parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, text='Извините, я не понимаю')


bot.polling(none_stop=True, interval=0)

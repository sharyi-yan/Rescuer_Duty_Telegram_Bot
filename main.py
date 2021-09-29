from flask import Flask
from flask import request
import datetime
import telebot
from telebot import types
import os

TOKEN = 'Bot_Token'

APP_URL = f'https://heroku-flask-rescuer.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

names = []
duty_days = []
index_up = 1



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, photo='https://i.postimg.cc/N0htGPMC/channels4-banner.jpg', caption="БУДЬТЕ ВНИМАТЕЛЬНЫ: СЕГОДНЯШНЯЯ ДАТА ДОЛЖНА СОВПАДАТЬ С ВАШЕЙ СМЕНОЙ!!!"
                                      "\nДОЖДИТЕСЬ СВОЕЙ СМЕНЫ и введите 'Начать' для начала работы телеграмм бота:")


def main_menu(message):
    global keyboard_main_menu
    keyboard_main_menu = types.InlineKeyboardMarkup()
    button_Add_Duty = types.InlineKeyboardButton(text='Добавить в список дежурных', callback_data='button_Add_Duty')
    keyboard_main_menu.add(button_Add_Duty)
    button_Minus_Duty = types.InlineKeyboardButton(text='Удалить из списка дежурных', callback_data='button_Minus_Duty')
    keyboard_main_menu.add(button_Minus_Duty)
    button_Check_Duty = types.InlineKeyboardButton(text='Узнать когда дежуришь', callback_data='button_Check_Duty')
    keyboard_main_menu.add(button_Check_Duty)
    button_Now_Duty = types.InlineKeyboardButton(text='Сегодня дежурит:', callback_data='button_Now_Duty')
    keyboard_main_menu.add(button_Now_Duty)
    bot.send_message(message.chat.id, 'ВЫБЕРИТЕ ДЕЙСТВИЕ \nИЗ ПРЕДЛОЖЕННЫХ :', reply_markup=keyboard_main_menu)



@bot.message_handler(func=lambda call: True)
def get_first_message(message):
    START_CMD = 'начать'
    if message.text.lower() == START_CMD:
        start = datetime.datetime.today()
        end = start + datetime.timedelta(days=60)
        interval = datetime.timedelta(days=4)
        while start <= end:
            duty_days.append(start.strftime('%d:%m:%Y'))
            start += interval
        main_menu(message)
    else:
        bot.send_message(message.from_user.id, 'СЛЕДУЙТЕ УКАЗАНИЯМ ВЫШЕ')


@bot.callback_query_handler(func=lambda call: True)
def choose_operation(call):
    if call.data == 'button_main_menu':
        bot.send_message(call.message.chat.id, 'ВЫБЕРИТЕ ДЕЙСТВИЕ \nИЗ ПРЕДЛОЖЕННЫХ :', reply_markup=keyboard_main_menu)

    elif call.data == 'button_Add_Duty':
        bot.send_message(call.message.chat.id, 'Введите имя человека,которого хотите добавить в список дежурных:')
        bot.register_next_step_handler(call.message, add_name_duty)

    elif call.data == 'button_Minus_Duty':
        if len(names) >= 1:
            bot.send_message(call.message.chat.id, 'Введите имя человека, которого хотите удалить из списка дежурных:')
            bot.register_next_step_handler(call.message, delete_duty)
        else:
            no_names(call)

    elif call.data == 'button_confirm_delete':
        for n in names:
            if n == name_delete:
                keyboard_main_menu2 = types.InlineKeyboardMarkup()
                button_Add_Duty = types.InlineKeyboardButton(text='Добавить в список дежурных',
                                                             callback_data='button_Add_Duty')
                keyboard_main_menu2.add(button_Add_Duty)
                button_Minus_Duty = types.InlineKeyboardButton(text='Удалить из списка дежурных',
                                                               callback_data='button_Minus_Duty')
                keyboard_main_menu2.add(button_Minus_Duty)
                button_Check_Duty = types.InlineKeyboardButton(text='Узнать когда дежуришь',
                                                               callback_data='button_Check_Duty')
                keyboard_main_menu2.add(button_Check_Duty)
                button_Now_Duty = types.InlineKeyboardButton(text='Сегодня дежурит:', callback_data='button_Now_Duty')
                keyboard_main_menu2.add(button_Now_Duty)

                names.remove(n)
                bot.send_message(call.message.chat.id, name_delete + ' удален из списка дежурных!')
                bot.send_message(call.message.chat.id, 'ВЫБЕРИТЕ ДЕЙСТВИЕ \nИЗ ПРЕДЛОЖЕННЫХ :',
                                 reply_markup=keyboard_main_menu2)

    elif call.data == 'button_cancel_delete':
        bot.send_message(call.message.chat.id, 'ВЫБЕРИТЕ ДЕЙСТВИЕ \nИЗ ПРЕДЛОЖЕННЫХ :', reply_markup=keyboard_main_menu)

    elif call.data == 'button_Check_Duty':
        if len(names) >= 1:
            bot.send_message(call.message.chat.id, 'Введите имя человека чтобы узнать дату его дежурства:')
            bot.register_next_step_handler(call.message, name_recognize)
        else:
            no_names(call)

    elif call.data == 'button_Now_Duty':
        global index_today
        global today
        if len(names) >= 1:
            today = datetime.datetime.today().strftime('%d:%m:%Y')
            if duty_days[0] == today:
                confirm_duty(call)

            else:

                go_to_main_menu(call)

        else:
            no_names(call)

    elif call.data == 'button_confirm_today_duty':
        names.append(names[index_today])
        if today >= duty_days[0]:
            keyboard_go_to_main_menu = types.InlineKeyboardMarkup()
            button_go_to_main_menu = types.InlineKeyboardButton(text='Перейти в главное меню',
                                                                callback_data='button_main_menu')
            keyboard_go_to_main_menu.add(button_go_to_main_menu)


            bot.send_photo(call.message.chat.id, photo='https://i.postimg.cc/N0htGPMC/channels4-banner.jpg',
                           caption = f'{names[index_today]} - умывальников начальник \nи мочалок командир!', reply_markup=keyboard_go_to_main_menu)

            duty_days.pop(0)
            names.pop(0)


    elif call.data == 'button_cancel_today_duty':
        global index_up
        names.append(names[index_today])
        names[index_today], names[index_today + index_up] = names[index_today + index_up], names[index_today]
        index_up += 1
        confirm_duty(call)





def go_to_main_menu(call):
    global keyboard_go_to_main_menu2
    keyboard_go_to_main_menu2 = types.InlineKeyboardMarkup()
    button_go_to_main_menu2 = types.InlineKeyboardButton(text='Перейти в главное меню',
                                                         callback_data='button_main_menu')
    keyboard_go_to_main_menu2.add(button_go_to_main_menu2)
    bot.send_message(call.message.chat.id, 'Дежурный уже принял свой пост!!!', reply_markup=keyboard_go_to_main_menu2)


def confirm_duty(call):
    global keyboard_confirm_today_duty
    global index_today
    index_today = duty_days.index(today)
    bot.send_message(call.message.chat.id, 'Сегодня дежурит: ' + names[index_today])

    keyboard_confirm_today_duty = types.InlineKeyboardMarkup()
    button_confirm_today_duty = types.InlineKeyboardButton(text='Подтвердить',
                                                           callback_data='button_confirm_today_duty')
    button_cancel_today_duty = types.InlineKeyboardButton(text='Не дежурит', callback_data='button_cancel_today_duty')
    keyboard_confirm_today_duty.add(button_confirm_today_duty, button_cancel_today_duty)
    bot.send_message(call.message.chat.id, 'Нажмите "Подтвердить", \nесли ' + names[
        index_today] + ' дежурит сегодня \nИли "Не дежурит" - если нет!\nБУДЬТЕ ВНИМАТЕЛЬНЫ : \nИзменить дежурного сегодня \nбудет уже НЕЛЬЗЯ!!!',
                     reply_markup=keyboard_confirm_today_duty)


def name_recognize(message):
    global name_check
    name_check = message.text
    if name_check in names:
        index_name_check = names.index(name_check)
        bot.send_message(message.chat.id, name_check + ' дежурит: ' + duty_days[index_name_check])
        bot.send_message(message.chat.id, 'ВЫБЕРИТЕ ДЕЙСТВИЕ \nИЗ ПРЕДЛОЖЕННЫХ :', reply_markup=keyboard_main_menu)

    else:
        keyboard_mistake_recognize = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Попробовать еще', callback_data='button_Check_Duty')
        keyboard_mistake_recognize.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, name_check + ' нет в списке дежурных! \nПопробуйте ввести имя еще раз!',
                         reply_markup=keyboard_mistake_recognize)


def delete_duty(message):
    global name_delete
    name_delete = message.text
    if name_delete in names:
        keyboard_confirm_delete = types.InlineKeyboardMarkup()
        button_confirm_delete = types.InlineKeyboardButton(text='Удалить', callback_data='button_confirm_delete')
        button_cancel_delete = types.InlineKeyboardButton(text='Отмена', callback_data='button_cancel_delete')
        keyboard_confirm_delete.add(button_confirm_delete, button_cancel_delete)
        bot.send_message(message.chat.id, 'Вы хотите удалить ' + name_delete + ' из списка дежурных?',
                         reply_markup=keyboard_confirm_delete)

    else:
        keyboard_mistake_delete = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Попробовать еще', callback_data='button_Minus_Duty')
        keyboard_mistake_delete.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, name_delete + ' нет в списке дежурных! \nПопробуйте ввести имя еще раз!',
                         reply_markup=keyboard_mistake_delete)


def add_name_duty(message):
    global name1
    name1 = message.text
    bot.send_message(message.chat.id, 'Повторно введите имя человека:')
    bot.register_next_step_handler(message, add_finish)



def add_finish(message):
    global name2
    name2 = message.text

    if name1 == name2:
        names.append(name2)


        keyboard_correct_add = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Добавить еще', callback_data='button_Add_Duty')
        keyboard_correct_add.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, name2 + ' добавлен в список дежурных!', reply_markup=keyboard_correct_add)

    else:
        keyboard_mistake_add = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text=' Ввести имя ', callback_data='button_Add_Duty')
        keyboard_mistake_add.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, 'ИМЕНА НЕ СОВПАДАЮТ!!!', reply_markup=keyboard_mistake_add)



def no_names(call):
    global keyboard_no_names
    keyboard_no_names = types.InlineKeyboardMarkup()
    button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
    button_add_duty = types.InlineKeyboardButton(text='Добавить в список', callback_data='button_Add_Duty')
    keyboard_no_names.add(button_main_menu, button_add_duty)
    bot.send_message(call.message.chat.id, 'Список дежурных пока еще пуст!!! \nДобавьте людей в список дежурных!',
                     reply_markup=keyboard_no_names)




@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url= APP_URL)
    return "!", 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

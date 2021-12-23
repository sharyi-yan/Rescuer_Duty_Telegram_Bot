from flask import Flask
from flask import request
import datetime
import telebot
from telebot import types
import os
from database import db, cursor
import threading
from time import sleep


TOKEN = 'This is place for your Token'

APP_URL = f'https://name_your_app_on_heroku.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

delay = 50

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    cursor.execute("CREATE TABLE IF NOT EXISTS duty_days (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, date_order SMALLINT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rescuers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), name_order SMALLINT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS archive (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, name VARCHAR(255))")
    bot.send_photo(message.chat.id, photo='https://i.postimg.cc/N0htGPMC/channels4-banner.jpg', caption="БУДЬТЕ ВНИМАТЕЛЬНЫ: СЕГОДНЯШНЯЯ ДАТА ДОЛЖНА СОВПАДАТЬ С ВАШЕЙ СМЕНОЙ!!!"
                                      "\nДОЖДИТЕСЬ СВОЕЙ СМЕНЫ и введите 'Начать' для начала работы телеграмм бота:")

    
# Эта функция нужна чтобы обдурить бесплатный ClearDb, который разрывает соединение с базой данных, если в течении 60 секунд нет запросов))
def send_reminder():
    while True:
        cursor.execute("SELECT COUNT(id) FROM rescuers")
        sleep(delay)


treading = threading.Thread(target=send_reminder)
treading.start()


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
    start_cmd = 'начать'
    if message.text.lower() == start_cmd:
        cursor.execute('SELECT COUNT(*) FROM duty_days')
        result = cursor.fetchone()
        len_duty_days = result[0]
        if len_duty_days >= 1:
            main_menu(message)
        else:
            start = datetime.date.today()
            end = start + datetime.timedelta(days=365)
            interval = datetime.timedelta(days=4)

            while start <= end:
                query = "INSERT INTO duty_days (date) VALUES (%s)"
                value = start
                cursor.execute(query, (value,))
                cursor.execute("SET @num=0")
                cursor.execute("UPDATE duty_days SET date_order =@num:= (@num +1)")
                db.commit()
                start += interval
            main_menu(message)

    else:
        bot.send_message(message.from_user.id, 'СЛЕДУЙТЕ УКАЗАНИЯМ ВЫШЕ')


@bot.callback_query_handler(func=lambda call: True)
def choose_operation(call):
    if call.data == 'button_main_menu':
        main_menu(call.message)

    elif call.data == 'button_Add_Duty':
        bot.send_message(call.message.chat.id, 'Введите имя человека, которого хотите добавить в список дежурных:')
        bot.register_next_step_handler(call.message, add_name_duty)

    elif call.data == 'button_Minus_Duty':
        cursor.execute("SELECT COUNT(name) FROM rescuers")
        result = cursor.fetchone()
        len_rescuers = result[0]
        if len_rescuers >= 1:
            bot.send_message(call.message.chat.id, 'Введите имя человека, которого хотите удалить из списка дежурных:')
            bot.register_next_step_handler(call.message, delete_duty)
        else:
            no_names(call)

    elif call.data == 'button_confirm_delete':
        query = "DELETE FROM rescuers WHERE name = %s"
        value = name_delete
        cursor.execute(query, (value,))
        cursor.execute("SET @num=0")
        cursor.execute("UPDATE rescuers SET name_order =@num:= (@num +1)")
        db.commit()

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

        bot.send_message(call.message.chat.id, name_delete + ' удален из списка дежурных!')
        main_menu(call.message)

    elif call.data == 'button_cancel_delete':
        main_menu(call.message)

    elif call.data == 'button_Check_Duty':
        cursor.execute("SELECT COUNT(name) FROM rescuers")
        result = cursor.fetchone()
        len_rescuers = result[0]
        if len_rescuers >= 1:
            bot.send_message(call.message.chat.id, 'Введите имя человека чтобы узнать дату его дежурства: ')
            bot.register_next_step_handler(call.message, check_duty_date)
        else:
            no_names(call)

    elif call.data == 'button_Now_Duty':
        cursor.execute("SELECT COUNT(name) FROM rescuers")
        result = cursor.fetchone()
        len_rescuers = result[0]
        if len_rescuers >= 1:
            cursor.execute("SELECT COUNT(date) FROM duty_days WHERE date=CURDATE()")
            result = cursor.fetchone()
            result_value = result[0]
            if result_value >= 1:
                cursor.execute('CREATE TABLE IF NOT EXISTS counter (id INT AUTO_INCREMENT PRIMARY KEY, num SMALLINT)')
                query = 'INSERT INTO counter (num) VALUES (%s)'
                value = 1
                cursor.execute(query, (value,))
                db.commit()
                confirm_duty(call)

            else:
                not_today_duty_day(call)

        else:
            no_names(call)

    elif call.data == 'button_cancel_today_duty':
        query = 'INSERT INTO counter (num) VALUES (%s)'
        value = 1
        cursor.execute(query, (value,))
        db.commit()
        now_duty(call)

    elif call.data == 'button_confirm_today_duty':
        change_queue()
        delete_duty_day()
        cursor.execute("DELETE FROM counter WHERE id>0")
        db.commit()

        keyboard_go_to_main_menu = types.InlineKeyboardMarkup()
        button_go_to_main_menu = types.InlineKeyboardButton(text='Перейти в главное меню',
                                                            callback_data='button_main_menu')
        keyboard_go_to_main_menu.add(button_go_to_main_menu)

        bot.send_photo(call.message.chat.id, photo='https://i.postimg.cc/N0htGPMC/channels4-banner.jpg',
                        caption=f'{result_duty_name} - умывальников начальник \nи мочалок командир!',
                        reply_markup=keyboard_go_to_main_menu)


def confirm_duty(call):
    global keyboard_confirm_today_duty
    global result_duty_name

    cursor.execute(" SELECT COUNT(id) FROM counter")
    result_counter = cursor.fetchone()
    result_value = result_counter[0]

    query = "SELECT name FROM rescuers WHERE name_order= %s"
    cursor.execute(query, (result_value,))
    result = cursor.fetchone()
    if result is None:
        bot.send_message(call.message.chat.id, 'Еееййй... Очередь тю-тю, закончилась!!!')

    else:
        result_duty_name = result[0]
        bot.send_message(call.message.chat.id, f"Сегодня дежурит: {result_duty_name}")

        keyboard_confirm_today_duty = types.InlineKeyboardMarkup()
        button_confirm_today_duty = types.InlineKeyboardButton(text='Подтвердить',
                                                               callback_data='button_confirm_today_duty')
        button_cancel_today_duty = types.InlineKeyboardButton(text='Не дежурит',
                                                              callback_data='button_cancel_today_duty')
        keyboard_confirm_today_duty.add(button_confirm_today_duty, button_cancel_today_duty)
        bot.send_message(call.message.chat.id, f'Нажмите "Подтвердить", '
                                               f'\nесли {result_duty_name} дежурит сегодня \nИли "Не дежурит" - если нет!'
                                               f'\nБУДЬТЕ ВНИМАТЕЛЬНЫ : \nИзменить дежурного сегодня \nбудет уже НЕЛЬЗЯ!!!',
                         reply_markup=keyboard_confirm_today_duty)


def now_duty(call):
    cursor.execute("SELECT COUNT(name) FROM rescuers")
    result = cursor.fetchone()
    len_rescuers = result[0]
    if len_rescuers >= 1:
        cursor.execute("SELECT COUNT(date) FROM duty_days WHERE date=CURDATE()")
        result = cursor.fetchone()
        result_value = result[0]
        if result_value >= 1:
            confirm_duty(call)

        else:
            not_today_duty_day(call)

    else:
        no_names(call)


def not_today_duty_day(call):
    global keyboard_not_today_duty_day
    keyboard_not_today_duty_day = types.InlineKeyboardMarkup()
    button_go_to_main_menu3 = types.InlineKeyboardButton(text='Перейти в главное меню',
                                                         callback_data='button_main_menu')
    keyboard_not_today_duty_day.add(button_go_to_main_menu3)
    bot.send_message(call.message.chat.id, 'Дождитесь следующей смены!!! '
                                           '\nНазначить нового дежурного можно будет только в день смены!!!', reply_markup=keyboard_not_today_duty_day)


def change_queue():
    query_replica = "INSERT INTO rescuers(name) SELECT name FROM rescuers WHERE name = %s"
    value = result_duty_name
    cursor.execute(query_replica, (value,))

    query_insert = "INSERT INTO archive(name) SELECT name FROM rescuers WHERE name= %s LIMIT 1"
    cursor.execute(query_insert, (value,))

    query_delete = "DELETE FROM rescuers WHERE name= %s LIMIT 1"
    cursor.execute(query_delete, (value,))
    cursor.execute("SET @num=0")
    cursor.execute("UPDATE rescuers SET name_order =@num:= (@num +1)")
    db.commit()


def delete_duty_day():
    cursor.execute("SELECT date FROM duty_days WHERE date_order= 1")
    result = cursor.fetchone()
    value = result[0]
    query = "UPDATE archive SET date= %s WHERE name= %s"
    cursor.execute(query, (value, result_duty_name))

    cursor.execute("DELETE FROM duty_days WHERE date_order= 1")
    cursor.execute("SET @num=0")
    cursor.execute("UPDATE duty_days SET date_order =@num:= (@num +1)")
    db.commit()


def no_names(call):
    global keyboard_no_names
    keyboard_no_names = types.InlineKeyboardMarkup()
    button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
    button_add_duty = types.InlineKeyboardButton(text='Добавить в список', callback_data='button_Add_Duty')
    keyboard_no_names.add(button_main_menu, button_add_duty)
    bot.send_message(call.message.chat.id, 'Список дежурных пока еще пуст!!! \nДобавьте людей в список дежурных!',
                     reply_markup=keyboard_no_names)


def add_name_duty(message):
    global name1
    name1 = message.text
    query = "SELECT COUNT(name) FROM rescuers where name = %s"
    value = (name1)
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    result_value = result[0]

    if result_value >=1:

        keyboard_mistake_add = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Попробовать еще', callback_data='button_Add_Duty')
        keyboard_mistake_add.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, f"Дежурный {name1} уже есть в базе!!! \nНельзя дважды добавлять одно и то же имя!",
                                reply_markup=keyboard_mistake_add)
    else:
        bot.send_message(message.chat.id, 'Повторно введите имя человека:')
        bot.register_next_step_handler(message, add_finish)


def add_finish(message):
    global name2
    name2 = message.text

    if name1 == name2:
        query = "INSERT INTO rescuers (name) VALUES (%s)"
        value = name2
        cursor.execute(query, (value,))
        cursor.execute("SET @num=0")
        cursor.execute("UPDATE rescuers SET name_order =@num:= (@num +1)")
        db.commit()

        keyboard_correct_add = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Добавить еще', callback_data='button_Add_Duty')
        keyboard_correct_add.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, name2 + ' добавлен в список дежурных!')
        main_menu(message)

    else:
        keyboard_mistake_add = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text=' Ввести имя ', callback_data='button_Add_Duty')
        keyboard_mistake_add.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, 'ИМЕНА НЕ СОВПАДАЮТ!!!', reply_markup=keyboard_mistake_add)


def delete_duty(message):
    global name_delete
    name_delete = message.text
    query = "SELECT COUNT(name) FROM rescuers WHERE name= %s"
    value = name_delete
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    result_value = result[0]

    if result_value >= 1:
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


def check_duty_date(message):
    global name_check
    name_check = message.text
    query = "SELECT COUNT(name) FROM rescuers WHERE name = %s"
    value = name_check
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    result_value = result[0]

    if result_value >= 1:
        query1 = "SELECT name_order FROM rescuers WHERE name = %s LIMIT 0, 1"
        value1 = name_check
        cursor.execute(query1, (value1,))
        result = cursor.fetchone()
        result_value1 = result[0]

        query2 = "SELECT date FROM duty_days WHERE date_order = %s"
        value2 = result_value1
        cursor.execute(query2, (value2,))
        result = cursor.fetchone()
        result_value2 = result[0]

        bot.send_message(message.chat.id, f"{name_check}  дежурит:  {result_value2}")
        main_menu(message)

    else:
        keyboard_mistake_check_duty_date = types.InlineKeyboardMarkup()
        button_main_menu = types.InlineKeyboardButton(text='В главное меню', callback_data='button_main_menu')
        button_one_more = types.InlineKeyboardButton(text='Попробовать еще', callback_data='button_Check_Duty')
        keyboard_mistake_check_duty_date.add(button_main_menu, button_one_more)
        bot.send_message(message.chat.id, name_check + ' нет в списке дежурных! \nПопробуйте ввести имя еще раз!',
                         reply_markup=keyboard_mistake_check_duty_date)


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

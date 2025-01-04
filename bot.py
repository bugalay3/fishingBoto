import telebot
import pymysql.cursors
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import random


connection = pymysql.connect(host='localhost',
                             user='chiz',
                             password='1231',
                             database='riba',
                             cursorclass=pymysql.cursors.DictCursor)

bot = telebot.TeleBot("8073637300:AAEpVRPS5-Zfn4Ku7YYgJ5qwVu-kQgbUAEY", parse_mode=None)

fishCollection = []

def check_message_exists(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
        return True
    except Exception as e:
        if e.error_code == 400: 
            return False

def getFish(tier):
    rand = random.randint(1, 100)
    cumulative_probability = 0

    fishList = [fish for fish in fishCollection if fish['tier'] == tier]

    for fish in fishList:
        cumulative_probability += fish['rate']
        if rand <= cumulative_probability:
            return fish

def getFishCollection():
    with connection.cursor() as cursor:
        checkIfExistsSQL = ("select * from fish_collection;")
        cursor.execute(checkIfExistsSQL)
        collection = cursor.fetchall()
        global fishCollection
        fishCollection = collection

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    data = json.loads(call.data)

    if (data['event_id'] == 1):
        if (check_message_exists(call.message.chat.id, call.message.id)):
            if (data['success']):
                the_fish = [fish for fish in fishCollection if fish['id'] == data['the_fish_id']][0]
                bot.send_message(call.message.chat.id, f'вы поймиали {the_fish['name']}')
            else:
                bot.send_message(call.message.chat.id, 'рыба сорвалась!!')

def handleCastingALine(msg):

    fishBtn = random.randint(1, 25)

    #fetching the user's rod to determine which tier to generate fish from def 1
    fish = getFish(1) #tier 1
    markup = InlineKeyboardMarkup()

    for i in range(5): 
        row_buttons = []
        for j in range(1, 6): 
            button_number = i * 5 + j

            button = InlineKeyboardButton(text='🐟' if button_number == fishBtn else '🟦', callback_data=json.dumps({'event_id': 1, 'success': True if button_number == fishBtn else False, 'the_fish_id': fish['id']}))
                
            row_buttons.append(button)
        markup.add(*row_buttons)

    bot.send_message(msg.chat.id, "Выберите кнопку:", reply_markup=markup)

def handleStart(msg):
    with connection.cursor() as cursor:
        checkIfExistsSQL = ("select username, user_id from users where user_id = '%s';")
        cursor.execute(checkIfExistsSQL, msg.from_user.id)
        user = cursor.fetchone()
        
        if (user):

            bot.send_message(msg.chat.id, 'привет, ' + user['username'])
        else:

            addUserSQL = "INSERT INTO users (user_id, username, fishing_rod) VALUES (%s, %s, %s)"
            cursor.execute(addUserSQL, (msg.from_user.id, msg.from_user.username, str(msg.from_user.id) + "s_rod"))
            connection.commit()
            bot.send_message(msg.chat.id, 'привет, ' + msg.from_user.username + ' тебя добавили в бата')

with connection:

    getFishCollection()

    @bot.message_handler(func=lambda message: True)
    def send_welcome(msg):

        if (msg.text == '/start'):
            handleStart(msg)
        if (msg.text == '/cast_a_line'):
            handleCastingALine(msg)

    bot.infinity_polling()
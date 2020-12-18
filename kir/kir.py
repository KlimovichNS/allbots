import time
import telebot
import datetime
import telebot_calendar
from telebot_calendar import CallbackData
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import pandas as pd
from io import BytesIO 
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#bot = telebot.TeleBot('1171523590:AAEvAeI-ICnoQZe355KilvGLPmczfbsElxY')
bot = telebot.TeleBot('1278542676:AAEFRZhNoFxrrXdK2-E3tk_F_Z0vHevdJTU')

calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
state = {}
req_date = {}


    

def tip_import():
    spreadsheet_id = '1hrR2lJW32sRmHS5kZPdvRys-dNEYRgTIEGzaOjOJjCk'
    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
    r = requests.get(file_name) 
    df = pd.read_csv(BytesIO(r.content), dtype = {'Глава':'object'})
    a = [1,2] #список волн
    tip = ''
    for i in a:
        b = i
        out = df.query('Волна == @b')
        out = out.reset_index()
        for n in range(len(out.index)):
            tip += str(out.iat[n,1]) + ' - ' + str(out.iat[n,2]) + '\n'
    return tip


spreadsheet_id = {'Кадровые запросы':'1PrKh_dp-R882bzAcvcHL3M9Rcy5EL_OsNyfFeKEcYf8',
                  'Табельные запросы':''}

def choose_date(call):
    """
    :param message:
    :return:
    """

    now = datetime.datetime.now()  # Get the current date
    bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                          text="Выберите дату отчета:",
                          reply_markup=telebot_calendar.create_calendar(
                              name=calendar_1.prefix,
                              year=now.year,
                              month=now.month,
                              ),
                          )
                          
        
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = telebot_calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        day = f"{date.strftime('%d.%m.%Y')}"
        req_date[call.from_user.id] = day
        msg_text = '*' + state[call.from_user.id] + ' на дату: \n' + day + '* \n Введите код главы по БК:'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Вывести по всем', callback_data='all'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=state[call.from_user.id]))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
        
    elif action == "CANCEL":
        state[call.from_user.id] ='start'
        callback(call)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    state[user_id] = ''
    req_date[user_id] = ''
    tip = tip_import()#формирование закрепленного сообщения
    try:
        bot.unpin_chat_message(message.chat.id)#открепление старого закрепленного
    except:
        pass
    res = bot.send_message(message.chat.id, text=tip, parse_mode= "Markdown")
    bot.pin_chat_message(message.from_user.id, res.message_id)#закрепление сообщения 

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Кадровые запросы', callback_data='Кадровые запросы'))
    markup.add(telebot.types.InlineKeyboardButton(text='Табельные запросы', callback_data='Табельные запросы'))
    bot.send_message(message.chat.id, text='Выберите тип запроса:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global state, spreadsheet_id, req_date
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, text=call.data)

    if call.data == "В начало" :
        state[call.from_user.id] = ''
        req_date[call.from_user.id] = ''
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Кадровые запросы', callback_data='Кадровые запросы'))
        markup.add(telebot.types.InlineKeyboardButton(text='Табельные запросы', callback_data='Табельные запросы'))
        
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите тип запроса',
                              reply_markup=markup,
                              parse_mode= "Markdown")
    if call.data == "Кадровые запросы" or call.data == "Табельные запросы":
        state[call.from_user.id]= call.data
        req_date[call.from_user.id] = ''
        choose_date(call)
        
    if call.data == "all":
        try:
            date = req_date.get(call.from_user.id)
            sh_id = spreadsheet_id.get(state.get(call.from_user.id))
            file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(sh_id) 
            r = requests.get(file_name) 
            df_tabel = pd.read_csv(BytesIO(r.content), dtype = {'`БК`':'object'})
            df_tabel = df_tabel.fillna("-------")
            message_to_send = ''
            df_tabel = df_tabel[df_tabel['БК']!= '100']
            df_tabel = df_tabel[df_tabel['Дата']== date]
            msg_text = '*' + state[user_id] + '\n на ' + date + '\n *'
            for i in range(len(df_tabel.index)):
                message_to_send += "[" + df_tabel.iat[i,0] + '](' + df_tabel.iat[i,5] + ') ' + df_tabel.iat[i,2] + '\n '
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='В начало', callback_data='В начало'))
            message_to_send = msg_text + message_to_send
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_to_send, reply_markup=markup, parse_mode="Markdown")
        except:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='В начало', callback_data='В начало'))
            bot.send_message(call.message.chat.id, text='Задайте другие параметры', reply_markup=markup, parse_mode= "Markdown");
    return state, req_date


@bot.message_handler(content_types=['text'])
def code_input(message):
    global state, req_date
    
    user_id = message.from_user.id
    if req_date.get(user_id) != '' and state.get(user_id) !='':
        BK = message.text
        try:
            date = req_date.get(user_id)
            sh_id = spreadsheet_id.get(state[user_id])
            file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(sh_id) 
            r = requests.get(file_name) 
            df_tabel = pd.read_csv(BytesIO(r.content), dtype = {'`БК`':'object'})
            df_tabel = df_tabel.fillna("-------")
            msg_text = '*' + state[user_id] + '\n на ' + date + '\n *'
            message_to_send = ''
            df1 = df_tabel.query('`БК` == @BK')
            df1 = df1[df1['Дата']== date]
            
            #запрос к таблице по БК
            for i in range(len(df1.index)):
                message_to_send += '[' + df1.iat[i,0] + '](' + df1.iat[i,5] + ') ' + df1.iat[i,2] + '\n'
            if len(message_to_send)>2 :
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='В начало'))
                message_to_send = msg_text + message_to_send
                bot.send_message(message.chat.id, text = message_to_send, reply_markup=markup, parse_mode= "Markdown"); #проверка на непустое сообщение
            else :
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='В начало'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='В начало'))
                bot.send_message(message.chat.id,  text='Проверьте входные параметры', reply_markup=markup)

               
        except Exception as e:
            print(e)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='В начало', callback_data='В начало'))
            bot.send_message(message.chat.id, text='Неверный код', reply_markup=markup)
    else :
        bot.delete_message(message.chat.id, message.message_id)
        
if __name__ == '__main__' :
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(7)
        


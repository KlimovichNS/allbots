import telebot
import datetime
import time
import pandas as pd
from io import BytesIO 
import requests 
import numpy as np

#bot = telebot.TeleBot('1171523590:AAEvAeI-ICnoQZe355KilvGLPmczfbsElxY')#токен для отладки
bot = telebot.TeleBot('1222655772:AAFqhMIq6-neoYy7_OGcaVBVGOiJ6yR_EC8')
bot.delete_webhook()
sheet_id =['1bMzTytAtyy1pWXfdxEyFRdhOrKPF21Wd',#таблица пакетов
           '12NhRBW9Vw7OyDZtj-G5kq3S736hjdB2KfjU-gD9Am18', #статус интеграции
           '1hrR2lJW32sRmHS5kZPdvRys-dNEYRgTIEGzaOjOJjCk']#список глав по волнам
state = {}
BKu = {}
tip = '_здесь будет подсказка по кодам глав_'
tip_bot = ''
def Bold(string):
    string = '*'+string+'*'
    return string

def Italic(string):
    string = '_'+string+'_'
    return string

def tip_import():
    spreadsheet_id = sheet_id[2]
    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
    r = requests.get(file_name) 
    df = pd.read_csv(BytesIO(r.content), dtype = {'Глава':'object'})
    a = [1,2,3] #список волн
    tip = ''
    for i in a:
        b = i
        out = df.query('Волна == @b')
        out = out.reset_index()
        for n in range(len(out.index)):
            tip += str(out.iat[n,1]) + ' - ' + str(out.iat[n,2]) + '\n'
    return tip

@bot.message_handler(commands=['start'])

def start_message(message):
    
    user_id = message.from_user.id
    print(user_id)
    state[user_id] = ''
    BKu[user_id] = ''
    tip = tip_import()#формирование закрепленного сообщения
    try:
        bot.unpin_chat_message(message.chat.id)#открепление старого закрепленного
    except:
        pass
    
    res = bot.send_message(message.chat.id, text=tip, parse_mode= "Markdown")
    bot.pin_chat_message(message.from_user.id, res.message_id)#закрепление сообщения 
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Статус интеграции', callback_data='Статус интеграции'))
    markup.add(telebot.types.InlineKeyboardButton(text='Проверка пакетов', callback_data='Проверка пакетов'))
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text='Выберите тип запроса', reply_markup=markup)
    return state

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
        global sheet_id, state
        user_id = call.from_user.id
        if call.data == "delete":
            bot.answer_callback_query(call.id, text=call.data)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            
        if call.data == "start":
                bot.answer_callback_query(call.id, text=call.data)
                state[call.from_user.id] = ''
                BKu[call.from_user.id] = ''
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Статус интеграции', callback_data='Статус интеграции'))
                markup.add(telebot.types.InlineKeyboardButton(text='Проверка пакетов', callback_data='Проверка пакетов'))
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text='Выберите тип запроса', reply_markup=markup, parse_mode= "Markdown")
                bot.answer_callback_query(call.id, text=call.data)

        if call.data == "Пакеты по всем учреждениям":
                bot.answer_callback_query(call.id, text=call.data)
                spreadsheet_id = sheet_id[0]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'Код БК':'object'})
                kura = df[['ФОИВ', "Код БК", "Проверка пакетов 16.10"]]
                kura.columns = ['фоив', "БК", "статус ошибки"]
                name = 'Все учреждения'
                all_count = kura['БК'].count()
                status_not = kura.loc[kura['статус ошибки'] == 'есть ошибки','БК'].count()
                perc_all = status_not/all_count* 100
                status_no_problem = kura.loc[kura['статус ошибки'] == 'нет ошибок','БК'].count()
                perc_all_no_problem = status_no_problem/all_count * 100
                perc_all = str(np.format_float_positional(perc_all, precision=2))
                all_count = str(np.format_float_positional(all_count))[0:-1]
                status_not = str(np.format_float_positional(status_not, precision=2))[0:-1]
                
                perc_all_no_problem = str(np.format_float_positional(perc_all_no_problem, precision=2, trim='0'))
                status_no_problem = str(np.format_float_positional(status_no_problem, precision=2))[0:-1]
                message_to_send = Bold(call.data) + '\n'  + 'всего: ' + all_count + '\n' + 'есть ошибки: ' + status_not + '_ (' + perc_all + '%'+ ')_' + '\n' + 'нет ошибок: ' + status_no_problem + '_ (' + perc_all_no_problem + '%'+ ')_'
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Проверка пакетов'))
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")
                
        elif call.data == "Статус интеграции":
                state[call.from_user.id] = call.data
                BKu[user_id] = '' 
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Общая статистика', callback_data='Общая статистика'))
                markup.add(telebot.types.InlineKeyboardButton(text='Детализация по учреждениям', callback_data='Детализация по учреждениям'))
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='start'))
                msg_text = Bold(call.data) + '\n Выберите вариант отчета:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")


        elif call.data == "Проверка пакетов":
                state[call.from_user.id] = call.data
                
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Вывести по всем главам', callback_data='Пакеты по всем учреждениям'))
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='start'))
                msg_text = Bold(call.data) + '\n Укажите код главы по БК:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")

        elif call.data == "Детализация по учреждениям":
                BKu[user_id] = ''
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Не приступали', callback_data='Не приступали'))
                markup.add(telebot.types.InlineKeyboardButton(text='Сверка первичных сведений', callback_data='Первичный'))
                markup.add(telebot.types.InlineKeyboardButton(text='Расчет зарплаты', callback_data='Расчет зарплаты'))
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статус интеграции'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='start'))
                msg_text = Bold('Статус интеграции по списку') + '\nВыберите статус интеграции:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
                
        elif call.data == "Не приступали":
            bot.answer_callback_query(call.id, text=call.data)
            user_id = call.from_user.id
            state[user_id] = 'не приступали'
            if BKu.get(user_id) == '' or BKu.get(user_id) == None:
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Детализация по учреждениям'))
                msg_text = Bold('Статус интеграции по списку:\n Не приступали') + '\n Укажите код главы по БК:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
            else:
                BK = BKu[user_id]
                spreadsheet_id = sheet_id[1]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                kura = kura.dropna(subset = ['БК'])
                kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                kura['Статус'].unique()
                kura['Дата'] = kura['Дата'].fillna('нет')
                kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                kura['Переключение'] = kura['Переключение'].fillna('----')
                foiv_first = kura.query('БК == @BK')
                status = state[user_id]
                if status == 'операторская' or status == 'дата документа':
                        foiv = foiv_first .query('Переключение == @status')
                elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                        foiv = foiv_first .query('Статус == @status')
                foiv = foiv.reset_index()
                message_to_send ='*Статус интеграции по списку:*\n' + Bold('Не приступали') +'\n'+'код главы: ' + BK + '\n' +'~~~~~~~~~~\n'
                if foiv.empty == False:
                    str_count = len(message_to_send)

                    for i in range(len(foiv.index)):
                            if str_count > 4000 :
                                bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= "Markdown")
                                message_to_send = ''
                                str_count = 0
                            msg = foiv.iat[i,2] + '\n '
                            str_count += len(msg)
                            message_to_send += msg
                else :
                    message_to_send += '_нет учреждений_'
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Скрыть', callback_data='delete'))
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                
                
        elif call.data == "Расчет зарплаты":
                state[call.from_user.id] = 'Расчет зарплаты'
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Расчет з/п по данным ЕИСУ КС', callback_data='Операторская дата'))
                markup.add(telebot.types.InlineKeyboardButton(text='Сверка предыдущих периодов', callback_data='Дата документа'))
                markup.add(telebot.types.InlineKeyboardButton(text='Расчет з/п(общий)', callback_data='Дельта'))
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Детализация по учреждениям'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='start'))
                msg_text = Bold('Статус интеграции по списку:\n Расчет зарплаты')
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
                
        elif call.data == "Дельта":
            bot.answer_callback_query(call.id, text=call.data)
            user_id = call.from_user.id
            state[user_id] = 'дельта'
            if BKu.get(user_id) == '' or BKu.get(user_id) == None:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Расчет зарплаты'))
                msg_text = Bold('Статус интеграции по списку:\n Расчет з/п(общий)') + '\n Укажите код главы по БК:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
            else:
                BK = BKu[user_id]
                spreadsheet_id = sheet_id[1]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                kura = kura.dropna(subset = ['БК'])
                kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                kura['Статус'].unique()
                kura['Дата'] = kura['Дата'].fillna('нет')
                kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                kura['Переключение'] = kura['Переключение'].fillna('----')
                foiv_first = kura.query('БК == @BK')
                status = state[user_id]
                if status == 'операторская' or status == 'дата документа':
                        foiv = foiv_first .query('Переключение == @status')
                elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                        foiv = foiv_first .query('Статус == @status')
                foiv = foiv.reset_index()
                message_to_send ='*Статус интеграции по списку:*\n' + Bold('Расчет з/п(общий)') +'\n'+'код главы: ' + BK + '\n' +'~~~~~~~~~~\n'
                if foiv.empty == False:
                    str_count = len(message_to_send)

                    for i in range(len(foiv.index)):
                            if str_count > 4000 :
                                bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= "Markdown")
                                message_to_send = ''
                                str_count = 0
                            msg = foiv.iat[i,2] + '\n '
                            str_count += len(msg)
                            message_to_send += msg
                else :
                    message_to_send += '_нет учреждений_'
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Скрыть', callback_data='delete'))
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                
        elif call.data == "Первичный":
            bot.answer_callback_query(call.id, text=call.data)
            user_id = call.from_user.id
            state[user_id] = 'первичный'
            if BKu.get(user_id) == '' or BKu.get(user_id) == None:        
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Детализация по учреждениям'))
                msg_text = Bold('Статус интеграции по списку:\n Сверка первичных сведений') + '\n Укажите код главы по БК:'
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
            else:
                BK = BKu[user_id]
                spreadsheet_id = sheet_id[1]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                kura = kura.dropna(subset = ['БК'])
                kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                kura['Статус'].unique()
                kura['Дата'] = kura['Дата'].fillna('нет')
                kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                kura['Переключение'] = kura['Переключение'].fillna('----')
                foiv_first = kura.query('БК == @BK')
                status = state[user_id]
                if status == 'операторская' or status == 'дата документа':
                        foiv = foiv_first .query('Переключение == @status')
                elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                        foiv = foiv_first .query('Статус == @status')
                foiv = foiv.reset_index()
                message_to_send ='*Статус интеграции по списку:*\n' + Bold('Сверка первичных сведений') +'\n'+'код главы: ' + BK  + '\n' +'~~~~~~~~~~\n'
                if foiv.empty == False:
                    str_count = len(message_to_send)

                    for i in range(len(foiv.index)):
                            if str_count > 4000 :
                                bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= "Markdown")
                                message_to_send = ''
                                str_count = 0
                            msg = foiv.iat[i,2] + '\n '
                            str_count += len(msg)
                            message_to_send += msg
                else :
                    message_to_send += '_нет учреждений_'
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Скрыть', callback_data='delete'))
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")
               
        elif call.data == "Операторская дата":
                bot.answer_callback_query(call.id, text=call.data)
                user_id = call.from_user.id
                state[user_id] = 'операторская'
                if BKu.get(user_id) == '' or BKu.get(user_id) == None:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Расчет зарплаты'))
                    msg_text = Bold('Статус интеграции по списку:\n Расчет з/п по данным ЕИСУ КС') + '\n Укажите код главы по БК:'
                    #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
                else:
                    BK = BKu[user_id]
                    spreadsheet_id = sheet_id[1]
                    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                    r = requests.get(file_name) 
                    df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                    kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                    kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                    kura = kura.dropna(subset = ['БК'])
                    kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                    kura['Статус'].unique()
                    kura['Дата'] = kura['Дата'].fillna('нет')
                    kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                    kura['Переключение'] = kura['Переключение'].fillna('----')
                    foiv_first = kura.query('БК == @BK')
                    status = state[user_id]
                    if status == 'операторская' or status == 'дата документа':
                            foiv = foiv_first .query('Переключение == @status')
                    elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                            foiv = foiv_first .query('Статус == @status')
                    foiv = foiv.reset_index()
                    message_to_send ='*Статус интеграции по списку:*\n' + Bold('Расчет з/п по данным ЕИСУ КС') +'\n'+'код главы: ' + BK  + '\n' +'~~~~~~~~~~\n'
                    if foiv.empty == False:
                        str_count = len(message_to_send)

                        for i in range(len(foiv.index)):
                                if str_count > 4000 :
                                    bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= "Markdown")
                                    message_to_send = ''
                                    str_count = 0
                                msg = foiv.iat[i,2] + '\n '
                                str_count += len(msg)
                                message_to_send += msg
                    else :
                        message_to_send += '_нет учреждений_'
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Скрыть', callback_data='delete'))
                    bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")
                
        elif call.data == "Дата документа":
            bot.answer_callback_query(call.id, text=call.data)
            user_id = call.from_user.id
            state[user_id] = 'дата документа'
            if BKu.get(user_id) == '' or BKu.get(user_id) == None:
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Расчет зарплаты'))
                msg_text = Bold('Статус интеграции по списку:\n Сверка расчетов за предыдущие периоды') + '\n Укажите код главы по БК:'
               #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=msg_text, reply_markup=markup, parse_mode= "Markdown")
            else:
                BK = BKu[user_id]
                spreadsheet_id = sheet_id[1]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                kura = kura.dropna(subset = ['БК'])
                kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                kura['Статус'].unique()
                kura['Дата'] = kura['Дата'].fillna('нет')
                kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                kura['Переключение'] = kura['Переключение'].fillna('----')
                foiv_first = kura.query('БК == @BK')
                status = state[user_id]
                if status == 'операторская' or status == 'дата документа':
                        foiv = foiv_first .query('Переключение == @status')
                elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                        foiv = foiv_first .query('Статус == @status')
                foiv = foiv.reset_index()
                message_to_send ='*Статус интеграции по списку:*\n' + Bold('Сверка расчетов за предыдущие периоды') +'\n'+'код главы: ' + BK  + '\n' +'~~~~~~~~~~\n'
                if foiv.empty == False:
                    str_count = len(message_to_send)

                    for i in range(len(foiv.index)):
                            if str_count > 4000 :
                                bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= "Markdown")
                                message_to_send = ''
                                str_count = 0
                            msg = foiv.iat[i,2] + '\n '
                            str_count += len(msg)
                            message_to_send += msg
                else :
                    message_to_send += '_нет учреждений_'
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Скрыть', callback_data='delete'))
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")
                        
        elif call.data == "Общая статистика":
                state[call.from_user.id] = call.data
                BKu[call.from_user.id] = ''
                bot.answer_callback_query(call.id, text=call.data)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Вывести по всем главам', callback_data='Статистика по всем'))
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статус интеграции'))
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text="*Свод по интеграции:* \n Укажите код главы по БК", reply_markup=markup, parse_mode= "Markdown")
                              
        elif call.data == "Статистика по всем":
                bot.answer_callback_query(call.id, text=call.data)
                spreadsheet_id = sheet_id[1]
                file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                r = requests.get(file_name) 
                df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                kura = kura.dropna(subset = ['БК'])
                kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                kura['Статус'].unique()
                kura['Дата'] = kura['Дата'].fillna('нет')
                kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                kura['Переключение'] = kura['Переключение'].fillna('----')
                all_count = kura['БК'].count()
                status_delt = kura.loc[kura['Статус'] == 'дельта','БК'].count()
                status_perv = kura.loc[kura['Статус'] == 'первичный','БК'].count()
                status_not_start = kura.loc[kura['Статус'] == 'не приступали','БК'].count()
                type_oper = kura.loc[kura['Переключение'] == 'операторская','БК'].count()
                type_date = kura.loc[kura['Переключение'] == 'дата документа','БК'].count()
                delt_perc = status_delt/all_count * 100
                delt_perc = str(np.format_float_positional(delt_perc, precision=1, trim='0'))
                status_delt = str(np.format_float_positional(status_delt, precision=1))[0:-1]
                perv_perc = status_perv/all_count * 100
                perv_perc = str(np.format_float_positional(perv_perc, precision=1, trim='0'))
                status_perv = str(np.format_float_positional(status_perv, precision=1))[0:-1]
                not_perc = status_not_start/all_count * 100
                status_not_start = str(np.format_float_positional(status_not_start, precision=1))[0:-1]
                oper_perc = type_oper/all_count * 100 #последнее добавление
                oper_perc = str(np.format_float_positional(oper_perc, precision=1, trim='0'))#последнее добавление процент опер
                date_perc = type_date/all_count * 100#последнее добавление процент дата
                date_perc = str(np.format_float_positional(date_perc, precision=1, trim='0'))#последнее добавление
                not_perc = str(np.format_float_positional(not_perc, precision=1, trim='0'))
                all_count = str(np.format_float_positional(all_count))[0:-1]
                type_oper = str(np.format_float_positional(type_oper))[0:-1]
                type_date = str(np.format_float_positional(type_date))[0:-1]
                message_to_send = Bold('Общая статистика') + '\n'+ 'количество организаций: ' + all_count + '\n' + 'cтатус интеграции: '+ '\n' + 'не приступивших: ' + status_not_start + ' _(' + not_perc + '%)_' +'\n' + 'Сверка первичных сведений: ' + status_perv +' _(' + perv_perc + '%)_' + '\n'  + 'Расчет з/п: ' + status_delt +'_ (' + delt_perc + '%)_'  + '\n Из них:\n' + '- Сверка прошлых периодов: ' + type_date +'_ (' + date_perc + '%)_ \n' + '- По данным ЕИСУ КС: ' + type_oper +' _(' + oper_perc + '%)_'  + '\n'   
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Общая статистика'))
                #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                                         
        return state

@bot.message_handler(content_types=['text']) #пакеты по коду
def code_input(message):
        global sheet_id, state
        BKu [message.from_user.id] = message.text
        BK = message.text
        try:
            if state[message.from_user.id] == 'Проверка пакетов':               
                    spreadsheet_id = sheet_id[0]
                    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                    r = requests.get(file_name) 
                    df = pd.read_csv(BytesIO(r.content), dtype = {'Код БК':'object'})
                    kura = df[['ФОИВ', "Код БК", 'Сокращенное наименование', "Проверка пакетов 16.10", 'Ссылка на пакеты']]
                    kura.columns = ['фоив', "БК",'Наименование', "статус ошибки", 'ссылка']        
                    
                    foiv = kura.query('БК == @BK')
                    name = foiv.iat[0,0]
                    all_count = foiv['БК'].count()
                    status_not = foiv.loc[foiv['статус ошибки'] == 'есть ошибки','БК'].count()
                    perc_all = status_not/all_count * 100
                    status_no_problem = foiv.loc[foiv['статус ошибки'] == 'нет ошибок','БК'].count()
                    perc_all_no_problem = status_no_problem /all_count* 100
                    perc_all = np.format_float_positional(perc_all, precision=2, trim='0')
                    all_count = str(np.format_float_positional(all_count))[:-1]
                    status_not = str(np.format_float_positional(status_not, precision=2))[:-1]
                    
                    perc_all_no_problem = np.format_float_positional(perc_all_no_problem, precision=2, trim='0')
                    status_no_problem = str(np.format_float_positional(status_no_problem, precision=2))[:-1]
                    message_to_send = '*Проверка пакетов \n*' +  'Код главы: ' + Bold(BK) + '\n'+ ' ('+ name + ') \n' + 'всего: ' + all_count + '\n' + 'есть ошибки: ' + status_not + '_ (_' + Italic(perc_all) + '_%)_' + '\n' + 'нет ошибок: ' + status_no_problem + '_ (_' + Italic(perc_all_no_problem) + '_%)_'
                    err = 'есть ошибки'
                    #error_list = 'Проверка пакетов, приложение ' + BK + ':\n'
                    foiv = foiv.query('`статус ошибки` == @err')
                    if foiv.empty == False:
                        foiv = foiv.reset_index()
                        message_to_send += '\n [Отчеты по ошибкам](' + str(foiv.iat[0,5]) + ')'
                        #str_count = len(error_list)
                        #for i in range(len(foiv.index)):
                                #if str_count > 4000 :
                                    #bot.send_message(message.from_user.id, error_list, parse_mode= "Markdown")
                                    #error_list = ''
                                    #str_count = 0
                                #msg = str(foiv.iat[i,3]) + '\n'
                                #str_count += len(msg)
                                #error_list += msg
                        #bot.send_message(message.from_user.id, error_list, parse_mode= "Markdown")                       


                        
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Проверка пакетов'))
                    bot.send_message(message.from_user.id, message_to_send, reply_markup=markup, parse_mode= "Markdown")                       
                            
                                        
                    

                            
            elif state[message.from_user.id] == 'Общая статистика':
                    spreadsheet_id = sheet_id[1]
                    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                    r = requests.get(file_name) 
                    df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                    kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                    kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                    kura = kura.dropna(subset = ['БК'])
                    kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                    kura['Статус'].unique()
                    kura['Дата'] = kura['Дата'].fillna('нет')
                    kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                    kura['Переключение'] = kura['Переключение'].fillna('----')
                    foiv = kura.query('`БК` == @BK')
                    
                    all_count = foiv['БК'].count()
                    status_delt = foiv.loc[foiv['Статус'] == 'дельта','БК'].count()
                    status_perv = foiv.loc[foiv['Статус'] == 'первичный','БК'].count()
                    status_not_start = foiv.loc[foiv['Статус'] == 'не приступали','БК'].count()
                    type_oper = foiv.loc[foiv['Переключение'] == 'операторская','БК'].count()
                    type_date = foiv.loc[foiv['Переключение'] == 'дата документа','БК'].count()
                    
                    delt_perc = status_delt/all_count * 100
                    delt_perc = np.format_float_positional(delt_perc, precision=2, trim='0')
                    status_delt = str(np.format_float_positional(status_delt, precision=1))[:-1]
                    perv_perc = status_perv/all_count * 100
                    perv_perc = np.format_float_positional(perv_perc, precision=2, trim='0')
                    status_perv = str(np.format_float_positional(status_perv, precision=1))[:-1]
                    not_perc = status_not_start/all_count * 100
                    status_not_start = str(np.format_float_positional(status_not_start, precision=1))[:-1]
                    oper_perc = type_oper/all_count * 100 #последнее добавление
                    oper_perc = np.format_float_positional(oper_perc, precision=2, trim='0')#последнее добавление процент опер
                    date_perc = type_date/all_count * 100#последнее добавление процент дата
                    date_perc = str(np.format_float_positional(date_perc, precision=2, trim='0'))#последнее добавление
                    not_perc = np.format_float_positional(not_perc, precision=2, trim='0')
                    all_count = str(np.format_float_positional(all_count))[:-1]
                    type_oper = str(np.format_float_positional(type_oper))[:-1]
                    type_date = str(np.format_float_positional(type_date))[:-1]

                    message_to_send = '*Свод по интеграции* \nкод главы: ' + BK + '\n'+ 'количество учреждений: ' + all_count 
                    bot.send_message(message.from_user.id, text=message_to_send, parse_mode= "Markdown")


                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Детализация', callback_data='Не приступали'))                   
                    message_to_send = 'Не приступившие: ' + status_not_start + '_ (' + not_perc + '%)_'
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Детализация', callback_data='Первичный'))
                    message_to_send = 'Cверка первичных сведений: ' + status_perv +'_ (' + perv_perc + '%)_'
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Детализация', callback_data='Дельта'))
                    message_to_send = 'Расчет з/п(общий): ' + status_delt +'_ (' + delt_perc + '%)_'
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Детализация', callback_data='Дата документа'))
                    message_to_send = 'Расчет з/п - сверка предыдущих периодов: ' + type_date +' _(' + date_perc + '%)_'
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Детализация', callback_data='Операторская дата'))
                    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Общая статистика'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='start'))
                    message_to_send = 'Расчет з/п - по данным ЕИСУ КС: ' + type_oper +' _(' + oper_perc + '%)_'
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")

                    
                    
                    
                    state[message.from_user.id] = BK
                    
                    



                    
            elif state[message.from_user.id] !='':
                    spreadsheet_id = sheet_id[1]
                    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
                    r = requests.get(file_name) 
                    df = pd.read_csv(BytesIO(r.content), dtype = {'БК':'object'})
                    kura = df[[ "Код главы", "Организация", "первичный/дельта/не приступали", "тип переключения", "дата переключения"]]
                    kura.columns = ['БК','Организация',"Статус","Переключение","Дата" ]
                    kura = kura.dropna(subset = ['БК'])
                    kura.loc[kura['Статус'] == 'дельта ', 'Статус'] = "дельта" 
                    kura['Статус'].unique()
                    kura['Дата'] = kura['Дата'].fillna('нет')
                    kura.loc[kura['Переключение'] == 'операционная', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская ', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'операторская дата', 'Переключение'] = "операторская"
                    kura.loc[kura['Переключение'] == 'дата документа ', 'Переключение'] = "дата документа"
                    kura['Переключение'] = kura['Переключение'].fillna('----')
                    foiv_first = kura.query('БК == @BK')
                    status = state[message.from_user.id]
                    if status == 'операторская' or status == 'дата документа':
                            foiv = foiv_first .query('Переключение == @status')
                    elif status == 'дельта' or status == 'первичный' or status == 'не приступали':
                            foiv = foiv_first .query('Статус == @status')
                    foiv = foiv.reset_index()
                    message_to_send ='*Статус интеграции по списку:*\n' + Bold(state[message.from_user.id]) +'\n'+'код главы: ' + BK + '\n' + 'находятся на : ' + status  + '\n' +'~~~~~~~~~~\n'
                    if foiv.empty == False:
                        str_count = len(message_to_send)
                        for i in range(len(foiv.index)):
                                if str_count > 4000 :
                                    bot.send_message(message.from_user.id, message_to_send, parse_mode= "Markdown")
                                    message_to_send = ''
                                    str_count = 0
                                msg = foiv.iat[i,2] + '\n '
                                str_count += len(msg)
                                message_to_send += msg
                    else :
                        message_to_send += '_нет учреждений_'
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Детализация по учреждениям'))
                    bot.send_message(message.from_user.id, text=message_to_send, reply_markup=markup, parse_mode= "Markdown")
        except Exception as e:
            print(e)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='start'))
            #bot.send_message(1153266974, text=e, reply_markup=markup)
            bot.send_message(message.from_user.id, text='Проверьте входные параметры или начните сначала', reply_markup=markup)
        return BKu
                                               
if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(7)
        

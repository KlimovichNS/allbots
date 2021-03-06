import telebot
import datetime
import pandas as pd
from io import BytesIO 
import requests 
import numpy as np




state = {}
state_bk = {}
table_filter={}

DF = {}
sheet_id =['1zvPAJP6PNsZ7u37eV9uPCdZB29RCcOpBkTMDf6eXEXE', #статус миграции
           '1hrR2lJW32sRmHS5kZPdvRys-dNEYRgTIEGzaOjOJjCk'] #фоив - БК

#bot = telebot.TeleBot('1171523590:AAEvAeI-ICnoQZe355KilvGLPmczfbsElxY')#отладка
bot = telebot.TeleBot('1253376897:AAFssJD2m18CBgaVo4xaIR3_yFvonYtYCRw')


#def todb_count(user_id, a):
#    element = (user_id, '', a)
    

def send_stat_all_heads(user_id,df,a):
    
    all_count = df['БК'].count()
    #статус получена
    status_here = df.loc[df['получена'] == 'да','БК'].count()
    status_not_here = df.loc[df['получена'] == 'нет','БК'].count()
    status_not_matter = df.loc[df['получена'] == 'не требуется','БК'].count()
    # загружено  
    status_download = df.loc[df['загружено'] == 'загружено','БК'].count()
    status_not_download = df.loc[df['загружено'] == 'нет','БК'].count()
    # протоколы  
    status_plus = df.loc[df['протокол'] == 'положительный','БК'].count()
    status_minus = df.loc[df['протокол'] == 'отрицательный','БК'].count()
    #status_not_yet = df.loc[df['протокол'] == 'не требуется','БК'].count()
    status_not_yet_rec = df.loc[df['протокол'] == 'не получен','БК'].count()
    # перемиграция  
    status_need = df.loc[df['перемиграция'] == 'да','БК'].count()
    status_not_need = df.loc[df['перемиграция'] == 'не требуется','БК'].count()
    #загрузка_ВИС
    status_VIS = df.loc[df['загружено_ВИС'] == 'да','БК'].count()
    status_VIS_not = df.loc[df['загружено_ВИС'] == 'нет','БК'].count()
    #расчет значений
    perc_status_here = status_here / all_count * 100
    perc_status_not_here = status_not_here / all_count * 100
    perc_status_not_matter = status_not_matter / all_count * 100
    perc_status_download = status_download / all_count * 100
    perc_status_not_download = status_not_download / all_count * 100
    perc_status_VIS = status_VIS / all_count * 100
    perc_status_VIS_not = status_VIS_not / all_count * 100
    perc_status_plus = status_plus / all_count * 100
    perc_status_minus = status_minus / all_count * 100
    perc_status_need = status_need / all_count * 100
    perc_status_not_need = status_not_need / all_count * 100
    perc_status_not_yet_rec = status_not_yet_rec / all_count * 100
    all_count = str(np.format_float_positional(all_count))[0:-1]
    status_here = str(np.format_float_positional(status_here))[0:-1]
    status_not_here = str(np.format_float_positional(status_not_here))[0:-1]
    status_not_matter = str(np.format_float_positional(status_not_matter))[0:-1]
    status_download = str(np.format_float_positional(status_download))[0:-1]
    status_not_download = str(np.format_float_positional(status_not_download))[0:-1]
    
    status_plus = str(np.format_float_positional(status_plus))[0:-1]
    status_minus = str(np.format_float_positional(status_minus))[0:-1]
    status_not_yet_rec = str(np.format_float_positional(status_not_yet_rec))[0:-1]
    status_need = str(np.format_float_positional(status_need))[0:-1]
    status_not_need = str(np.format_float_positional(status_not_need))[0:-1]
    status_VIS = str(np.format_float_positional(status_VIS))[0:-1]
    status_VIS_not = str(np.format_float_positional(status_VIS_not))[0:-1]
    perc_status_here = str(np.format_float_positional(perc_status_here, precision=1, trim='0'))
    perc_status_not_here = str(np.format_float_positional(perc_status_not_here, precision=1, trim='0'))
    perc_status_not_matter = str(np.format_float_positional(perc_status_not_matter, precision=1, trim='0'))
    perc_status_download = str(np.format_float_positional(perc_status_download, precision=1, trim='0'))
    perc_status_not_download = str(np.format_float_positional(perc_status_not_download, precision=1, trim='0'))
    perc_status_VIS = str(np.format_float_positional(perc_status_VIS, precision=1, trim='0'))
    perc_status_VIS_not = str(np.format_float_positional(perc_status_VIS_not, precision=1, trim='0'))
    perc_status_plus = str(np.format_float_positional(perc_status_plus, precision=1, trim='0'))
    perc_status_minus = str(np.format_float_positional(perc_status_minus, precision=1, trim='0'))
    perc_status_not_yet_rec = str(np.format_float_positional(perc_status_not_yet_rec, precision=1, trim='0'))
    perc_status_need = str(np.format_float_positional(perc_status_need, precision=1, trim='0'))
    perc_status_not_need = str(np.format_float_positional(perc_status_not_need, precision=1, trim='0'))
    # сообщение на отправку
    message_to_send = '\n' + '*Количество учреждений: *' + all_count + '\n' + '*Статус получения баз: *' + '\n' + ' - получена: ' + status_here + '_ (_' + Italic(perc_status_here) + '_%)_' + '\n' + ' - не получена: ' + status_not_here + '_ (_' + Italic(perc_status_not_here) + '_%)_' + '\n'+'*Статус загрузки из ЕИСУ КС: *' + '\n' + '- загружена: ' + status_download + '_ (_' + Italic(perc_status_download) + '_%)_' + '\n' '- не загружена: ' + status_not_download + '_ (_' + Italic(perc_status_not_download) + '_%)_' + '\n' + '*Статус загрузки из ВИС: *' + '\n' + '- загружена: ' + status_VIS + '_ (_' + Italic(perc_status_VIS) + '_%)_' + '\n' '- не загружена: ' + status_VIS_not + '_ (_' + Italic(perc_status_VIS_not) + '_%)_' + '\n' + '*Статус протоколов: *' + '\n' + '- положительный: ' + status_plus + '_ (_' + Italic(perc_status_plus) + '_%)_' + '\n' + '- отрицательный: ' + status_minus + '_ (_' + Italic(perc_status_minus) + '_%)_'  + '\n' + '- не получен: ' + status_not_yet_rec + '_ (_' + Italic(perc_status_not_yet_rec) + '_%)_' + '\n' + '*Статус перемиграции: *' + '\n' + '- требуется: ' + status_need + '_ (_' + Italic(perc_status_need) + '_%)_' + '\n'+ '- не требуется: ' + status_not_need + '_ (_' + Italic(perc_status_not_need) + '_%)_' + '\n'
    msg_text = Bold('Статистика по всем учреждениям') + '\n('+a+')\n' + message_to_send
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
    bot.send_message(user_id, msg_text, reply_markup=markup, parse_mode= 'Markdown')

def send_stat_one_head(BK,user_id,df,a):
    if len(BK)!=3:
        name='error'
    else:
        name = get_name(BK)
    if name=='error':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статистика миграции'))
        bot.send_message(user_id, text='Проверьте правильность введенного кода главы. Обратите внимание, код главы - трехзначный', reply_markup=markup)
    else:
        foiv = df.query('БК == @BK')
        name = '(' + name + ')'
        all_count = foiv['БК'].count()
        status_here = foiv.loc[foiv['получена'] == 'да','БК'].count()
        status_not_here = foiv.loc[foiv['получена'] == 'нет','БК'].count()
        status_not_matter = foiv.loc[foiv['получена'] == 'не требуется','БК'].count()
        # загружено  
        status_download = foiv.loc[foiv['загружено'] == 'загружено','БК'].count()
        status_not_download = foiv.loc[foiv['загружено'] == 'нет','БК'].count()
        # протоколы  
        status_plus = foiv.loc[foiv['протокол'] == 'положительный','БК'].count()
        status_minus = foiv.loc[foiv['протокол'] == 'отрицательный','БК'].count()
        status_not_yet_rec = foiv.loc[foiv['протокол'] == 'не получен','БК'].count()
        #загрузка_ВИС
        status_VIS = foiv.loc[df['загружено_ВИС'] == 'да','БК'].count()
        status_VIS_not = foiv.loc[df['загружено_ВИС'] == 'нет','БК'].count()
        # перемиграция  
        status_need = foiv.loc[foiv['перемиграция'] == 'да','БК'].count()
        status_not_need = foiv.loc[foiv['перемиграция'] == 'не требуется','БК'].count()
        #расчет значений
        perc_status_here = status_here / all_count * 100
        perc_status_not_here = status_not_here / all_count * 100
        perc_status_not_matter = status_not_matter / all_count * 100
        perc_status_download = status_download / all_count * 100
        perc_status_not_download = status_not_download / all_count * 100
        perc_status_VIS = status_VIS / all_count * 100
        perc_status_VIS_not = status_VIS_not / all_count * 100
        perc_status_plus = status_plus / all_count * 100
        perc_status_minus = status_minus / all_count * 100
        perc_status_need = status_need / all_count * 100
        perc_status_not_need = status_not_need / all_count * 100
        perc_status_not_yet_rec = status_not_yet_rec / all_count * 100
        all_count = str(np.format_float_positional(all_count))[0:-1]
        status_here = str(np.format_float_positional(status_here))[0:-1]
        status_not_here = str(np.format_float_positional(status_not_here))[0:-1]
        status_not_matter = str(np.format_float_positional(status_not_matter))[0:-1]
        status_download = str(np.format_float_positional(status_download))[0:-1]
        status_not_download = str(np.format_float_positional(status_not_download))[0:-1]
        status_plus = str(np.format_float_positional(status_plus))[0:-1]
        status_minus = str(np.format_float_positional(status_minus))[0:-1]
        status_not_yet_rec = str(np.format_float_positional(status_not_yet_rec))[0:-1]
        status_need = str(np.format_float_positional(status_need))[0:-1]
        status_not_need = str(np.format_float_positional(status_not_need))[0:-1]
        status_VIS = str(np.format_float_positional(status_VIS))[0:-1]
        status_VIS_not = str(np.format_float_positional(status_VIS_not))[0:-1]
        perc_status_here = str(np.format_float_positional(perc_status_here, precision=1, trim='0'))
        perc_status_VIS = str(np.format_float_positional(perc_status_VIS, precision=1, trim='0'))
        perc_status_VIS_not = str(np.format_float_positional(perc_status_VIS_not, precision=1, trim='0'))
        perc_status_not_here = str(np.format_float_positional(perc_status_not_here, precision=1, trim='0'))
        perc_status_download = str(np.format_float_positional(perc_status_download, precision=1, trim='0'))
        perc_status_not_download = str(np.format_float_positional(perc_status_not_download, precision=1, trim='0'))
        perc_status_plus = str(np.format_float_positional(perc_status_plus, precision=1, trim='0'))
        perc_status_minus = str(np.format_float_positional(perc_status_minus, precision=1, trim='0'))
        perc_status_not_yet_rec = str(np.format_float_positional(perc_status_not_yet_rec, precision=1, trim='0'))
        perc_status_need = str(np.format_float_positional(perc_status_need, precision=1, trim='0'))
        perc_status_not_need =str(np.format_float_positional(perc_status_not_need, precision=1, trim='0'))
        # сообщение на отправку
        message_to_send = '\n' + '*Количество учреждений: *' + all_count + '\n' + '*Статус получения баз: *' + '\n' + '- получена: ' + status_here + '_ (_' + Italic(perc_status_here) + '_%)_' + '\n' + ' - не получена: ' + status_not_here + '_ (_' + Italic(perc_status_not_here) + '_%)_' + '\n' + '*Статус загрузки баз: *' + '\n' + '- загружена: ' + status_download + '_ (_' + Italic(perc_status_download) + '_%)_' + '\n' '- не загружена: ' + status_not_download + '_ (_' + Italic(perc_status_not_download) + '_%)_' + '\n' + '*Статус загрузки из ВИС: *' + '\n' + '- загружена: ' + status_VIS + '_ (_' + Italic(perc_status_VIS) + '_%)_' + '\n' '- не загружена: ' + status_VIS_not + '_ (_' + Italic(perc_status_VIS_not) + '_%)_' + '\n' + '*Статус протоколов: *' + '\n' + '- положительный: ' + status_plus + '_ (_' + Italic(perc_status_plus) + '_%)_' + '\n' + '- отрицательный: ' + status_minus + '_ (_' + Italic(perc_status_minus) + '_%)_'  + '\n' + '- не получен: ' + status_not_yet_rec + '_ (_' + Italic(perc_status_not_yet_rec) + '_%)_' + '\n' + '*Статус перемиграции: *' + '\n' + '- требуется: ' + status_need + '_ (_' + Italic(perc_status_need) + '_%)_' + '\n'+ '- не требуется: ' + status_not_need + '_ (_' + Italic(perc_status_not_need) + '_%)_' + '\n'
        msg_text = '*Статистика по главе *' + Bold(BK) + '\n' + name + ' '+a+'\n' + message_to_send
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статистика миграции'))
        bot.send_message(user_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')




def Get_Table():
    global sheet_id
    spreadsheet_id = sheet_id[0]
    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
    r = requests.get(file_name) 
    df = pd.read_csv(BytesIO(r.content), dtype = {'Код БК':'object','Код по СВР':'object'})
    df  = df[['Код по СВР',
              'GUID организации',
              'ФОИВ',
              'Код БК',
              'КРАТКОЕ НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ',#5
              'База получена',
              'дата получения базы',
              'проблемы (база при получении)',
              'Загружено из ЕИСУКС',
              'дата загрузки из ЕИСУКС',#10
              'проблемы при загрузке из ЕИСУКС ШР',
              'кол-во ошибок по отчету ЕИСУКС сотрудники',
              'Количество назначенных ЛД',
              'Дата подписания акта',
              'дата загрузки дампа в ЭБ',#15
              'Протокол (полож, отр)',
              'заявка на перемиграцию',
              'Загружено из ВИС',
              'проблемы загрузки из ВИС',
              'Дата протокола ВИС',#20
              'Признак',
              'Акт приема-передачи']]
    df.columns = ['СВР',
                  'GUID',
                  'фоив',
                  'БК',
                  'наименование',#5
                  'получена',
                  'дата получения',
                  'проблема(получение)',
                  'загружено',
                  'дата ЕИСУКС',#10
                  'проблемы',
                  'ошибки(сотрудники)',
                  'кол-во назначенных',
                  'дата акта п/п',
                  'дата дампа',#15
                  'протокол',
                  'перемиграция',
                  'загружено_ВИС',
                  'проблемы_ВИС',
                  'дата протокола ВИС',#20
                  'признак',
                  'акт п/п']
    df.loc[df['получена'] == 'Не требуется', 'получена'] = 'не требуется'
    df['протокол'] = df['протокол'].fillna('не получен')
    df['получена'] = df['получена'].fillna('нет')
    df['загружено'] = df['загружено'].fillna('нет')
    df['загружено_ВИС'] = df['загружено_ВИС'].fillna('нет')
    df['перемиграция'] = df['перемиграция'].fillna('не требуется')
    #print(df['загружено_ВИС'])
    return df

def status_count(call_data, user_id):
    global DF
    call = call_data
    df = DF[user_id]
    allcount = df.pivot_table(values = 'наименование', index = [call_data], aggfunc = ['count'])
    allcount = allcount.reset_index() 
    allcount.columns = ['Статус','Количество']
    text = ''
    for i in range(len(allcount)):
        text += str(allcount.iat[i,0]) + ' - ' + str(allcount.iat[i,1]) + '\n'
    return text
def get_values_SVR(df):
    df=df.fillna('-')
    #print(df['загружено_ВИС'])
    final_text=''
    #создание массива значений
    array_values = []
    array_values.append(str(df.iat[0,0])+'\n')
    array_values.append(str(df.iat[0,1])+'\n')
    array_values.append(str(df.iat[0,4])+'\n')
    array_values.append(str(df.iat[0,3])+' '+str(df.iat[0,2])+'\n')
    array_values.append(str(df.iat[0,6])+'\n')
    array_values.append(str(df.iat[0,7])+'\n')
    array_values.append(str(df.iat[0,9])+'\n')
    array_values.append(str(df.iat[0,10])+'\n')
    array_values.append(str(df.iat[0,11])+'\n')
    array_values.append(str(df.iat[0,12])+'\n')
    array_values.append(str(df.iat[0,13])+'\n')
    array_values.append(str(df.iat[0,17])+'\n')
    array_values.append(str(df.iat[0,18])+'\n')
    array_values.append(str(df.iat[0,15])+' '+str(df.iat[0,19])+'\n')

    array_text = []
    array_text.append('Код СВР:\n')
    array_text.append('GUID организации:\n')
    array_text.append('учреждение:\n')
    array_text.append('глава:\n')
    array_text.append('данные получены:\n')
    array_text.append('проблемы передачи:\n')
    array_text.append('загружено из ЕИСУ КС:\n')
    array_text.append('кол-во незагруженных позиций ШР:\n')
    array_text.append('кол-во незагруженных карточек Сотрудников:\n')
    array_text.append('всего кол-во карточек в ЕИСУ КС на 30.12.2020:\n')
    array_text.append('акт приема передачи:\n')
    array_text.append('загружено из ВИС:\n')
    array_text.append('проблемы загрузки из ВИС:\n')
    array_text.append('протокол:\n')
    #формирование текста сообщения
    for i in range(len(array_text)):
        array_text[i]=Bold(array_text[i])
        final_text += array_text[i]+array_values[i]
    return final_text
            

def get_name(BK):
    global sheet_id
    #print(BK)
    spreadsheet_id = sheet_id[1]
    file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
    r = requests.get(file_name) 
    df = pd.read_csv(BytesIO(r.content), dtype = {'Глава':'object'})
    df = df.query('Глава == @BK')
    df = df.reset_index()
    if df._get_value(0,3, takeable=True)!=3:
        name = 'error'
    else:
        name = str(df.iat[0,1])
    return name

def Bold(string):
    string = str(string)
    string = '*'+string+'*'
    return string

def Italic(string):
    string = str(string)
    string = '_'+string+'_'
    return string
def vyborka(user_id):
    global state_bk, DF
    if state_bk[user_id] == 'all':
        df = Get_Table()
        msg_text = 'Выборка по всем'
    else :
        df = Get_Table()
        BK =  state_bk[user_id]
        df = df.query('БК == @BK')
        df = df.reset_index()
        del df['index']
        name = get_name(BK)
        msg_text = 'Выборка по: ' + name
        msg_text = Bold(msg_text)
    DF[user_id] = df
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Полученные базы', callback_data='Полученные'))
    markup.add(telebot.types.InlineKeyboardButton(text='Загруженные базы', callback_data='Загруженные'))
    markup.add(telebot.types.InlineKeyboardButton(text='Перемиграция', callback_data='Перемиграция'))
    markup.add(telebot.types.InlineKeyboardButton(text='Протоколы', callback_data='Протоколы'))
    markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Выборка по статусу'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
    bot.send_message(user_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')
    return DF



@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    state[user_id] = ''
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Статистика миграции', callback_data='Статистика миграции'))
    markup.add(telebot.types.InlineKeyboardButton(text='Проблемы миграции', callback_data='Проблемы миграции'))
    markup.add(telebot.types.InlineKeyboardButton(text='Выборка по статусу', callback_data='Выборка по статусу'))
    markup.add(telebot.types.InlineKeyboardButton(text='Статус по учреждению', callback_data='Статус по учреждению'))
    bot.send_message(message.chat.id, text='*Выберите тип запроса*', reply_markup=markup, parse_mode= 'Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, text=call.data)
    global state, DF, state_bk

   

    if call.data == 'Статус по учреждению':
        
        state[call.from_user.id] = call.data
        user_id = call.from_user.id
        markup = telebot.types.InlineKeyboardMarkup()
        msg_text = 'Укажите код по сводному реестру:\n(используйте цифры от 0 до 9 и только латинские буквы)'
        markup.add(telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)
        


    
    if call.data == 'Полученные':
        
        user_id = call.from_user.id
        msg_text = status_count('получена',user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Список полученных', callback_data='базы получены'))
        markup.add(telebot.types.InlineKeyboardButton(text='Список неполученных', callback_data='базы не получены'))
        markup.add(telebot.types.InlineKeyboardButton(text='Не требуется передача', callback_data='не требуется'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Выборка по статусу'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)


    if call.data == 'Загруженные':
        
        user_id = call.from_user.id
        msg_text = status_count('загружено',user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Список загруженных в ЭБ', callback_data='загружены'))
        markup.add(telebot.types.InlineKeyboardButton(text='Список незагруженных в ЭБ', callback_data='не загружены'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Выборка по статусу'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'Перемиграция':
        
        user_id = call.from_user.id
        msg_text = status_count('перемиграция',user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Заявки на перемиграцию', callback_data='перемиграция'))
        markup.add(telebot.types.InlineKeyboardButton(text='Перемиграция не требуется', callback_data='не_перемиграция'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Выборка по статусу'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'Протоколы':
        
        user_id = call.from_user.id
        msg_text = status_count('протокол',user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Положительные', callback_data='положительные'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отрицательные', callback_data='отрицательные'))
        markup.add(telebot.types.InlineKeyboardButton(text='Не получены', callback_data='протоколы не получены'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Выборка по статусу'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'положительные':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['протокол'] == 'положительный']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Протоколы'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')
    if call.data == 'отрицательные':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['протокол'] == 'отрицательный']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Протоколы'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')


    if call.data == 'протоколы не получены':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['протокол'] == 'не получен']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Протоколы'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except Exception as e:
           bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')
    if call.data == 'перемиграция':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['перемиграция'] == 'да']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Перемиграция'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')
    if call.data == 'не_перемиграция':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['перемиграция'] == 'не требуется']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Перемиграция'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')
            
    if call.data == 'загружены':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['загружено'] == 'загружено']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Загруженные'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')    

    if call.data == 'не загружены':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['загружено'] == 'нет']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Загруженные'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')   


        
    if call.data == 'базы получены':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['получена'] == 'да']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Полученные'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')
    if call.data == 'базы не получены':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
            df = df.loc[df['получена'] == 'нет']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Полученные'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except Exception as e:
            print(e)
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')

    if call.data == 'не требуется':
        
        user_id = call.from_user.id
        try:
            df = DF[user_id]
        
            df = df.loc[df['получена'] == 'не требуется']
            message_to_send = ''
            df = df.reset_index()
            if df.empty == False:
                str_count = len(message_to_send)

                for i in range(len(df.index)):
                        if str_count > 3900 :
                            bot.send_message(chat_id=call.message.chat.id, text = message_to_send, parse_mode= 'Markdown')
                            message_to_send = ''
                            str_count = 0
                        msg = str(i+1) + ') ' + df.iat[i,5] + '\n '
                        str_count += len(msg)
                        message_to_send += msg
            else :
                message_to_send += '_нет учреждений_'
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Полученные'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=message_to_send, reply_markup=markup, parse_mode= 'Markdown')
        except:
            bot.send_message(user_id, text='Что-то пошло не так, попробуйте начать командой /start')

    
    if call.data == 'Назад':
        
        
        msg_text = '*Выберите тип запроса*'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Статистика миграции', callback_data='Статистика миграции'))
        markup.add(telebot.types.InlineKeyboardButton(text='Проблемы миграции', callback_data='Проблемы миграции'))
        markup.add(telebot.types.InlineKeyboardButton(text='Выборка по статусу', callback_data='Выборка по статусу'))
        markup.add(telebot.types.InlineKeyboardButton(text='Статус по учреждению', callback_data='Статус по учреждению'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')
        state[call.from_user.id] = ''
        
    if call.data == 'Статистика миграции':
        state[call.from_user.id] = call.data
        
        msg_text = Bold(call.data) + '\n' + 'Введите код главы:'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='По всем главам', callback_data='Статистика по всем учреждениям'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')
        
    if call.data == 'Проблемы миграции':
        state[call.from_user.id] = call.data
        
        msg_text = call.data + '\n' + 'Введите код главы:'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Вывести по всем', callback_data='Проблемы по всем учреждениям'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'Выборка по статусу':
        state[call.from_user.id] = call.data
        
        msg_text = call.data + '\n' + 'Введите код главы:'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выборка по всем', callback_data='Выборка по всем'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'Выборка по всем':
        
        state_bk[user_id] = 'all'
        df = vyborka(user_id)
        
    if call.data == 'Статистика по всем учреждениям':
        
        msg_text = 'Уточните выборку:'
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Все учреждения', callback_data='все_стат'))
        markup.add(telebot.types.InlineKeyboardButton(text='ЦА', callback_data='ЦА_все_стат'),telebot.types.InlineKeyboardButton(text='ТО', callback_data='ТО_все_стат'),telebot.types.InlineKeyboardButton(text='ФКУ', callback_data='ФКУ_все_стат'))
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статистика миграции'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup)

    if call.data == 'ЦА_все_стат':
        df = Get_Table()
        a='ЦА'
        df = df.query('признак == @a')
        send_stat_all_heads(user_id,df,a)

    if call.data == 'все_стат':
        df = Get_Table()
        a=''
        send_stat_all_heads(user_id,df,a)
    
    if call.data == 'ТО_все_стат':
        df = Get_Table()
        a='ТО'
        df = df.query('признак == @a')
        send_stat_all_heads(user_id,df,a)

    if call.data == 'ФКУ_все_стат':
        df = Get_Table()
        a='ФКУ'
        df = df.query('признак == @a')
        send_stat_all_heads(user_id,df,a)

    if call.data == 'ЦА_глава':
        df = Get_Table()
        BK =  state_bk[user_id]
        a='ЦА'
        df = df.query('признак == @a')
        send_stat_one_head(BK,user_id,df,a)

    if call.data == 'ТО_глава':
        df = Get_Table()
        BK =  state_bk[user_id]
        a='ТО'
        df = df.query('признак == @a')
        send_stat_one_head(BK,user_id,df,a)

    if call.data == 'ФКУ_глава':
        df = Get_Table()
        BK =  state_bk[user_id]
        a='ФКУ'
        df = df.query('признак == @a')
        send_stat_one_head(BK,user_id,df,a)

    if call.data == 'все_глава':
        df = Get_Table()
        BK =  state_bk[user_id]
        a=''
        send_stat_one_head(BK,user_id,df,a)
        
    if call.data == 'Проблемы по всем учреждениям':
        
        df = Get_Table()
        nope = 'нет'
        df = df.query('проблемы != @nope')
        df = df.groupby('проблемы')['наименование'].nunique()
        #print(df)
        message_to_send = ''
        df = df.reset_index()
        for i in range(len(df.index)):  
            message_to_send += df.iat[i,0] + ': \n    ' + str(df.iat[i,1]) + '\n'
        if message_to_send == '' : message_to_send = 'нет проблем'
        msg_text = Bold(call.data) + '\n' +  message_to_send
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')




        
    return state, DF

@bot.message_handler(content_types=['text']) #вывод по коду
def code_input(message):
    global state
    #получение таблицы
    df = Get_Table()
    #запрос по выбранной главе
    BK = str(message.text)
    
    user_id = message.from_user.id
    try:
    
        if state[user_id] == 'Выборка по статусу':
            state_bk[user_id] = BK
            vyborka(user_id)

        elif state[message.from_user.id] == 'Статистика миграции' :
            #sendstat(BK,user_id,df)
            state_bk[user_id]=BK
            msg_text = 'Уточните выборку:'
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Все учреждения', callback_data='все_глава'))
            markup.add(telebot.types.InlineKeyboardButton(text='ЦА', callback_data='ЦА_глава'),telebot.types.InlineKeyboardButton(text='ТО', callback_data='ТО_глава'),telebot.types.InlineKeyboardButton(text='ФКУ', callback_data='ФКУ_глава'))
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статистика миграции'))
            bot.send_message(user_id, text=msg_text, reply_markup=markup)

        elif state[user_id] == 'Проблемы миграции' :
            #поменять индексы
            name = get_name(BK)
            name = '(' + name + ')'
            df = df.query('БК == @BK')
            
            nope = 'нет'
            df = df.query('проблемы != @nope')
            df = df.groupby('проблемы')['наименование'].nunique()
            message_to_send = ''
            df = df.reset_index()
            for i in range(len(df.index)):  
                message_to_send += df.iat[i,0] + ': \n    ' + str(df.iat[i,1]) + '\n'
            if message_to_send == '' : message_to_send = 'нет проблем'
            msg_text = '*Проблемы миграции по главе *' + Bold(BK) + '\n' + name + '\n' +  message_to_send
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
            bot.send_message(user_id, text='Раздел находится в стадии разработки', reply_markup=markup, parse_mode= 'Markdown')


        elif state[user_id] == 'Статус по учреждению' :
            
            df = df.query('СВР == @BK')
            msg_text=get_values_SVR(df)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Статус по учреждению'),telebot.types.InlineKeyboardButton(text='В начало', callback_data='Назад'))
            bot.send_message(user_id, text=msg_text, reply_markup=markup, parse_mode= 'Markdown')

        else:
            bot.delete_message(message.chat.id, message.message_id)
        
            
            
    except Exception as e:
        print(e)
        #markup = telebot.types.InlineKeyboardMarkup()
        #markup.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='Назад'))
        bot.send_message(user_id, text='Произошла ошибка.Проверьте правильность введенного кода и попробуйте сначала, нажав /start')

    
def moysespoll():
    if __name__ == '__main__':
        try:
            bot.infinity_polling()
        except Exception as e:
            
            print(e)
            time.sleep(7)

moysespoll()

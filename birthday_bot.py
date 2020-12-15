import db_connect
import telebot
import datetime as dt
import time
import schedule
import pandas as pd
import requests
import threading

token = '1456040026:AAGgyrzAENSDEroayw9MalX7C4UmRVDir-A'
db_name = 'bdaylist.db'
tip = 'Этот бот напоминает о днях рождения.\nДля использования пришлите таблицу в формате .xlsx.\nПример таблицы будет ниже'
bot = telebot.TeleBot(token)

#создание таблицы пользователей


#параллелизация задач в расписании
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def read_table(uid):
    path = 'docs/' + str(uid) + '.xlsx'
    table = pd.read_excel(path)
    text = 'Файл загружен, содержит ' + str(len(table.index)) + ' строки'
    return text
    



def check_and_send():
    
    userlist = db_connect.get_users()
    for n in range(len(userlist)):
        print(n)
        path = 'docs/' + str(userlist[n]) + '.xlsx'
        table = pd.read_excel(path)    
        for i in range(len(table)):
            now = dt.datetime.date(dt.datetime.today())
            now_date = dt.date(now.year, table.iat[i,2].month, table.iat[i,2].day)#дата в текущем году
            
            if now == now_date :
                how_old = now.year - table.iat[i,2].year
                msg_to_send = 'Сегодня день рождения у:\n'
                msg_to_send += str(table.iat[i,0]) + '\n' + str(table.iat[i,3]) + '\n' + str(table.iat[i,1]) + '\n'
                msg_to_send +='\n Исполняется ' + str(how_old) + ' лет'
                print(msg_to_send)
                
                bot.send_message(userlist[n], text=msg_to_send)
            




@bot.message_handler(commands=['start'])
def start_message(message):
    uid = message.from_user.id
    name = str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)
    entities = [uid, name]
    con = db_connect.sql_connection()
    db_connect.users_table(con)
    con = db_connect.sql_connection()
    db_connect.sql_insert(con, entities)
    
    
    bot.send_message(uid, text=tip)
    ex = open('docs/' + 'example.xlsx', 'rb')
    bot.send_document(uid, ex)
    ex.close()


@bot.message_handler(content_types=["document"])
def handle_docs(message):
    uid = message.from_user.id
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    file_path ='docs/'
    file = bot.download_file(file_info.file_path)
    file_path += str(uid) +'.xlsx'
    with open(file_path, 'wb') as new_file:
        new_file.write(file)
        new_file.close()
    try:
        msg = read_table(uid)
        bot.send_message(uid, text=msg)
        db_connect.new_table(uid)
    except:
        bot.send_message(uid, text='не удалось загрузить файл')
    
def polling():
    if __name__ == '__main__':
        try:
            bot.infinity_polling()
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(7)
    return schedule.CancelJob
           





schedule.every().second.do(polling)
schedule.every().day.at("09:00").do(run_threaded, check_and_send)





while True:
    
    schedule.run_pending()
    time.sleep(1)



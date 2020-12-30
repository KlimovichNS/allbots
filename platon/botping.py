from telethon import TelegramClient, sync
import time



api_id = 2419610
api_hash = '687cbe9c453f32b5a56af9e8ef8d7a9d'
client = TelegramClient('session_name', api_id, api_hash)
#client.start()
#client.run_until_disconnected()
def ping():
    while True:
        client.send_message('platon_mbu_bot', '/start')
        print('send message')
        for n in range(0,14,1):
            time.sleep(60)
            print('#', end='')

if __name__ == '__main__':
    client.start()
    ping()
    client.run_until_disconnected()
    

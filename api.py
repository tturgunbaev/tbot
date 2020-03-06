import requests
import json

url = "https://api.telegram.org/bot{}/{}"

token = "1103159656:AAGJhmpijCeoxsQk1DZQfxKKgzv_VqdrLvI"
methods= {'update': url.format(token, 'Update'), 'getupdates': url.format(token, 'getUpdates'), 'send': 'sendMessage', 'kb': url.format(token, 'KeyboardButton')}


get_me = url.format(token, "getMe")

data = requests.post(methods['getupdates']).json()


def send_message(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url.format(token, methods['send']), params=payload)
    print(response.json())

# for _ in range(10):
#     text = "I love you Ainura"
#     send_message(578941100, text)

def get_chat_id():
    response = requests.post(methods['getupdates'])
    return response.json()['result'][-1]['message']['chat']['id']

def kb(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url.format(token, methods['kb']), params=payload)


# send_message(-419955772, 'SOme message')

response = requests.post(methods['getupdates'])
print(response.json()['result'])
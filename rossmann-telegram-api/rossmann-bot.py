import os
import json
import requests
import pandas as pd
from flask import Flask, request, Response

# Constants
TOKEN = '5002832482:AAGZIDOArzivZGmEx_FyRgmK3Z9JGQL0WvE'

# Info about the bot
# https://api.telegram.org/bot5002832482:AAGZIDOArzivZGmEx_FyRgmK3Z9JGQL0WvE/getMe

# Get Updates
#https://api.telegram.org/bot5002832482:AAGZIDOArzivZGmEx_FyRgmK3Z9JGQL0WvE/getUpdates

# Send Message
#https://api.telegram.org/bot5002832482:AAGZIDOArzivZGmEx_FyRgmK3Z9JGQL0WvE/sendMessage?chat_id=1149013271&text=I am very well, thx

# WebHook
#https://api.telegram.org/bot5002832482:AAGZIDOArzivZGmEx_FyRgmK3Z9JGQL0WvE/setWebhook?url=https://rossmann-telegram-bot-caio.herokuapp.com
#https://git.heroku.com/rossmann-telegram-bot-caio.git
#https://rossmann-telegram-bot-caio.herokuapp.com

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/'
    url = url + f'sendMessage?chat_id={chat_id}'

    r = requests.post(url, json={'text': text})
    print(f'Status Code {r.status_code}')

    return None

def loading_dataset(store_id):
    # loading test dataset
    df10 = pd.read_csv( 'test.csv' )
    df_store_raw = pd.read_csv( 'store.csv' )

    # merge test dataset + store
    df_test = pd.merge( df10, df_store_raw, how='left', on='Store' )

    # choose store for prediction
    df_test = df_test[df_test['Store'] == store_id]
    if not df_test.empty:
        # remove closed days and id columns
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop( 'Id', axis=1 )

        # convert Dataframe to json
        data = json.dumps( df_test.to_dict( orient='records' ) )

    else:
        data = 'Error'
    return data

def predict(data):
    # API Call
    url = ' https://rossmann-model-caio.herokuapp.com/rossmann/predict'
    header = {'Content-type': 'application/json' }
    data = data

    r = requests.post( url, data=data, headers=header )
    print( 'Status Code {}'.format( r.status_code ) )

    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )

    return d1

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']

    store_id = store_id.replace('/','')

    try:
        store_id = int(store_id)
    except ValueError:
        store_id = 'Error'
    return chat_id, store_id

#API Initialize
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, store_id = parse_message(message)
        if store_id != 'Error':
            # loading data
            data = loading_dataset(store_id)
            if data != 'Error':
                # predict
                d1 = predict(data)

                # calculation
                d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()

                # send message
                msg = 'Store Number {} will sell R$ {:,.2f} in the next 6 weeks'.format(
                d2['store'].values[0],
                d2['prediction'].values[0])

                send_message(chat_id, msg)
                return Response('Ok', status=200)
            else:
                send_message(chat_id, 'Store not Available')
                return Response('Ok', status = 200)
        else:
            send_message(chat_id, 'Store ID is Wrong')
            return Response('Ok', status=200)
    else:
        return '<h1> Rossmann Telegram Bot <\h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host = '0.0.0.0', port = port)




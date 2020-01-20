from urllib.parse import quote, unquote
import requests as req
from conf import apiKey

# telegram bot api key generated from bot father
api = apiKey

# for effecient request sending and gathering
def serv(page, *datas):
    data1 = ""
    for data in datas:
        data1 += data + "&"

    resp = req.get(f"https://api.telegram.org/bot{api}/"+page+"?"+data1)

    if resp.status_code == 200:
        return resp.json()
    return 0

# clear prev buffer - removes old messages if sent when server was not running
def tfreshStart():
    while 1:
        msg = serv('getupdates')
        if msg['result'] == []:
            break
        serv('getupdates', "offset="+str(msg['result'][0]['update_id']+1))
    return 1

# clear current buffer message
def clearBuffer(msg):
    serv('getupdates', "offset="+str(msg['result'][0]['update_id']+1))

# recive message send to the bot
def trecv():
    try:
        while 1:
            msg = serv("getupdates", "timeout=999999999")
            if msg['result'] != []:
                clearBuffer(msg)
                break
        return msg['result'][0]['message']['from']['id'], msg['result'][0]['message']['text']
    except:
        return False

# send message to user
def tsend(id, text):
    text = quote(text)
    return serv('sendmessage', "chat_id="+str(id), "text="+text)


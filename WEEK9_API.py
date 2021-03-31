import urllib.parse
import requests
import json
import datetime
import string

B_TOKEN = ""
ROOM_ID = ""

# main room = Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3

def findISSbyLocation(location):
    key = ""
    main_api = "http://open.mapquestapi.com/geocoding/v1/address?"

    url = main_api + urllib.parse.urlencode({"key":key, "location":location})
    json_data = requests.get(url).json()
    data_lat = json_data['results'][0]['locations'][0]['latLng']['lat']
    data_Lng = json_data['results'][0]['locations'][0]['latLng']['lng']
    
    req = requests.get("http://api.open-notify.org/iss-pass.json?lat="+str(data_lat)+"&lon="+str(data_Lng)+"&n=1")
    response = req.json()
    print(response)

    data = response['response'][0]
    date = datetime.datetime.fromtimestamp(data['risetime']).strftime("%Y-%m-%d %H:%M:%S")

    text2 = "ISS will pass {} by {} duration {} second(s).".format(location, date, data['duration'])
    text = "{} is located at Latitude and Longtitude are {} and {}".format(location.capitalize(), data_lat, data_Lng)

    return text+"\n"+text2

def retrieveMsg():
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(B_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'max':1}
    webex_response = requests.get(url=webex_url, headers=webex_auth, params=webex_param).json()
    return webex_response['items'][0]['text']

def senderMsg(text):
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(B_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'text':text}
    webex_response = requests.post(url=webex_url, headers=webex_auth, json=webex_param).json()
    print(webex_response)

def catFact():
    url = 'https://cat-fact.herokuapp.com/facts/random'
    catFact_response = requests.get(url=url).json()
    return catFact_response['text']

def getCurrencyFamily():

    url = 'https://bbl-sea-apim-p.azure-api.net/api/ExchangeRateService/Getfxfamily'
    access_token =  ""
    headers = {
        'Ocp-Apim-Subscription-Key':access_token
    }

    res = requests.get(url=url, headers=headers).json()
    text = "|---Family---|--------Description--------|"

    for i in res:
        text+="\n|{:^12}|".format(i['Family'])
        text+="{:^27}|".format(i['Description'])
    text += "\n"
    text += "-"*42

    return text

def exchangeService(amount, cur1, cur2):
    url = 'https://bbl-sea-apim-p.azure-api.net/api/ExchangeRateService/FxCal/{}/{}/{}'.format(amount, cur1, cur2)
    access_token =  ""
    headers = {
        'Ocp-Apim-Subscription-Key':access_token
    }

    print(amount)
    print(cur1)
    print(cur2)
    
    res = requests.get(url=url, headers=headers).json()

    return str(res)+" {}".format(cur2)

def main():

    while 1:
        msg = retrieveMsg()
        print(msg)

        if msg.startswith('/'):
            senderMsg(findISSbyLocation(msg[1:]))

        elif msg.lower() == 'cat':
            senderMsg(catFact())
        
        elif msg.startswith('+'):
            if msg.lower() == '+currency':
                senderMsg(getCurrencyFamily())
            elif 'to' in msg.lower()[1:]:
                subtext = msg.lower()[1:].split()
                senderMsg(exchangeService(subtext[0], subtext[1].upper(), subtext[3].upper()))
            
                
        
        elif msg.lower() == 'end':
            print("finish operation")
            break

main()
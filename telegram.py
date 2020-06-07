import json 
import requests
import os
from database import check_user, add_user, set_field, reset_field, get_state, change_parameters
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick2_ochl as candlestick
import matplotlib.dates as dates
from datetime import datetime


class telegram_bot():
    
    def __init__(self):
        token_file = open("token.cfg",'r')
        TOKEN = token_file.readline().strip('\n')
        token_file.close()
        self.url = "https://api.telegram.org/bot{}/".format(TOKEN)
        self.options = init_options()
        self.offset = 0
   
    def update_offset(self,update_id):
        self.offset = update_id + 1

    def get_url(self,url):
        response = requests.get(url)
        #content = response.content.decode("utf8")
        try:
            content = json.loads(response.text)['result'][0]
        except Exception as e:
            content = None
        return content

    def send_message(self,number,message):   
        url = self.url + "sendMessage?text={}&chat_id={}".format(message,number)
        self.get_url(url)
    
    def send_img(self,number,img_path):
        print("Sending file...")
        img = open(img_path,"rb")
        url = self.url + "sendPhoto?chat_id={}".format(number)
        files = {'photo':img}
        response = requests.post(url, files = files)
        print(response)

    def check_new_msg(self):
        url = self.url + "getUpdates?offset={}".format(self.offset)
        content = self.get_url(url)
        if content == None:
            return
        try:
            update_id = content['update_id']
            txt = content['message']['text']
            user_id = content['message']['from']['id']
            self.update_offset(update_id)
            if int(check_user(user_id)) == 1:
                if get_state(user_id,"on_register")[0][0] == 1:
                    txt = txt.strip(" ")
                    try:
                        text = txt.split(",")
                        res = change_parameters(user_id,text[0],text[1],text[2],text[3], text[4])
                    except Exception as e:
                        print(e)
                        res = 0
                    if res ==1:
                        self.send_message(user_id, "Valores registrados con exito!")
                        reset_field(user_id,"ack_eth")
                        reset_field(user_id,"ack_btc")
                    else:
                        self.send_message(user_id, "Hubo un problema registrando sus valores. Intentelo nuevamente")
                    reset_field(user_id, "on_register")
                else:
                    print(txt)
                    if txt == '1':
                        history_file = open("./history.txt")
                        last_prices = history_file.readlines()[-1]
                        history_file.close()
                        last_prices = last_prices.strip("\n")
                        last_prices = last_prices.split(",")
                        self.send_message(user_id,"Los ultimos precios registrados son:\nFECHA: "+last_prices[0]+"\nBTC = "+last_prices[1]+" USD"+"\nETH = "+last_prices[2]+" USD")
                    elif txt == '2':
                        generate_plot('BTC', get_state(user_id, 'hours')[0][0])
                        generate_plot('ETH', get_state(user_id, 'hours')[0][0])
                        self.send_img(user_id,"./btc.png")
                        self.send_img(user_id,"./eth.png")
                        self.send_img(user_id,"./btc_candlestick.png")
                        self.send_img(user_id,"./eth_candlestick.png")
                    elif txt == '3':
                        self.send_message(user_id,"Para registrarse correctamente, escriba los limites superiores e inferiores de su alarma separados por coma. Si no desea tener en cuenta un parametro escriba -1 en su valor. Por ejemplo: btc_sup,btc_inf,eth_sup,eth_inf, hours.\n")
                        set_field(user_id, "on_register")
                    elif txt == '4':
                        th_sup_btc = get_state(user_id,'th_sup_btc')[0][0]
                        th_inf_btc = get_state(user_id,'th_inf_btc')[0][0]
                        th_sup_eth = get_state(user_id,'th_sup_eth')[0][0]
                        th_inf_eth = get_state(user_id,'th_inf_eth')[0][0]
                        hours = str(get_state(user_id,'hours')[0][0])
                        self.send_message(user_id,"Tus parametros actuales son:\nLIMITE SUPERIOR BTC = " +th_sup_btc+"\nLIMITE INFERIOR BTC = "+th_inf_btc+"\nLIMITE SUPERIOR ETH = "+th_sup_eth+"\nLIMITE INFERIOR ETH = "+th_inf_eth+"\nVENTANA DE TIEMPO PARA GRAFICOS = "+hours+"h")
                    elif txt == 'btc_ok':
                        set_field(user_id , "ack_btc")
                        self.send_message(user_id, " Alarma de BTC reconocida!")
                        print("BTC ACK = 1")
                    elif txt == 'eth_ok':
                        set_field(user_id , "ack_eth")
                        self.send_message(user_id, " Alarma de ETH reconocida!")
                        print("ETH ACK = 1")
                    else:    
                        self.display_options(user_id)
            else:
                self.send_message(user_id,"Para registrarse correctamente, escriba los limites superiores e inferiores de su alarma separados por coma. Si no desea tener en cuenta un parametro escriba -1 en su valor. Por ejemplo: btc_sup,btc_inf,eth_sup,eth_inf, hours.\n")
                print(add_user(user_id))
                set_field(user_id, "on_register")
        except Exception as e:
            self.update_offset(update_id)
            print(e)
            pass
    
    def display_options(self,user_id): 
        msg = self.options
        self.send_message(user_id,msg) 

def init_options():
    options = get_str("./options/options.txt")
    return options

def get_str(file_path):
    file = open(file_path,'r')
    text = ""
    for line in file.readlines():
        text = text+line
    return text

def generate_plot(name,hours):
    dates = []
    btc = []
    eth = []
    n = 0
    history_file = open('./history.txt','r')
    lines  = history_file.readlines()
    history_file.close()
    date = datetime.now()
    while (datetime.now() - date).total_seconds() < hours * 3600:
        n = n + 1
        line = lines[-n].split(",")
        date = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f")
        btc_price = float(line[1])
        eth_price = float(line[2])
        dates.append(date)
        btc.append(btc_price)
        eth.append(eth_price)
    if name == 'BTC':
        fig, ax = plt.subplots()
        ax.plot(dates,btc)
        ax.set_title("Evolution of the price in the last "+str(hours)+" h")
        plt.xlabel("Date")
        plt.ylabel("BTC price")
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%H:%M') 
        plt.grid()
        plt.savefig("./btc.png")
        plt.clf()
        fig, ax = plt.subplots()
        opens, closes, highs, lows , d = get_candlesticks(btc,dates,2*hours)
        candlestick(ax, opens, closes, highs, lows, width = 0.6)
        print("Candlesticks for BTC plotted")
        ax.set_title("Evolution of the price in the last "+str(hours)+" h")
        plt.xlabel("Step = "str(2*hours)+" points")
        plt.ylabel("BTC price")
        plt.grid()
        plt.savefig("./btc_candlestick.png")
        plt.clf()
    if name == 'ETH':
        fig, ax = plt.subplots()
        ax.plot(dates,eth)
        ax.set_title("Evolution of the price in the last "+str(hours)+" h")
        plt.xlabel("Step")
        plt.ylabel("ETH price")
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%H:%M') 
        plt.grid()
        plt.savefig("./eth.png")
        plt.clf()
        fig, ax = plt.subplots()
        opens, closes, highs, lows, d = get_candlesticks(eth,dates,2*hours)
        candlestick(ax, opens, closes, highs , lows, width = 0.6) 
        ax.set_title("Evolution of the price in the last "+str(hours)+" h")
        plt.xlabel("Step = "str(2*hours)+" points")
        plt.ylabel("ETH price")
        plt.grid()
        plt.savefig("./eth_candlestick.png")
        plt.clf()

def get_candlesticks(price, date, ran):
    
    opens = []
    closes = []
    highs = []
    lows = []
    d = []
    i = 0
    while i < len(price) and i + ran - 1 < len(price):
        maximum = price[-1-i]
        minimum = price[-1-i]
        closing = price[-1-i - ran + 1]
        opening = price[-1-i]
        for j in range(ran - 1):
            if price[-1-i-j] > maximum:
                maximun = price[-1-i-j]
            if price[-1-i-j] < minimum:
                minimum = price[-1-i-j]
        opens.append(opening)
        closes.append(closing)
        highs.append(maximum)
        lows.append(minimum)
        d.append(date[i+ran-1])
        i = i + ran - 1
    return opens, closes, highs, lows, d

    
    
    

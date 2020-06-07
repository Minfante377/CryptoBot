from model import Currency, Logger
import time
import threading
from database import create_table, get_all_users, reset_field

UPDATE_TIME = 5
GRAPH = 10

log = Logger("./history.txt", UPDATE_TIME)
from queue_handler import init_bot, bot_loop, check_queue, update_queue
create_table()
init_bot()
bot_thread = threading.Thread(target = bot_loop)
bot_thread.start()
btc = Currency('BTC', 'USD')
eth = Currency('ETH', 'USD')
btc_price = btc.get_price()
eth_price = eth.get_price()
last_prices = log.get_last_line()
if not last_prices == None:
    last_prices = last_prices.split(",")
    btc_last_price = float(last_prices[1])
    eth_last_price = float(last_prices[2])
    btc_delta = (btc_last_price - btc_price) / btc_last_price * 100
    eth_delta = (eth_last_price - eth_price) / eth_last_price * 100
else:
    btc_delta = 0.0
    eth_delta = 0.0
log.log([btc_price,eth_price] , [btc_delta,eth_delta])
while True:
    print("\n" * 20)
    print("%s\t|%s\t|%s\t|%s\t|%s" %('DATE'.center(30),'BTC'.center(30),'ETH'.center(30),'DELTA_BTC %'.center(30),'DELTA_ETH %'.center((30))))
    lines = log.get_n_lines(GRAPH)
    for line in lines:
        line = line.strip("\n")
        line = line.split(",")
        print("%s\t|%s\t|%s\t|%s\t|%s" %(line[0].center(30),line[1].center(30),line[2].center(30),line[3].center(30),line[4].center(30)))
    time.sleep(UPDATE_TIME)
    btc_price = btc.get_price()
    eth_price = eth.get_price()
    last_prices = log.get_last_line()
    last_prices = last_prices.split(",")
    btc_last_price = float(last_prices[1])
    eth_last_price = float(last_prices[2])
    btc_delta = (btc_last_price - btc_price) / btc_last_price * 100
    eth_delta = (eth_last_price - eth_price) / eth_last_price * 100
    log.log([btc_price,eth_price] , [btc_delta,eth_delta])
    for user in get_all_users():
        telegram_id = user[0]
        th_sup_btc = float(user[4])
        ack_btc = int(user[1])
        ack_eth = int(user[2])
        th_inf_btc = float(user[5])
        th_sup_eth = float(user[6])
        th_inf_eth = float(user[7])
        if ( btc_last_price > th_sup_btc and ack_btc == 0 and th_sup_btc > 0 ):
            update_queue(telegram_id, "Se ha superado el limite superior para BTC!!!\nCotizacion actual: "+str(btc_last_price)+"\nLimite superior = " +str(th_sup_btc)+ "\nEscriba btc_ok para eliminar la alarma")
        elif ( btc_last_price < th_inf_btc and ack_btc == 0 and th_inf_btc > 0 ):
            update_queue(telegram_id, "La cotizacion ha caido por debajo del limite inferior para BTC!!!\nCotizacion actual: "+str(btc_last_price)+"\nLimite inferior = " +str(th_inf_btc)+ "\nEscriba btc_ok para eliminar la alarma")
        elif btc_last_price > th_inf_btc and btc_last_price < th_sup_btc:
           reset_field(telegram_id, 'ack_btc') 
        if ( eth_last_price > th_sup_eth and ack_eth == 0 and th_sup_eth > 0 ):
            update_queue(telegram_id, "Se ha superado el limite superior para ETH!!!\nCotizacion actual: "+str(eth_last_price)+"\nLimite superior = " +str(th_sup_eth) + "\nEscriba eth_ok para eliminar la alarma")
        elif ( eth_last_price < th_inf_eth and ack_eth == 0 and th_inf_eth > 0):
            update_queue(telegram_id, "La cotizacion ha caido por debajo del limite inferior para ETH!!!\nCotizacion actual: "+str(eth_last_price)+"\nLimite inferior = " +str(th_inf_eth) +"\n escriba eth_ok para eliminar la alarma")
        elif eth_last_price > th_inf_eth and eth_last_price < th_sup_eth:
            reset_field(telegram_id, "ack_eth")
    


    
    

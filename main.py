from model import Currency, Logger
import time
import threading
from database import create_table

UPDATE_TIME = 30
GRAPH = 10

log = Logger("./history.txt")
from queue_handler import init_bot, bot_loop
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
    


    
    

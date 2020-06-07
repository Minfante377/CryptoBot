from telegram import telegram_bot
import time



def init_bot():
    global telegram_bot
    global queue
    queue = []
    telegram_bot = telegram_bot()

def update_queue(user,msg):
    global queue
    queue.append((user,msg))

def check_queue():
    global queue
    for msg in queue:
        telegram_bot.send_message(msg[0],msg[1])
        queue.remove(msg)

def bot_loop():
    global queue
    while True:
        telegram_bot.check_new_msg()
        check_queue()
        time.sleep(0.5)

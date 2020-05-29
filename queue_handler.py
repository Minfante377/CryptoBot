from telegram import telegram_bot
import time



def init_bot():
    global telegram_bot
    global queue
    queue = []
    telegram_bot = telegram_bot()

def update_queue(target):
    global queue
    telegram_queue.append(target)

def bot_loop():
    global queue
    while True:
        telegram_bot.check_new_msg()
        time.sleep(0.1)

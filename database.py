import sqlite3

def create_table():
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    try:
        cursor.execute("""CREATE TABLE user (telegram_id VARCHAR(20) PRIMARY KEY,ack_btc INTEGER, ack_eth INTEGER,  on_register INTEGER ,th_sup_btc VARCHAR(30),th_inf_btc VARCHAR(30),th_sup_eth VARCHAR(30),th_inf_eth VARCHAR(30), hours INTEGER);""")
    except Exception as e:
        print(e)
        pass

def add_user(telegram_id,th_sup_btc = '-1.0' ,th_inf_btc = '-1.0', th_sup_eth = '-1.0', th_inf_eth = '-1.0'):
    try:
        db = sqlite3.connect("telegram_user.db")
        cursor = db.cursor()
        query = '''INSERT OR REPLACE  INTO user (telegram_id, ack_btc, ack_eth ,on_register, th_sup_btc, th_inf_btc, th_sup_eth, th_inf_eth, hours) VALUES(''' + str(telegram_id)+''',0,0,0,'''+th_sup_btc+''','''+ th_inf_btc + ''','''+th_sup_eth + ''',''' + th_inf_eth + ''', 4)'''
        cursor.execute(query)
        db.commit()
        return 1
    except Exception as e:
        print(e)
        return 0
    
def check_user(telegram_id):
    print(telegram_id)
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    query = "SELECT *  FROM user WHERE telegram_id = "+str(telegram_id)
    cursor.execute(query)
    res = cursor.fetchall()
    print(str(res))
    if len(res) == 0:
        return 0
    else:
        return 1

def set_field(telegram_id, field):
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    query = "UPDATE user SET " + field + " = 1 WHERE telegram_id = " + str(telegram_id)
    cursor.execute(query)
    db.commit()

def reset_field(telegram_id, field):
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    query = "UPDATE user SET " + field + " = 0 WHERE telegram_id = " + str(telegram_id)
    cursor.execute(query)
    db.commit()

def change_parameters (telegram_id, th_sup_btc, th_inf_btc, th_sup_eth, th_inf_eth, hours):
    try:
        float(hours)
        float(th_sup_btc)
        float(th_inf_btc)
        float(th_sup_eth)
        float(th_inf_eth)
    except Exception as e:
        print(e)
        return 0
    try:
        if int(hours) < 0:
            hours = '4'
        db = sqlite3.connect("telegram_user.db")
        cursor = db.cursor()
        query = "UPDATE user SET th_sup_btc = "+th_sup_btc+",th_inf_btc = "+th_inf_btc+",th_sup_eth = "+th_sup_eth +", th_inf_eth = "+th_inf_eth +", hours =" + hours + " WHERE telegram_id = " + str(telegram_id)
        cursor.execute(query)
        db.commit()
        return 1
    except:
        return 0


def get_state(telegram_id, field):
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    query = "SELECT "+ field + " FROM user WHERE telegram_id = " + str(telegram_id)
    cursor.execute(query)
    res = cursor.fetchall()
    return res

def get_all_users():
    db = sqlite3.connect("telegram_user.db")
    cursor = db.cursor()
    query = "SELECT * FROM user"
    cursor.execute(query)
    res = cursor.fetchall()
    return res

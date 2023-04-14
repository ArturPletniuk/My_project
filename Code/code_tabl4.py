import sqlite3
from sqlite3 import Error
from datetime import datetime
def tabl4(link):
    year = datetime.today().year
    month_nay = datetime.today().month   ### текущий месяц
    if month_nay < 10:
        month_nay = '0'+ str(month_nay)
    else:
        month_nay = str(month_nay) 
    daten = str(year)+'-'+ month_nay      ## это текущий год и текущий месяц для третьей таблицы    
    conect = sqlite3.connect(link)
    ### функция для выборки одного знвчения из базы
    def value(conect,x):
        y =  func(conect,x)
        for i in y:
            for j in i:
                return j
    def func(conect,reqest):
        cursor =  conect.cursor()
        try:
            value = cursor.execute(reqest)
            conect.commit()
            #print("Подключение к базе данных SQLite прошло успешно")
        except Error as e:
            return f"Произошла ошибка {e}" 
        return value 
    lession = f"""SELECT SUM(number_of_lession) FROM client_month WHERE  date GLOB '*-{month_nay}' """
    lession = value(conect,lession)
    price = f"""SELECT SUM(price_lesson) FROM client_month WHERE  date GLOB '*-{month_nay}' """
    price = value(conect,price)
    date = f"""SELECT COUNT(date) FROM price_month WHERE date = '{daten}'"""
    f = func(conect,date)
    for i in f:
        for j in i:
            date = j    
    if date == 1:
        update_client = f"""UPDATE  price_month SET number_of_lession_month = {lession}, price_lession  = {price}, date  = '{daten}'
    WHERE date = '{daten}'"""
        base = func(conect,update_client)
    else:    
        update_client = f"""INSERT INTO price_month ('number_of_lession_month','price_lession','date')
        VALUES ('{lession}','{price}','{daten}')"""
        base = func(conect,update_client) 





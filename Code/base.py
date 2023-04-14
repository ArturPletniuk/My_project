import sqlite3
from sqlite3 import Error
conect = sqlite3.connect('C:/Users/admin/Desktop/Extension/baza.db')
def func(conect,reqest):
    cursor =  conect.cursor()
    try:
        value = cursor.execute(reqest)
        conect.commit()
        print("Подключение к базе данных SQLite прошло успешно")
    except Error as e:
        return f"Произошла ошибка {e}" 
    return value 
tabl = """CREATE TABLE IF NOT EXISTS client 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomer INTEGER  DEFAULT  0,
        message TEXT DEFAULT  message,
        elictronic_diary TEXT DEFAULT https,
        mother TEXT DEFAULT mother,
        child TEXT DEFAULT child,
        ade REAL DEFAULT 0,
        soudrs TEXT DEFAULT abcde,
        number_of_lession INTEGER NOT NULL,
        praice TEXT DEFAULT praice )"""
tabl2 = """CREATE TABLE IF NOT EXISTS client_day 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomer INTEGER  DEFAULT  0,
        mother TEXT DEFAULT mother,
        date TEXT DEFAULT date,
        number_of_lession REAL,
        price_lesson INTEGER ,
        praice TEXT DEFAULT praice,
        client_id INTEGER,
        FOREIGN KEY (client_id)  REFERENCES client (id) )"""
tabl3 = """CREATE TABLE IF NOT EXISTS client_month 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomer INTEGER  DEFAULT  0,
            mother TEXT DEFAULT mother,
            date TEXT DEFAULT date,
            number_of_lession INTEGER,
            price_lesson INTEGER ,
            praice TEXT DEFAULT praice)"""
tabl4 = """CREATE TABLE IF NOT EXISTS price_month 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_of_lession_month INTEGER,
            price_lession INTEGER,
            date TEXT DEFAULT date)"""
tabl5 = """CREATE TABLE IF NOT EXISTS extension 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomer INTEGER  DEFAULT  0,
            mother TEXT DEFAULT mother,
            child TEXT DEFAULT child,
            date_OS TEXT DEFAULT date_OS,
            date_extension TEXT DEFAULT date_extension,
            price INTEGER DEFAULT 0,
            price_10 REAL DEFAULT 0.0
            )"""
tabl6 = """CREATE TABLE IF NOT EXISTS extension_month 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_count_not_null INTEGER DEFAULT 0,
            price_10_month REAL DEFAULT 0.0,
            date TEXT DEFAULT 0              
            )"""
drop_table = """DROP TABLE price_month"""
add = """INSERT INTO client ('nomer','message','elictronic_diary','mother','child',
'ade','soudrs','number_of_lession','praice') VALUES (79625422274,'зум','https://docs.google.com/spreadsheets/d/1klYRxjWN7OVC6rJc7-UHlYGgscIRRRFJdzvHxRMTPJM/edit#gid=0',
'Гузель','Тимур',4.1,'ц,щ,ч,л,р,рь',1,'not')
"""
update1 = """UPDATE client SET number_of_lession = 14.0 WHERE id = 15 """
delet = "DELETE FROM extension_month  WHERE id = 1"
update = """UPDATE client SET number_of_lession = 10.2 WHERE id = 6
"""
a = """ALTER TABLE client DROP COLUMN number_of_lession11 """
##f = func(conect,delet)

array_drop = ['DROP TABLE extension','DROP TABLE extension_month ']
array_add_table = [tabl5,tabl6]
def array_tabl_up(conect,array):
    for i in array:
        f =  func(conect,i)
#array_tabl_up(conect,array_drop)
array_tabl_up(conect,array_add_table)      








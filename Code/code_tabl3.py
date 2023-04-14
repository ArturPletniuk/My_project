import sqlite3
from sqlite3 import Error
from datetime import datetime
def tabl3(link):
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
    select = f"""SELECT DISTINCT(client_id) FROM client_day WHERE  date GLOB '*-{month_nay}-*' ORDER BY client_id"""
    f =  func(conect,select)
    ### сдесь мы выбираем все параметры для 3 таблицы
    for i in f:
        for j in i:    #  j это  номер client_id клиента в таблице 2
            nomer = f"""SELECT nomer FROM client_day WHERE client_id = {j} """
            nomer = value(conect,nomer)
            mother = f"""SELECT mother FROM client_day WHERE client_id = {j} """
            mother = value(conect,mother)
            #### тут остановились нужно сделать количество уроков чтоб считал только 0.2 
            ###  и когда поменяется прайс считал только целые и 0.2
            price = f"""SELECT SUM(D.price_lesson)  FROM client_day AS D JOIN client AS C ON
            D.client_id = C.id WHERE C.id = {j} AND D.date glob '*-{month_nay}-*'"""
            price = value(conect,price)
            praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
            D.client_id = C.id WHERE C.id = {j} AND D.date glob '*-{month_nay}-*'"""
            praice = func(conect,praice)
            praice_len = len(praice.fetchall())    ## это показывает есть ли два прайса в месяце
            if praice_len == 1:                     ## это если один прайс то количство уроков считается тут
                praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
            D.client_id = C.id WHERE C.id = {j} AND D.date glob '*-{month_nay}-*'"""
                praice = value(conect,praice)         
                if praice == "yes_50" or praice == "not_50":
                    number_of_lession = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                        D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*' AND D.number_of_lession GLOB '*2'"""
                    number_of_lession = value(conect,number_of_lession)
                else:
                    number_of_lession = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                        D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'""" 
                    number_of_lession = value(conect,number_of_lession)
            ### это код если в месяц был изменён прайс тоесть их теперь два у клиента в месяце
            elif praice_len > 1:
                pr = ''
                praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
            D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'"""
                praice = func(conect,praice)
                array = []
                for pra in praice:
                    for prai in pra:
                        array.append(prai)
                if (array[0] == "yes" and array[1] == "not") or (array[0] == "not" and array[1] == "yes"):
                    number_of_lession = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*' AND D.number_of_lession GLOB '*0'"""
                    number_of_lession = value(conect,number_of_lession)
                    praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'"""
                    praic = func(conect,praice)
                    praice = ''
                    for p in praic:
                        for ce in p:
                            praice += ce
                elif (array[0] == "yes_50" and array[1] == "not_50") or (array[0] == "not_50" and array[1] == "yes_50"):    
                    number_of_lession = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*' AND D.number_of_lession GLOB '*2'"""
                    number_of_lession = value(conect,number_of_lession)
                    praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'"""
                    praice = func(conect,praice)
                    praice = ''
                    for p in praic:
                        for ce in p:
                            praice += ce
                else: 
                    number_of_lession1 = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*' AND D.number_of_lession GLOB '*0'"""
                    number_of_lession1 = value(conect,number_of_lession1)
                    number_of_lession2 = f"""SELECT COUNT(D.number_of_lession)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*' AND D.number_of_lession GLOB '*2'"""
                    number_of_lession2 = value(conect,number_of_lession2)
                    number_of_lession =  number_of_lession1 + number_of_lession2
                    praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
                    D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'"""
                    praic = func(conect,praice)
                    praice = ''
                    for p in praic:
                        for ce in p:
                            praice += ce       
            else:
                praice = f"""SELECT DISTINCT(D.praice)  FROM client_day AS D JOIN client AS C ON
            D.client_id = C.id WHERE C.id = {j} AND D.date GLOB '*-{month_nay}-*'"""
                praice = value(conect,praice) 
            date_table3 = f"""SELECT COUNT(date) FROM client_month WHERE nomer = {nomer} AND date = '{daten}'""" 
            f = func(conect,date_table3)
            for i in f:
                for j in i:
                    date = j            
            if  date == 1:
                update_client = f"""UPDATE client_month SET nomer = {nomer}, mother = '{mother}',
                date = '{daten}', number_of_lession = {number_of_lession}, price_lesson = {price}, praice = '{praice}' WHERE
                nomer = {nomer} AND date = '{daten}'"""
                base = func(conect,update_client) 
            else:
                insert_client = f"""INSERT INTO client_month ('nomer','mother','date','number_of_lession','price_lesson','praice')
                    VALUES ('{nomer}','{mother}','{daten}','{number_of_lession}','{price}','{praice}')"""
                base = func(conect,insert_client) 

     



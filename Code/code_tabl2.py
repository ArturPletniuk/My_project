# здесь мы будем выполнять проверку наличия 2 условий: 1 это находятся ли 
# данные в таблице client, 2  не ходятся ла данные с такой же датай во второй таблице
# если эти два условия выполняются то мы добавляем в таблицу client этому клиенту +1 
# к столбцу урока или 0.1 соответственно  и производим расчёт урока и добавляем данные 
# в вторую таблицу

import sqlite3
from sqlite3 import Error
from dick_client import client_base
from nedel import ned
import re
def tabl2(link):
    conect = sqlite3.connect(link)
    def value(x):
        for i in x:
            for j in i:
                return j
    # функция проверки значений во второй таблице
    def nones(x):
        array = []
        for i in x:
            for j in i:
                array.append(j)
        for i in array:
            if i == None:
                return None
        return array            
    def func(conect,reqest):
        cursor =  conect.cursor()
        try:
            value = cursor.execute(reqest)
            conect.commit()
            #print("Подключение к базе данных SQLite прошло успешно")
        except Error as e:
            return f"Произошла ошибка {e}" 
        return value 
    price_not = [250,275,310,350]  # 250 = 1 - 9 урок,275 = 10 - 19, 310 = 20 - 33,350 = 34+
    price_yes = [180,200,225] # 180 = 1- 19, 200 = 20 - 33, 225 = 34+
    f = ned()
    dates = client_base(f) 
    for date in dates:                 # date это дата проведения урока
        for nomer in dates.get(date):     # nomer это номер клиента
            select = f"""SELECT nomer FROM client WHERE nomer = {nomer}"""
            select_client_day = f"""SELECT nomer FROM client_day WHERE nomer = {nomer} AND date = '{date}'"""
            f = func(conect,select)
            values = value(f)
            f1 = func(conect,select_client_day)
            values1 = nones(f1)
            # находятся ли данные в таблице client,не ходятся ла данные с такой же датай и номерам во второй таблице
            if values != None and values1 == []:
                client = f"SELECT praice FROM client WHERE nomer = {nomer}"
                f1 = func(conect,client)
                praice = value(f1) 
                ### это добавление  к целым урокам     
                if praice == 'yes' or praice == 'not':
                    lession = f"""UPDATE client SET number_of_lession = (SELECT number_of_lession FROM client WHERE nomer = {nomer}) + 1 WHERE nomer = {nomer} """
                    lession = func(conect,lession)
                elif praice == 'yes_50' or praice == 'not_50':
                    les = f'SELECT number_of_lession FROM client WHERE nomer = {nomer}'
                    ##### надо определять после запятой цифры в уроку чтобы правельно плюсовать
                    fq = func(conect,les)
                    rew = value(fq)
                    t = re.findall(r'\w+',str(rew))
                    if t[1] == '1':
                        l = f'SELECT number_of_lession FROM client WHERE nomer = {nomer}'
                        f1 = func(conect,l)
                        l = value(f1)
                        l = round(l + 0.1,1)
                        lession_50 = f"""UPDATE client SET number_of_lession = {l} WHERE nomer = {nomer} """
                        lession_50 = func(conect,lession_50)
                    elif t[1] == '2':
                        l = f'SELECT number_of_lession FROM client WHERE nomer = {nomer}'
                        f1 = func(conect,l)
                        l = value(f1)
                        l = round((l - 0.1)+1,1)
                        lession_50 = f"""UPDATE client SET number_of_lession = {l} WHERE nomer = {nomer} """
                        lession_50 = func(conect,lession_50)
            ######## код для расчета цены за урок#############################
                praice = f"""SELECT praice FROM client WHERE nomer = {nomer}"""
                lession = f"""SELECT number_of_lession FROM client WHERE nomer = {nomer}"""
                base = func(conect,praice)
                praice = value(base)
                lession = func(conect,lession)
                lession = value(lession)
                if (praice == 'not' or praice == "not_50") and (lession > 0 and lession < 10):
                    price = 250
                elif (praice == 'not' or praice == "not_50") and (lession > 9 and lession < 20):
                    price = 275
                elif (praice == 'not' or praice == "not_50") and (lession > 19 and lession < 34):
                    price = 310 
                elif (praice == 'not' or praice == "not_50") and lession >= 34 :
                    price = 350
                elif (praice == 'yes' or praice == "yes_50") and (lession > 0 and lession < 20):
                    price = 180 
                elif (praice == 'yes' or praice == "yes_50") and (lession > 19 and lession < 34):
                    price = 200 
                elif (praice == 'yes' or praice == "yes_50") and lession >= 34:
                    price = 225
                    #### разобраться в прайсах 
                mother = f"""SELECT mother FROM client WHERE nomer = {nomer}"""  ### имя матери
                base = func(conect,mother)
                mother = value(base)
                id = f"""SELECT id FROM client WHERE nomer = {nomer}"""     ### id матери
                base = func(conect,id)
                id = value(base) 
                ### добавление во вторую таблицу  
                if praice == "yes" or praice == "not":
                    update_client = f"""INSERT INTO client_day ('nomer','mother','date','number_of_lession','price_lesson','praice','client_id')
                    VALUES ('{nomer}','{mother}','{date}','{lession}','{price}','{praice}','{id}')"""
                    base = func(conect,update_client)
                if praice == 'not_50' or praice == "yes_50":
                    lessi = lession %  1
                    if round(lessi,1) == 0.2:
                        update_client = f"""INSERT INTO client_day ('nomer','mother','date','number_of_lession','price_lesson','praice','client_id')
                        VALUES ('{nomer}','{mother}','{date}','{lession}','{price}','{praice}','{id}')"""
                        base = func(conect,update_client)
                    elif round(lessi,1) == 0.1:
                        update_client = f"""INSERT INTO client_day ('nomer','mother','date','number_of_lession','price_lesson','praice','client_id')
                        VALUES ('{nomer}','{mother}','{date}','{lession}',0,'{praice}','{id}')"""
                        base = func(conect,update_client)   



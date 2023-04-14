from datetime import datetime
from tkinter import font
from tkinter import*
import tkinter.messagebox as box
import re
from Proect import parser
from nedel import ned
from dates_nedel import dates_nedel
from dick_client import client_base
from code_tabl2 import tabl2
from code_tabl3 import tabl3
from code_tabl4 import tabl4
import sqlite3
from sqlite3 import Error
import os           ####  Модуль для автоматического запуска файла
conect = sqlite3.connect('C:/Users/Olga/Desktop/Extension/baza.db')
class Aplication(Frame):
    """Инициализация атрибутов"""
    def __init__(self,master):
        super(Aplication,self).__init__(master)
        self.method()
        self.grid()
        self.link = 'C:/Users/Olga/Desktop/Extension/baza.db'
        self.otm = True
        self.date = ''
        self.year = datetime.now().year
        self.month = datetime.now().month
    def days(self,x):
        if int(x) < 10:
            return f"0{x}"
        else:
            return x    
    def func(self,conect,reqest,a = 0):
        cursor =  conect.cursor()
        try:
            value = cursor.execute(reqest)
            conect.commit()
            if a == 1:
                box.showinfo(title='SQLite',message='Клиент успешно добавлен в базу данных!')
        except Error as e:
            return f"Произошла ошибка {e}" 
        return value
    def extension_month(self):
        month = self.days(self.month)
        self.date += str(self.year) + '-'+ month
        date_extension_count = f"""SELECT COUNT(date_extension) FROM extension WHERE 
        date_extension GLOB '{self.date}*'"""
        date_extension_count = self.func(conect,date_extension_count).fetchone()[0]
        price_10_sum = f"""SELECT SUM(price_10) FROM extension WHERE 
        date_extension GLOB '{self.date}*'"""
        price_10_sum = self.func(conect,price_10_sum).fetchone()[0]
        id_extension_month = f"""SELECT EXISTS(SELECT id FROM extension_month WHERE date GLOB '{self.date}*')"""
        id_extension_month = self.func(conect,id_extension_month).fetchone()[0]
        if int(id_extension_month) > 0:
            id_extension_month = f"""SELECT id FROM extension_month WHERE date GLOB '{self.date}*'"""
            id_extension_month = self.func(conect,id_extension_month).fetchone()[0]
            extension_month = f"""UPDATE extension_month SET date_count_not_null = 
            {date_extension_count}, price_10_month = {price_10_sum} WHERE id = {int(id_extension_month)}"""
            extension_month = self.func(conect,extension_month)
            self.date = ''
        else:
            extension_month = f"""INSERT INTO extension_month ('date_count_not_null', 
            'price_10_month', 'date') VALUES ({date_extension_count},{price_10_sum},'{self.date}')"""
            extension_month = self.func(conect,extension_month)
            self.date = ''    
    def dismiss(self):
        self.window.destroy()
    def lebel_window(self,text,x,y):
            font_Menu = font.Font(family= "Arial", size=10, weight="bold", slant="roman")
            Label(self.window,text=f"{text}",font= font_Menu,).place(x=f"{x}",y=f"{y}")
    def client_extension(self):
        try:
            if int(self.insert_id_enter.get()):
                id = f'''SELECT COUNT(id) FROM client WHERE id = {int(self.insert_id_enter.get())}'''
                id = self.func(conect,id)
                if id.fetchone()[0] == 1:
                    if self.favorite.get() == "client":
                        client = f'''SELECT nomer,mother,child FROM client WHERE id = {int(self.insert_id_enter.get())}'''
                        f = self.func(conect,client)
                        client = ''
                        for i in f:
                            for j in i:
                                client += str(j) + ' '
                        box.showinfo(title='client',message=f'{client}')
                    elif self.favorite.get() == "extension":
                        client = f'''SELECT nomer,mother,child,date_OS,date_extension,price,price_10
                          FROM extension WHERE id = {int(self.insert_id_enter.get())}'''
                        f = self.func(conect,client)
                        client = ''
                        for i in f:
                            for j in i:
                                client += str(j) + ' '    
                        box.showinfo(title='extension',message=f'{client}') 
                    else:
                        box.showerror(title='Ошибка',message='Вы не выбрали таблицу!')    
                else:
                    box.showerror(title='Ошибка',message='Такого клиента нет в вашей базе!')
        except ValueError:
            box.showerror(title='Ошибка',message='В поле ID должно быть только целое число')         
    def client_extension_insert(self):
        try:
            if int(self.insert_id_enter.get()):
                id = f'''SELECT COUNT(id) FROM client WHERE id = {int(self.insert_id_enter.get())}'''
                id = self.func(conect,id)
                if id.fetchone()[0] == 1:
                    if self.favorite.get() == "client":
                        date_OS = 'date_OS'
                        date_extension = 'date_extension'
                        price = 0
                        if self.insert_date_os.get():
                            match = re.fullmatch(r'\d\d\d\d\-\d\d\-\d\d',self.insert_date_os.get())
                            if match:
                                date_OS = self.insert_date_os.get()
                            else:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nФорма должна быть в виде 0000-00-00') 
                        if self.insert_date_extension.get():
                            match = re.fullmatch(r'\d\d\d\d\-\d\d\-\d\d',self.insert_date_extension.get())
                            if match:
                                date_extension = self.insert_date_extension.get()
                            else:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nФорма должна быть в виде 0000-00-00')
                        if self.insert_price.get():
                            try:
                                price = int(self.insert_price.get())
                                if price < 0:
                                    price *= -1  
                            except ValueError:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nЦена должна состоять только из целых цифр.')
                        price_10 = ('%.1f' %(price / 10))
                        nomer = f"""SELECT nomer FROM client WHERE id ={int(self.insert_id_enter.get())}""" 
                        nomer = self.func(conect,nomer).fetchone()[0]
                        mother = f"""SELECT mother FROM client WHERE id ={int(self.insert_id_enter.get())}""" 
                        mother = self.func(conect,mother).fetchone()[0]
                        child = f"""SELECT child FROM client WHERE id ={int(self.insert_id_enter.get())}""" 
                        child = self.func(conect,child).fetchone()[0]
                        insert = f"""INSERT INTO extension ('nomer','mother','child',
                        'date_OS','date_extension','price','price_10') 
                        VALUES ({nomer},'{mother}','{child}','{date_OS}','{date_extension}'
                        ,{price},{price_10})"""
                        insert = self.func(conect,insert)
                        self.extension_month()
                        box.showinfo(title='extension',message="Данные успешно добавлены в таблицу 'extension'")        
                    elif self.favorite.get() == "extension":
                        box.showerror(title='Ошибка',message='Вы выбрали  не таблицу client!')
                    else:
                        box.showerror(title='Ошибка',message='Вы не выбрали таблицу!')     
                else:
                    box.showerror(title='Ошибка',message='Такого клиента нет в вашей базе!')
        except ValueError:
            box.showerror(title='Ошибка',message='В поле ID должно быть только целое число')
    def delete_extension(self):
        try:
            if int(self.insert_id_enter.get()):
                id = f'''SELECT COUNT(id) FROM extension WHERE id = {int(self.insert_id_enter.get())}'''
                id = self.func(conect,id)
                if id.fetchone()[0] == 1:
                    if self.favorite.get() == "extension":
                        delet = f"""DELETE FROM extension WHERE id = {int(self.insert_id_enter.get())}"""
                        delet = self.func(conect,delet)
                        self.extension_month()
                        box.showinfo(title='extension',message="Данные из таблицы 'extension' успешно удалены.") 
                    else:
                        box.showerror(title='Ошибка',message="Вы выбрали не таблицу 'extension'")
                else:
                    box.showerror(title='Ошибка',message="Такого клиента нет в таблице 'extension'")
            else:
                box.showerror(title='Ошибка',message="Вы не ввели ID")
        except ValueError:
            box.showerror(title='Ошибка',message='В поле ID должно быть только целое число')            
    def update_extension(self):
        try:
            if int(self.insert_id_enter.get()):
                id = f'''SELECT COUNT(id) FROM extension WHERE id = {int(self.insert_id_enter.get())}'''
                id = self.func(conect,id)
                if id.fetchone()[0] == 1: 
                    if self.favorite.get() == "extension":       
                        date_OS = f"""SELECT date_OS FROM extension WHERE id ={int(self.insert_id_enter.get())}""" 
                        date_OS = self.func(conect,date_OS).fetchone()[0]
                        date_extension = f"""SELECT date_extension FROM extension WHERE id ={int(self.insert_id_enter.get())}""" 
                        date_extension = self.func(conect,date_extension).fetchone()[0]
                        price = f"""SELECT price FROM extension WHERE id ={int(self.insert_id_enter.get())}""" 
                        price = self.func(conect,price).fetchone()[0]
                        if self.insert_date_os.get():
                            match = re.fullmatch(r'\d\d\d\d\-\d\d\-\d\d',self.insert_date_os.get())
                            if match:
                                date_OS = self.insert_date_os.get()
                            else:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nФорма должна быть в виде 0000-00-00') 
                        if self.insert_date_extension.get():
                            match = re.fullmatch(r'\d\d\d\d\-\d\d\-\d\d',self.insert_date_extension.get())
                            if match:
                                date_extension = self.insert_date_extension.get()
                            else:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nФорма должна быть в виде 0000-00-00')
                        if self.insert_price.get():
                            try:
                                price = int(self.insert_price.get())
                                if price < 0:
                                    price *= -1  
                            except ValueError:
                                return box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nЦена должна состоять только из целых цифр.')
                        price_10 = ('%.1f' %(price / 10))
                        update_extensio = f"""UPDATE extension SET date_OS = '{date_OS}', 
                        date_extension = '{date_extension}', price = {int(price)}, price_10 = {price_10} WHERE
                        id = {int(self.insert_id_enter.get())}"""
                        update_extensio = self.func(conect,update_extensio)
                        self.extension_month()
                        return box.showinfo(title='extension',message="Данные из таблицы 'extension' успешно изменены и изменена таблица 'extension_month'.") 
                    else:
                        box.showerror(title='Ошибка',message="Вы выбрали не таблицу 'extension'")
                else:
                    box.showerror(title='Ошибка',message="Такого клиента нет в таблице 'extension'")
            else:
                box.showerror(title='Ошибка',message="Вы не ввели ID")
        except ValueError:
            box.showerror(title='Ошибка',message='В поле ID должно быть только целое число') 
    def click(self):
        self.window = Toplevel()
        self.window.title("Продления клиентов")
        self.window.geometry("900x600+400+50")
        self.window.resizable(False,False)
### Переключатели 
        self.favorite = StringVar()
        self.favorite.set(None)
        self.pon = Radiobutton(self.window,text="Client",variable= self.favorite,value="client",\
        command=  self.favorite,font='Algerian 12').place(x=480,y=50)
        Radiobutton(self.window,text="Extension",variable= self.favorite,value="extension",\
        command=  self.favorite,font='Algerian 12').place(x=250,y=50)
##### Добавить клиента в продлении        
        font_button = font.Font(family= "Arial", size=14, weight="bold", slant="roman")
        Button(self.window,text="Добавить клиента",cursor='hand2',command= self.client_extension_insert,background ='turquoise',fg='black',font=font_button,width=15,height=2).\
        grid(row=2,column=1,sticky=W,padx = 110,pady=230)
        Label(self.window,text="Продления клиентов",font='Forte 18' ).place(x=300,y=5)
        Label(self.window,text="Введите ID клиента:",font= 'Algerian 19').place(x=70,y=100)
        self.insert_id_enter = Entry(self.window,font='arial 18',width=15)
        self.insert_id_enter.place(x=320,y=100)
        Button(self.window,text="Показать клиента",cursor='hand2',command= self.client_extension,background ='lime',fg='black',font=font_button).\
        place(x = 540,y = 96)
        self.lebel_window('id',410,135)
        self.insert_date_os = Entry(self.window,font='arial 18',width=15)
        self.insert_date_os.place(y=160,x=102)
        self.insert_date_extension = Entry(self.window,font='arial 18',width=15)
        self.insert_date_extension.place(y=160,x=320)
        self.insert_price = Entry(self.window,font='arial 18',width=15)
        self.insert_price.place(y=160,x=538)
        self.lebel_window('date_os',174,193)
        self.lebel_window('date_extension',380,193)
        self.lebel_window('price',610,193)
### удалить клиента в продлении
        Button(self.window,cursor="X_cursor",text="Удалить клиента",command= self.delete_extension,background ='red',fg='black',font=font_button,width=15,height=2).\
        place(y=230,x=325)

##### Обновить клиента в продлении        
        font_button = font.Font(family= "Arial", size=14, weight="bold", slant="roman")
        Button(self.window,text="Обновить клиента",cursor='hand2',command= self.update_extension,background ='turquoise',fg='black',font=font_button,width=15,height=2).\
        grid(row=2,column=1,sticky=W,padx = 540,pady=50)
        Button(self.window,text="Выход",cursor='hand2',command= self.dismiss,background ='red',fg='black',font=font_button).\
        place(y=380,x=370)
        self.window.grab_set()       # захватываем пользовательский ввод      
    def lebel(self,text,x,y):
            font_Menu = font.Font(family= "Arial", size=10, weight="bold", slant="roman")
            Label(text=f"{text}",font= font_Menu,).place(x=f"{x}",y=f"{y}")    
    def method(self):
###### основные надписи ####
        font_Menu = font.Font(family= "Arial", size=18, weight="bold", slant="roman")
        Label(text="Введите дату:",font= font_Menu).place(x=10,y=12)
        font_Menu = font.Font(family= "Arial", size=9, weight="bold", slant="roman")
        Label(text="Формат ввода 'хххх-хх-хх'(2023-02-23)",font= font_Menu).place(x=198,y=52)
        self.date = Entry(self,font='arial 20',width=15)
        self.date.grid(row=1,column=1,sticky=W,padx = 200,pady=11)
        font_button = font.Font(family= "Arial", size=14, weight="bold", slant="roman")
        Button(self,text="OK",cursor='hand2',command= self.reveal,background ='lime',fg='black',font=font_button).\
        grid(row=1,column=1,sticky=W,padx = 440,pady=11)
        #### токстовые поля для добавления клиента
        Button(self,text="Добавить\nклиента",cursor='hand2',command= self.add_button,background ='turquoise',fg='black',font=font_button,width=13,height=6).\
        grid(row=2,column=1,sticky=W,padx = 10,pady=40)
        self.add_nomer = Entry(self,font='arial 18',width=15)
        self.add_nomer.place(y=100,x=180)
        self.add_message = Entry(self,font='arial 18',width=15)
        self.add_message.place(y=100,x=390)
        self.add_el = Entry(self,font='arial 18',width=15)
        self.add_el.place(y=100,x=600)
        self.add_mother = Entry(self,font='arial 18',width=15)
        self.add_mother.place(y=160,x=180)
        self.add_child = Entry(self,font='arial 18',width=15)
        self.add_child.place(y=160,x=390)
        self.add_age = Entry(self,font='arial 18',width=15)
        self.add_age.place(y=160,x=600)
        self.add_sourds= Entry(self,font='arial 18',width=15)
        self.add_sourds.place(y=220,x=180)
        self.add_praice= Entry(self,font='arial 18',width=15)
        self.add_praice.place(y=220,x=390)
        self.add_number_of_lession= Entry(self,font='arial 18',width=15)
        self.add_number_of_lession.place(y=220,x=600)
        self.lebel('nomer',245,132)
        self.lebel('message',440,132)
        self.lebel('electronic_diary',630,132)
        self.lebel('mother',245,195)
        self.lebel('child',450,195)
        self.lebel('age',660,195)
        self.lebel('soudrs',245,255)
        self.lebel('praice',450,255)
        self.lebel('number_of_lession',630,255)
        ### удалить клиента
        Button(self,cursor="X_cursor",text="Удалить клиента",command= self.delete,background ='red',fg='black',font='arial 14',width=14).\
        grid(row=3,column=1,sticky=W,padx = 10,pady=0)
        Button(self,text="Показать клиента",cursor='hand2', command= self.client_show_dalet,background ='lime',fg='black',font=font_button).\
        grid(row=3,column=1,sticky=W,padx = 395,pady=0)
        self.delete_nomer = Entry(self,font='arial 18',width=15)
        self.delete_nomer.grid(row=3,column=1,sticky=W,padx = 180,pady=0)
        self.lebel('nomer',245,325)
        ### обновить клиента
        Button(self,text="Обновить\nклиента",cursor='hand2',command= self.update_button,background ='turquoise',fg='black',font=font_button,width=13,height=6).\
        grid(row=4,column=1,sticky=W,padx = 10,pady=50)
        font_Menu = font.Font(family= "Arial", size=12, weight="bold", slant="roman")
        Label(text="Введите номер клиента:",font= font_Menu).place(x=180,y=380)
        self.update_nomer = Entry(self,font='arial 18',width=15)
        self.update_nomer.place(y=378,x=393)
        Button(self,text="Показать клиента",cursor='hand2',command= self.client_show_update,background ='lime',fg='black',font=font_button).\
        place(x = 600,y = 375)
        self.update_message_enter = Entry(self,font='arial 18',width=15)
        self.update_message_enter.place(y=420,x=180)
        self.update_elictronic_diary_enter = Entry(self,font='arial 18',width=15)
        self.update_elictronic_diary_enter.place(y=420,x=390)
        self.update_age_enter = Entry(self,font='arial 18',width=15)
        self.update_age_enter.place(y=420,x=600)
        self.update_soudrs_enter = Entry(self,font='arial 18',width=15)
        self.update_soudrs_enter.place(y=475,x=180)
        self.update_praice_enter = Entry(self,font='arial 18',width=15)
        self.update_praice_enter.place(y=475,x=390)
        self.update_number_of_lession_enter = Entry(self,font='arial 18',width=15)
        self.update_number_of_lession_enter.place(y=475,x=600)
        self.lebel('message',240,452)
        self.lebel('electronic_diary',430,452)
        self.lebel('age',670,452)
        self.lebel('soudrs',250,506)
        self.lebel('praice',450,506)
        self.lebel('number_of_lession',630,506)
    ### Показать базу
        Button(self,text="Показать базу",cursor='hand2',command= self.base,background ='lime',fg='black',font=font_button).\
        grid(row=5,column=1,sticky=W,padx = 100,pady=20) 
        Button(self,text="Выход",cursor='hand2',command= self.exit,background ='red',fg='black',font=font_button).\
        grid(row=5,column=1,sticky=W,padx = 600,pady=20)
        Button(self,text="Продление",cursor='hand2',command= self.click,background ='lime',fg='black',font=font_button).\
        grid(row=5,column=1,sticky=W,padx = 340,pady=20)  
    def exit(self):
        os._exit(1)
    def client_show_dalet(self):
        try:
            show = int(self.delete_nomer.get())
            if show < 0:
                show *= -1
            select = f"""SELECT nomer,mother,child,ade FROM client WHERE nomer = {show} """ 
            f = self.func(conect,select)
            select = ''
            for i in f:
                for j in i:
                    select += str(j) + ' ' 
            prov = f'SELECT EXISTS(SELECT nomer FROM client WHERE nomer = {show})' 
            prov = self.func(conect,prov)
            if prov.fetchone()[0] != 0:       
                box.showinfo(title='SQLite',message=f'Вот клиент которого вы хотите удалить - \n{select}') 
            else:
                box.showwarning(title='SQLite',message=f'Такого клиента нет в вашей базе!')
        except ValueError:
            box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nНомер должен состоять только из целых цифр.')  
    def base(self):
        os.startfile(r'C:/Users/Olga/Desktop/Extension/baza.db') ## Автоматически откра=ывает файл
    def client_show_update(self):    
        try:
            show = int(self.update_nomer.get())
            if show < 0:
                show *= -1
            select = f"""SELECT nomer,message,mother,child,ade,soudrs,number_of_lession,praice FROM client WHERE nomer = {show} """ 
            f = self.func(conect,select)
            select = ''
            for i in f:
                for j in i:
                    select += str(j) + ' ' 
            prov = f'SELECT EXISTS(SELECT nomer FROM client WHERE nomer = {show})' 
            prov = self.func(conect,prov)
            if prov.fetchone()[0] != 0:       
                box.showinfo(title='SQLite',message=f'Вот клиент которого вы хотите обновить - \n{select}') 
                self.nomer_select = show
            else:
                box.showwarning(title='SQLite',message=f'Такого клиента нет в вашей базе!')
        except ValueError:
            box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nНомер должен состоять только из целых цифр.')  
    def update_button(self):
        error = 1
        message = f'SELECT message FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,message)
        message = f.fetchone()[0]
        elictronic_diary = f'SELECT elictronic_diary FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,elictronic_diary)
        elictronic_diary = f.fetchone()[0]
        age = f'SELECT ade FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,age)
        age = f.fetchone()[0]
        sourds = f'SELECT soudrs FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,sourds)
        sourds = f.fetchone()[0]
        praice = f'SELECT praice FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,praice)
        praice = f.fetchone()[0]
        number_of_lession = f'SELECT number_of_lession FROM client WHERE nomer = {self.nomer_select}'
        f = self.func(conect,number_of_lession)
        number_of_lession = f.fetchone()[0]
        if self.update_message_enter.get():
            message = self.update_message_enter.get()
        if self.update_elictronic_diary_enter.get():
            elictronic_diary = self.update_elictronic_diary_enter.get()   
        if self.update_age_enter.get():
            age = self.update_age_enter.get()
            try:
                age = float(self.update_age_enter.get())
                if age < 0:
                    age *= -1  
            except ValueError:
                error = 0
                box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nВозраст должен быть только вещественным числом (5.6).') 
        if self.update_soudrs_enter.get():
            sourds = self.update_soudrs_enter.get()
        if self.update_praice_enter.get():
            praice_array = ['yes','not','yes_50','not_50']
            praice  = self.update_praice_enter.get()
            if praice not in praice_array: 
                error = 0      
                box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nПрайс может  быть только 'yes, not, yes_50, not_50'.") 
        if  self.update_number_of_lession_enter.get():
            try:
                number_of_lession = float(self.update_number_of_lession_enter.get()) 
                t = re.findall(r'\w+',str(number_of_lession))
                if t[1] == '1' or t[1] == '2' or t[1] == '0': 
                    if number_of_lession < 0:
                        number_of_lession *= -1
                else:
                    error = 0
                    box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nУрок должен быть либо целым числом либо заканчиватся только на 0.1 или 0.2.")   
            except:
                error = 0        
                box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nУрок должен быть либо целым числом либо заканчиватся только на 0.1 или 0.2.")
        if error != 0:
            try:   
                update = f"""UPDATE client SET message = '{message}',
                elictronic_diary = '{elictronic_diary}',ade = {age},soudrs = '{sourds}',
                praice = '{praice}',number_of_lession = {number_of_lession} WHERE nomer = {self.nomer_select}"""
                f = self.func(conect,update)
                box.showinfo(title='SQLite',message=f'Клиент с номером {self.nomer_select} успешно обновлён.')
            except:
                box.showwarning(title='SQLite',message=f'Вы не выбрали номер в вашей базе!')   
    def delete(self):
        try:
            nomer = int(self.delete_nomer.get())
            select = f"""SELECT nomer,mother,child,ade FROM client WHERE nomer = {nomer} """ 
            f = self.func(conect,select)
            select = ''
            for i in f:
                for j in i:
                    select += str(j) + ' ' 
            nomer = int(self.delete_nomer.get())
            if nomer < 0:
                nomer *= -1
            prov = f'SELECT EXISTS(SELECT nomer FROM client WHERE nomer = {nomer})' 
            prov = self.func(conect,prov)
            if prov.fetchone()[0] != 0:       
                delete = f"""DELETE FROM client WHERE nomer = {nomer}"""
                self.func(conect,delete)
                box.showinfo(title='SQLite',message=f'Клиент {select} успешно удалён из вашей базы')    
            else:
                box.showwarning(title='SQLite',message=f'Такого клиента нет в вашей базе!')
        except ValueError:
            box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nНомер должен состоять только из целых цифр.')            
    def add_button(self):
        error = 1
        nomer = 9999999999
        message = 'message'
        el = 'https'
        mother = 'mother'
        child = 'child'
        age = 0
        sourds = 'abcde'
        praice = 'praice'
        number_of_lession = 0
        if self.add_nomer.get():
            try:
                nomer = int(self.add_nomer.get())
                if nomer < 0:
                    nomer *= -1
            except ValueError:
                error = 0 
                box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nНомер должен состоять только из целых цифр.')     
        if self.add_message.get():
            message = self.add_message.get()
        if self.add_el.get():
            el = self.add_el.get()
        if self.add_mother.get():
            mother = self.add_mother.get()
        if self.add_child.get():
            child = self.add_child.get()
        if self.add_age.get():
            try:
                age = float(self.add_age.get())
                if age < 0:
                    age *= -1   
            except ValueError:
                error = 0 
                box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!\nВозраст должен быть только вещественным числом (5.6).')  
        if self.add_sourds.get():
            sourds = self.add_sourds.get()
        if self.add_praice.get():
            praice_array = ['yes','not','yes_50','not_50']
            praice = self.add_praice.get()
            if praice not in praice_array:
                error = 0         
                box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nПрайс может  быть только 'yes, not, yes_50, not_50'.")  
            praice = self.add_praice.get()
        if self.add_number_of_lession.get():
            try:
                number_of_lession = float(self.add_number_of_lession.get()) 
                t = re.findall(r'\w+',str(number_of_lession))
                if t[1] == '1' or t[1] == '2' or t[1] == '0': 
                    if number_of_lession < 0:
                        number_of_lession *= -1
                else:
                    error = 0 
                    box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nУрок должен быть либо целым числом либо заканчиватся только на 0.1 или 0.2.")
            except:
                error = 0        
                box.showerror(title='Ошибка!!!',message="Не верный формат ввода!!!\nУрок должен быть либо целым числом либо заканчиватся только на 0.1 или 0.2.")                          
        if error != 0:
            add = f"""INSERT INTO client ('nomer','message','elictronic_diary','mother','child',
    'ade','soudrs','praice','number_of_lession') VALUES ({nomer},'{message}','{el}',
    '{mother}','{child}',{age},'{sourds}','{praice}',{number_of_lession})"""
            self.func(conect,add,1)
    def reveal(self): 
        conten = self.date.get()
        match = re.fullmatch(r'\d\d\d\d\-\d\d\-\d\d',conten)
        if match: 
            parser(conten)
            f = ned()
            d = dates_nedel()
            c = client_base(f)
            t2 = tabl2(self.link)   ### ссылка на нашу базу прописываем путь к ней
            t3 = tabl3(self.link)
            t4 = tabl4(self.link)
            box.showinfo(title='Готово!!!',message="Программа завершила скачавание данных! Можете посмотреть результаты.") 
        else:
            box.showerror(title='Ошибка!!!',message='Не верный формат ввода!!!')    
##### основная часть ####### 
def main():        
    root = Tk()
    root.title("Расчёт зарплаты!")
    root.geometry("900x700+400+50")
    root.resizable(False,False)        ### фиксирует окно
    app = Aplication(root)
    app.mainloop()
main()     
## log = xxxxxxxx  -  здесь нужен логин
## password = xxxxxxxxx  -  пароль
### этот модуль парсит клиентов с + и записует в файл sw_templates.json
import json
from selenium import webdriver ## В настоящее время поддерживаются реализации WebDriver: Firefox, Chrome, IE и Remote
from selenium.webdriver.common.keys import Keys ## Класс Keys предоставляет клавиши на клавиатуре, такие как RETURN, F1, ALT и т. д.
from selenium.webdriver.common.by import By ## Класс By используется для поиска элементов в документе.
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.color import Color
import tkinter.messagebox as box
from selenium.webdriver.common.action_chains import ActionChains
def parser(daten):
    driver = webdriver.Chrome()  ## здесь мы выбираем браузер которым будем пользоваться и который установлен у нас
    try:
        url2 = 'https://www.yclients.com/'
        driver.get(url2)
        er = driver.find_element(By.XPATH,'//*[@id="mob-header"]/div[2]/div[3]/a[2]')
        er.send_keys(Keys.ENTER) ## нажимаем на кнопку
        sleep(10)
        driver.switch_to.window(driver.window_handles[1])
        elem = driver.find_element(By.XPATH,'//*[@id="onboarding"]/div[2]/div/div/form/div[2]/div[1]/div[1]/input') ## находим место для ввода
        elem1 = driver.find_element(By.XPATH,'//*[@id="onboarding"]/div[2]/div/div/form/div[2]/div[2]/div[1]/input')
        elem3 = driver.find_element(By.XPATH,'//*[@id="onboarding"]/div[2]/div/div/form/div[3]/button')
        elem.send_keys("375336441425") ##  имитируем ввод текста
        elem1.send_keys("tja852Gomola") 
        sleep(3)
        elem3.send_keys(Keys.RETURN) ## нажимаем на кнопку
        sleep(15)
        u = f"https://yclients.com/timetable/552042?#mode=0&main_date={daten}&master_id=2163320"
        driver.get(u)
        ### функция вызывает полноэкранный режим 
        driver.fullscreen_window() 
        sleep(10)
        button_plus = driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[4]/span/div/div[1]/button/span[2]/i')                                                     
        action = ActionChains(driver)
        action.click(on_element =  button_plus)
        action.perform()
        button_uvelich = driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[4]/span/div/div[2]/div/input')
        action = ActionChains(driver)   
        action.click(on_element = button_uvelich)
        action.perform()
        sleep(5)
        ## data по сути это список и мы можем обращатся к любому элементу
        vse = []
        list_date = []
        d = {}
        name_client_color = driver.find_elements(By.CLASS_NAME,'y-timetable-record-preview__protected_phone.y-timetable-record-preview__protected_phone_redesign')  
        sleep(2)
        name_client_vse1 = driver.find_elements(By.CSS_SELECTOR,'div.y-timetable-records-container')
        sleep(2)
        yer = driver.find_element(By.XPATH,'/html/body/nav/div/ul/li[3]/div/div/div/div/span[2]')
        sleep(2)
        date = driver.find_element(By.XPATH,'//*[@id="page-wrapper"]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/strong')
        sleep(2)
        list_date.append(date.text)
        list_date.append(yer.text)
        score = 0
        for i in name_client_color:
            score += 1
            col = Color.from_string(i.value_of_css_property("Color"))
            d[str(score) + '.' + i.text] = col.hex
        with open('color.json', 'w') as f:
            json.dump(d,f,ensure_ascii=False)  ## для кодировки в нормальный формат json
        for i in name_client_vse1:
            vse.append(i.text)
        with open('vse.json', 'w') as f:
            json.dump(vse,f,ensure_ascii=False)  ## для кодировки в нормальный формат json
        with open('date.json', 'w') as f:
            json.dump(list_date,f,ensure_ascii=False)  
    except Exception as e:
         driver.quit()                          
         box.showerror(title='Произошла ошибка!!!',message= 'Выбраная вами дата не найдена на сайте!!')              
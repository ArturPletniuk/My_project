## этот модуль возвращает список в котором подсчитано количество уроков по каждому дню [1,2,3] - понедельник 1 урок и т д
import json
import re
def list_day():
    with open('vse.json') as f:
            file_content = f.read()
    dates = json.loads(file_content)
    array = []
    for i in dates:
            r = re.findall(r'[+]\d+',i)
            array.append(r)
    day = []      
    for  i in range(7):
            d = len(array[i])
            day.append(d)
    return day     
       
        

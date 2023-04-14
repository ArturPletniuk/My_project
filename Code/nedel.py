# по цвету выбирает проведенные уроки оставляя последовательность дней их проведения в списке
# в итоге мы получаем список с проведенными уроками отсортированными по индексу
import json
import re 
from day_nedel import list_day
def ned():
    list_d = list_day()
    array = []
    d1 = {}
    with open('color.json') as f:
        file_content = f.read()
    color_novi = json.loads(file_content)
    score = 0
    scores = 0
    for i in color_novi:
        scores+=1
        if scores == len(color_novi):
            d1[i] = color_novi[i]
            array.append(d1)
        else:    
            if len(d1.keys()) < list_d[score]:
                d1[i] = color_novi[i]       
            else:
                array.append(d1)
                d1 = {}
                d1[i] = color_novi[i] 
                score += 1   
### код рабочий             
    array1 = []        
    for i in range(7):
        array1.append(array[i])  
    q = []
    ar = []
    c = "#854e0e"
    for i in array1:
        for j in i:
            if i[j] == c:
                r = re.findall(r'[+]\w+',j)
                q.append("".join(r))
        ar.append(q)
        q = [] 
    return ar





          


        


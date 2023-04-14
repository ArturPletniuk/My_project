## сдесь модуль берёт дату и делает список дат на неделю
from datetime import datetime
from calendar import monthrange
import json
import re
def dates_nedel():
    with open('date.json') as f:
        file_content = f.read()   
    dates = json.loads(file_content)
    current_year = datetime.now().year
    def days(x):
        if int(x) < 10:
            return f"0{x}"
        else:
            return x
    mon = {"сен":9,"окт":10,"ноя":11,"дек":12,"янв":1,"фев":2,"мар":3,"апр":4,
    "май":5,"июн":6,"июл":7,"авг":8}
    year = dates[1]  ## это чистый год
    date = dates[0]
    day = "".join(re.findall(r'^\w+',date))   ## это чистый день с начала недели
    mont = "".join(re.findall(r'\w+$',date))
    for i in mon:
        if i == mont:
            month = mon[i]                   ## это номер месяца
    days_v_month = monthrange(current_year, month)[1]  ## это количество дней в текущем месяце
    array_day = []
    score = int(day)
    year_score = int(year) +1
    if month >= 10:
        nov_month = month + 1
    else:
        nov_month = f'0{month + 1}'
        month = f"0{month}"
    if int(day) >= 23:
        for i in range(7):
            if score <= days_v_month:
                da = days(score)
                mon = days(month)
                daten = f'{year}-{month}-{da}'
                array_day.append(daten)
                score += 1
            else:
                if int(month) < 12:
                    da = days(1)
                    daten = f'{year}-{nov_month}-{da}'
                    array_day.append(daten)
                    score = 2
                    month = nov_month
                else:
                    daten = f'{year_score}-01-01'
                    array_day.append(daten)
                    year = year_score
                    month = '01'
                    score = 2     
    else:
        for i in range(7):
            da = days(score)
            daten = f'{year}-{month}-{da}'
            array_day.append(daten)
            score += 1
    return array_day

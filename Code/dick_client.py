## получить словарь в котором ключем является номер  а значением дата его проведения
from dates_nedel import dates_nedel
def client_base(x):
    date = dates_nedel()
    client_dickt = {}
    score = 0
    for i in x:
        if i != []:
            client_dickt[date[score]] = i
        score += 1 
    return client_dickt       

      
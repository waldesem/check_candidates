import datetime as dt
import httpx
import sqlite3
import menu_upload

# проверка по списку самозанятых
def check_npd_status(inn: str, req_date: dt.date) -> dict:
    #req_date = dt.date.today().isoformat()
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    data = {
        "inn": inn,
        "requestDate": req_date,
    }
    resp = httpx.post(url=url, json=data)
    return resp.json()

# проверка инн
def suggest(surname: str, name: str, patronymic: str, birthdate: str,
            doctype: str, docnumber: str, docdate: str) -> dict:
    url = "https://service.nalog.ru/inn-proc.do"
    data = {
        "fam": surname,
        "nam": name,
        "otch": patronymic,
        "bdate": birthdate,
        "bplace": "",
        "doctype": doctype,
        "docno": docnumber,
        "docdt": docdate,
        "c": "innMy",
        "captcha": "",
        "captchaToken": "",
    }
    resp = httpx.post(url=url, data=data)
    return resp.json()

# запрос в SQLite
def db_response(connect, query, resp, noresp):
    try:
        sqlite_connection = sqlite3.connect(connect)
        cursor_obj = sqlite_connection.cursor()
        cursor_obj.execute(query)
        record = cursor_obj.fetchall()
        if len(record) != 0:
            resp_db = resp
        else:
            resp_db = noresp
        cursor_obj.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return resp_db

def check():
    # создаем список для результатов проверки
    global response_check
    response_check = []
    
    # проверка самозанятого
    npd_response = check_npd_status(menu_upload.anketa_values[11], dt.date.today().isoformat())
    response_check.append(npd_response.get('message'))
    
    # проверка инн
    document = {'passport_foreign': '10', 'residence_permit': '12', 'passport_russia': '21'}
    inn_response = suggest(
        surname=menu_upload.anketa_values[2].split()[0],
        name=menu_upload.anketa_values[2].split()[1],
        patronymic=menu_upload.anketa_values[2].split()[2],
        birthdate=menu_upload.anketa_values[4],
        doctype=document.get('passport_russia'),
        docnumber=menu_upload.anketa_values[7][:2] + ' ' + menu_upload.anketa_values[7][2:] + ' ' + menu_upload.anketa_values[8],
        docdate=menu_upload.anketa_values[9])
    response_check.append(inn_response.get('inn'))
    
    # проверка по собственной Базе данных
    fio = menu_upload.anketa_values[2]
    dr = menu_upload.anketa_values[4]
    #dr = dt.datetime.strftime(birthday, '%d.%m.%Y')
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/kandidates.db'
    query = "SELECT * FROM Candidates WHERE ФИО like " + "'" + fio + "'" + ' and Датарождения like ' + "'" + dr + "'"
    resp = 'Найдены полные совпадения в Базе данных по ФИО и дате рождения'
    noresp = 'Не найдены совпадения в списке Базе данных (возможно совпадение по ФИО)'
    candidates_response = db_response(connect, query, resp, noresp)
    response_check.append(candidates_response)
    
    # проверка по списку Дисквалификации
    fio = str(menu_upload.anketa_values[2]).upper()
    dr = str(menu_upload.anketa_values[3])
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/disqual_db.db'
    query = "SELECT * FROM disqual_fns WHERE G2 like " + "'" + fio + "'" + ' and G3 like ' + "'" + dr + "'"
    resp = 'Найден в списке дисквалифицированных лиц'
    noresp = 'Отсутствует в списке дисквалифицированных лиц'
    response_disqual = db_response(connect, query, resp, noresp)
    response_check.append(response_disqual)
    
    # проверка по списку Недействительных паспортов
    connect = '/home/semenenko/Загрузки/passportDB.db'
    query = 'SELECT * FROM list_of_expired_passports WHERE PASSP_SERIES = ' + str(
                menu_upload.anketa_values[7]) + ' and PASSP_NUMBER = ' + str(menu_upload.anketa_values[8])
    resp = 'Найден в списке недействительных паспортов'
    noresp = 'В списке недействительных паспортов не найден'
    passport_response = db_response(connect, query, resp, noresp)
    response_check.append(passport_response)
    
    return response_check

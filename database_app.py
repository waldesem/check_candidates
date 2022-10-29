from tkinter import Toplevel, StringVar, Frame, Scrollbar
from app_window import MainWindow
import sqlite3

# columns = ['id', 'Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения', 'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН', 'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование', 'Период работы на 1-м МР', '1-е место работы', 'Проверка 1-го места работы', 'Период работы на 2-м МР', '2-е место работы', 'Проверка 2-го места работы', 'Период работы на 3-м МР', '3-е место работы', 'Проверка 3-го места работы', 'Проверка паспорта', 'Проверка по списку террористов', 'Проверка на самозанятого', 'Проверка ИНН', 'Проверка долгов', 'Проверка банкротства', 'Проверка по БКИ', 'Проверка аффилированности', 'Проверка дискваилфикации', 'Проверка по БД', 'Проверка Internet', 'Проверка Сronos', 'Проверка Cross', 'Результат', 'Дата проверки', 'Сотрудник', 'Ссылка']

# запрос в базу данных
def response_db(db, query):
    try:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
            record_db = cur.fetchall()
    except sqlite3.Error as error:
        print('Ошибка', error)       
    return record_db

def change_value():
    response_db(db = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db', query ="UPDATE candidates SET staff = '"+staff_val+"' where id = '"+id_val+"'")

# запустить окно редактирования базы данных
def update_db(columns, selected_people):
    print(selected_people)
    master = Toplevel()
    dw = MainWindow
    dw(master,'База данных', '960x780')
    master.rowconfigure(0, weight=1)
    
    frame_db = Frame(master)
    frame_db.grid(row=0, column=0, columnspan=4, rowspan=1, pady=10, padx=10)        

    #vert_s = Scrollbar(frame_db, orient = "vertical")
    #vert_s.grid(column = 3, rowspan=len(columns), row = 0, sticky = 'N'+'S')
    #vert_s.config(command=frame_db.yview)

    title_text = ['Название поля', 'Значение', 'Изменить значение в БД']
    for i in range(len(title_text)):
        dw.create_labeles(frame_db, f"{title_text[i]}", ('Arial', 10), 30, 'center', 10, 5, 0, i)
    
    for i in range(len(columns)):
        dw.create_labeles(frame_db, f"{columns[i]}", ('Arial', 10), 30, 'w', 10, 5, i+1, 0)
    
    id_val = StringVar()
    id_val.set(selected_people[0])
    dw.create_entries(frame_db, id_val, 40, None, 1, 1)
    
    staff_val = StringVar()
    staff_val.set(selected_people[1])
    dw.create_entries(frame_db, staff_val, 40, None, 2, 1)
    dw.create_buttons(frame_db, "Обновить", change_value, 2, 2)
    
    dept_val = StringVar()
    dept_val.set(selected_people[2])
    dw.create_entries(frame_db, dept_val, 40, None, 3, 1)
    dw.create_buttons(frame_db, "Обновить", change_value, 3, 2)





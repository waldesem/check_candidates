from tkinter import Toplevel, Label, Frame, Text, ttk, messagebox
from app_window import MainWindow
import sqlite3

CONNECT = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'

COLS = ['id', 'Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения', 'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН', 'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование', 'Период работы на 1-м МР', '1-е место работы', 'Период работы на 2-м МР', '2-е место работы', 'Период работы на 3-м МР', '3-е место работы', 'Проверка по местам работы', 'Проверка паспорта', 'Проверка по списку террористов', 'Проверка на самозанятого', 'Проверка ИНН', 'Проверка долгов', 'Проверка банкротства', 'Проверка по БКИ', 'Проверка аффилированности', 'Проверка дисквалификации', 'Проверка по БД', 'Проверка Internet', 'Проверка Сronos', 'Проверка Cros', 'Доп. информация', 'Результат', 'Дата проверки', 'Сотрудник', 'Ссылка']

# название столбцов базы данных
SQL = ["id", "staff", "department", "full_name", "last_name", "birthday", "birth_place", "country", "serie_passport", "number_passport", "date_given", "snils", "inn", "reg_address", "live_address", "phone", "email", "education", "first_time_work", "first_place_work", "second_time_work", "second_place_work", "third_time_work", "third_place_work", "check_work_place", "check_passport", "check_terror", "check_selfwork", "check_inn", "check_debt", "check_bancrupcy", "check_bki", "check_affilate", "check_disqual", "check_db", "check_internet", "check_cronos", "check_cross", "rand_info", "resume", "date_check", "officer", "url"]

# запрос в базу данных
def response_db(db, query):
    try:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
            if 'INSERT' in query:
                con.commit()
            record_db = cur.fetchall()    
    except sqlite3.Error as error:
        print('Ошибка', error)       
    return record_db

# запустить окно редактирования базы данных
def update_db(columns, selected_people):
    # свзяываем данные колонок SQl БД с их русским названием и данными, которые передаются из выделенной строки таблицы
    sql_col_dict = dict(zip(columns, SQL))
    col_select = dict(zip(columns, selected_people))

    # изменение записей в БД
    def change_value():
        resp = response_db(db = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db', query =f"UPDATE candidates SET {sql_col_dict[idx]} = {editor.get('1.0', 'end').strip()} where id = {selected_people[0]}")

        if len(resp):
            messagebox.showinfo(title="Ошибка", message="Проверьте данные", parent=master)
        else:
            messagebox.showinfo(title="Успех", message="Запись обновлена", parent=master)
    
    # получение данных из комбобокс
    def selected(event):
        global idx
        # получаем выбранный элемент в лейбле показываем его SQl поле, в текстовом - содержание строки.
        selection = combobox.get()
        for key in sql_col_dict:
            if key == selection:
                label["text"] = f"Вы выбрали изменить запись в колонке: {sql_col_dict[key]}"
                editor.delete("1.0", 'end')
                editor.insert("1.0", col_select[key])
                idx = key  # индекс для передачи в SQL запрос на изменение значения.
        return idx

    # старт окна базы данных
    master = Toplevel()
    dw = MainWindow
    dw(master,'База данных', '760x640')
    master.columnconfigure(0, weight=1)
    
    # создаем фрейм для размещения элементов
    frame_db = Frame(master)
    frame_db.grid(row=0, column=0, columnspan=2, rowspan=1, pady=10, padx=10)        
    
    # создаем динамический лейбл для информации
    label = Label(frame_db)
    label.grid(row=0, column=0, pady=10, padx=10)
    
    # создаем комбобокс
    combobox = ttk.Combobox(frame_db, values=columns, state="readonly")
    combobox.grid(row=1, column=0, pady=10, padx=10)
    combobox.bind("<<ComboboxSelected>>", selected)
    
    # создаем текстовое поле
    editor = Text(frame_db, wrap = "word")
    editor.grid(column = 0, row = 2, sticky = 'N'+'S'+'E'+'W')
    
    # создаем  скроллбары
    ys = ttk.Scrollbar(frame_db, orient = "vertical", command = editor.yview)
    ys.grid(column = 1, row = 2, sticky = 'N'+'S')
    xs = ttk.Scrollbar(frame_db, orient = "horizontal", command = editor.xview)
    xs.grid(column = 0, row = 3, sticky = 'E'+'W')
    editor["yscrollcommand"] = ys.set
    editor["xscrollcommand"] = xs.set
    
    # создаем кнопку для обновления  информации в БД
    dw.create_buttons(frame_db, "Обновить данные", change_value, 4, 0)

    


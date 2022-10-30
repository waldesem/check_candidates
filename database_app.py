from tkinter import Toplevel, Label, Frame, Text, ttk, messagebox
from app_window import MainWindow
import sqlite3


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

sql_col = ["id", "staff", "department", "full_name", "last_name", "birthday", "birth_place", "country", "serie_passport", "number_passport", "date_given", "snils", "inn", "reg_address", "live_address", "phone", "email", "education", "first_time_work", "first_place_work", "check_first_place", "second_time_work", "second_place_work", "check_second_place", "third_time_work", "third_place_work", "check_third_place", "check_passport", "check_terror", "check_selfwork", "check_inn", "check_debt", "check_bancrupcy", "check_bki", "check_affilate", "check_disqual", "check_db", "check_internet", "check_cronos", "check_cross", "resume", "date_check", "officer", "url"]


# запустить окно редактирования базы данных
def update_db(columns, selected_people):
    
    sql_col_dict = dict(zip(columns, sql_col))
    col_select = dict(zip(columns, selected_people))

    # обновление записей в БД
    def change_value():
        resp = response_db(db = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db', query ="UPDATE candidates SET '"+sql_col_dict[idx]+ "' = '"+editor.get("1.0", "end").strip()+"' where id = '"+selected_people[0]+"'")
        if len(resp):
            messagebox.showinfo(title="Ошибка", message="Проверьте данные", parent=master)
        else:
            messagebox.showinfo(title="Успех", message="Запись обновлена", parent=master)
    
    # получение данных из комбобокс
    def selected(event):
        global idx
        # получаем выделенный элемент
        selection = combobox.get()
        for key in sql_col_dict:
            if key == selection:
                label["text"] = f"Вы выбрали изменить: {sql_col_dict[key]}"
                editor.delete("1.0", 'end')
                editor.insert("1.0", col_select[key])
                idx = key
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

    


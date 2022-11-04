from tkinter import Tk, ttk, StringVar, messagebox, Frame, Scrollbar, Text, Menu
import subprocess

from docx import Document

from app_window import MainWindow
from about_app import about_db_pro
from login_app import user_login
from database_app import response_db, update_db, CONNECT, COLS


# клик по кнопке поиск в БД записей по ФИО и дате рождения
def db_search():
    query = (f"SELECT * FROM candidates WHERE full_name like {fio_search.get()} and birthday like {dr_search.get()}")
    try:
        search_query = [i for i in response_db(CONNECT, query)]
        # удаляем старые записи в окне таблицы
        for i in tree.get_children():
            tree.delete(i)
        # записываем найденные записи
        for i in range(len(search_query)):
            tree.insert('', 'end', values=search_query[i])
    except IndexError:
        messagebox.showinfo(title="Результат проверки", message="Запись в БД не найдена")
    return search_query

# клик по кнопке поиск в БД записей по SQL-запросу
def db_search_where():
    query = (str(sql_search.get()))
    print(query)
    try:
        search_query = [i for i in response_db(CONNECT, query)]
        # удаляем старые записи в окне таблицы
        for i in tree.get_children():
            tree.delete(i)
        # записываем найденные записи
        for i in range(len(search_query)):
            tree.insert('', 'end', values=search_query[i])
    except IndexError:
        messagebox.showinfo(title="Результат проверки", message="Запись в БД не найдена")
    return search_query

# общий запрос в БД перед стартом программы
def start_query():
    query = ("SELECT * FROM candidates ORDER BY date_check DESC LIMIT 10")
    try:
        for i in tree.get_children():
            tree.delete(i)
        search_query = [i for i in response_db(CONNECT, query)]
    except IndexError:
        messagebox.showinfo(title="Ошибка", message="БД не подключена")
    return search_query

# выбор строки в таблице базы данных и показ в текстовом поле
selected_people = ""
def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        global selected_people
        selected_people = '\n'.join(map(str, item["values"]))
    editor.delete("1.0", 'end')
    editor.insert("1.0", selected_people)
    return(selected_people)

# клик по кнопке Выгрузка информации из БД
def take_info():
    file_query = '/home/semenenko/Загрузки/yourfile.docx'
    document = Document()
    # создаем таблицу Word
    table = document.add_table(rows=len(COLS), cols=2)
    table.style = 'Table Grid'
    for i in range(len(COLS)):
        table.rows[i].cells[0].text = COLS[i]
        table.rows[i].cells[1].text = selected_people.split('\n')[i]
    document.save(file_query)
    subprocess.call(["xdg-open", file_query])

# клик по конопке меню изменить запись в БД
def change_db():
    update_db(COLS, selected_people.split('\n'))

if __name__ == '__main__':
    master = Tk()
    dbw = MainWindow
    dbw(master,'База данных', '960x860')
    # окно сообщений
    master.option_add('*Dialog.msg.font', 'Arial 10')   
    master.columnconfigure(0, weight=1)
    # master.rowconfigure(0, weight=1)

    dbw.menu = Menu(master)
    dbw.menu_label_lst = ['Войти в БД', 'Настройки', 'О программе']
    dbw.command_lst = [user_login, 'settings', about_db_pro]
    for n in range(len(dbw.command_lst)):
        dbw.create_menu(master, dbw.menu_label_lst[n], dbw.command_lst[n], dbw.menu)

    # фрейм виджетов базы данных
    db_frame = Frame(master)
    db_frame.grid(row=0, column=0, columnspan=4, rowspan=1, pady=10, padx=10)
    for i in range (3):
        db_frame.columnconfigure(i, weight=1)

    #создаем название видежетов на вкладке База данных
    dbw.txt_search = ['Фамилия Имя Отчество', 'Дата рождения']
    for i in range(len(dbw.txt_search)):
        dbw.create_labeles(db_frame, f"{dbw.txt_search[i]}", ('Arial', 10), 30, 'w', 10, 10, i, 0)
    fio_search = StringVar()
    fio_search.set("Фамилия Имя Отчество")
    dbw.create_entries(db_frame, fio_search, 40, None, 0, 1)
    dr_search = StringVar()
    dr_search.set("ДД.ММ.ГГГГ")
    dbw.create_entries(db_frame, dr_search, 40, None, 1, 1)
    dbw.create_labeles(db_frame, 'Найти по условию', ('Arial', 10), 40, 'center', 10, 10, 0, 2)
    dbw.create_buttons(db_frame, "Поиск", db_search, 1, 2)
    
    # поиск по sql запросу
    dbw.create_labeles(db_frame, 'Запрос в формате SQL', ('Arial', 10), 30, 'w', 10, 10, 2, 0)
    sql_search = StringVar()
    sql_search.set("Select * from candidates where...")
    dbw.create_entries(db_frame, sql_search, 40, None, 2, 1)
    dbw.create_buttons(db_frame, "SQL запрос", db_search_where, 2, 2)
    dbw.create_labeles(db_frame, 'Результаты поиска', ('Arial', 10), 30, 'w', 10, 10, 3, 1)
    dbw.create_buttons(db_frame, "Выгрузить данные", take_info, 0, 3)
    dbw.create_buttons(db_frame, "Изменить данные", change_db, 1, 3)
    dbw.create_buttons(db_frame, "Обновить данные", start_query, 2, 3)
    
    # фрейм и таблица записей из БД
    frame_table = Frame(master)
    frame_table.grid(row=4, column=0, columnspan=4, rowspan=1, pady=10, padx=20)
    for col in range(len(COLS)):
        frame_table.columnconfigure(col, weight=1)

    # настройки скролбаров
    x_scrollbar = Scrollbar(frame_table, orient='horizontal')
    x_scrollbar.grid(row=1, column=0, columnspan=3, sticky='E'+'W')
    y_scrollbar = Scrollbar(frame_table, orient='vertical')
    y_scrollbar.grid(row=0, column=3, sticky='N'+'S')
    
    # размещение столбцов, строк  и др.
    tree = ttk.Treeview(frame_table, columns=COLS, height=5, show="headings", displaycolumns= [COLS[1]] + [COLS[3]] + [COLS[5]] + [COLS[-4]] + [COLS[-2]], xscrollcommand=x_scrollbar.set,yscrollcommand=y_scrollbar.set)
    tree.grid(row=0, column=0, columnspan=3, sticky='E'+'W')
    x_scrollbar['command'] = tree.xview
    y_scrollbar['command'] = tree.yview
    
    # настройка заголовков
    for col in tree['columns']:
        tree.heading(col, text=f"{col}", anchor='center')
        tree.column(col, anchor='center', width=160)
   
    # загрузка записей по умолчанию на старте программы
    search_query = start_query()
    for i in range(len(search_query)):
        tree.insert('', 'end', values=search_query[i])

    # выбор строки в таблице результатов
    tree.bind("<<TreeviewSelect>>", item_selected)
    
    # фрейм и текстовое поле для выбранной записи из таблицы БД
    frame_select = Frame(master)
    frame_select.grid(row=5, column=0, columnspan=4, rowspan=1, pady=10, padx=20)        
    
    # параметры текстового поля
    editor = Text(frame_select, height=24, wrap = "word")
    editor.grid(column = 0, row = 0, sticky = 'E'+'W')
    
    #  скроллбары текстового поля
    ys = ttk.Scrollbar(frame_select, orient = "vertical", command = editor.yview)
    ys.grid(column = 3, row = 0, sticky = 'N'+'S')
    xs = ttk.Scrollbar(frame_select, orient = "horizontal", command = editor.xview)
    xs.grid(column = 0, row = 1, sticky = 'E'+'W')
    editor["yscrollcommand"] = ys.set
    editor["xscrollcommand"] = xs.set
    
    # запуск главного окна
    master.mainloop()
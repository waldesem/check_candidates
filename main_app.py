from tkinter import Tk, ttk, Menu, StringVar, messagebox, Frame, Scrollbar, Text
from app_window import MainWindow
from login_app import user_login
from about_app import about_program
from check_app import check, upload, db_add
from database_app import response_db, update_db
from docx import Document
import subprocess

# запуск по кнопке "Загрузить анкету"
def click_upload():
    # анкетные данные на вкладке Анкета
    anketa_response = upload()
    for k in range(len(anketa_response)):
        mw.create_labeles(mw.tab_anketa, anketa_response[k], ('Arial', 10), 100, 'w', 8, 5, k, 1)   

# запуск по кнопке "Проверить кандидата"
def click_check():
    response_all = check()
    for m in range(len(response_all)):
        mw.create_labeles(mw.tab_check, response_all[m], ('Arial', 10), 100, 'w', 8, 5, m, 1)

# клик по кнопке загрузить в БД
def upload_db():
    db_upload = db_add()
    if len(db_upload):
        messagebox.showinfo(title="Внимание", message="Ошибка записи. Проверьте БД.")
    else:
        messagebox.showinfo(title="Успех", message="Запись внесена в БД")

# клик по кнопке поиск в БД записей по ФИО и дате рождения
def db_search():
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'
    query = ("SELECT * FROM candidates WHERE full_name like "+"'"+fio_search.get()+"'"+' and birthday like '+"'"+dr_search.get()+"'")
    try:
        search_query = [i for i in response_db(connect, query)]
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
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'
    query = (str(sql_search.get()))
    print(query)
    try:
        search_query = [i for i in response_db(connect, query)]
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
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'
    query = ("SELECT * FROM candidates ORDER BY date_check DESC LIMIT 10")
    try:
        for i in tree.get_children():
            tree.delete(i)
        search_query = [i for i in response_db(connect, query)]
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
    table = document.add_table(rows=len(columns), cols=2)
    table.style = 'Table Grid'
    for i in range(len(columns)):
        table.rows[i].cells[0].text = columns[i]
        table.rows[i].cells[1].text = selected_people.split('\n')[i]
    document.save(file_query)
    subprocess.call(["xdg-open", file_query])

def change_db():
    update_db(columns, selected_people.split('\n'))

# главное окно приложения
if __name__ == '__main__':
    root = Tk()
    mw = MainWindow
    mw(root,'Кадровая безопасность', '960x780')
    # окно сообщений
    root.option_add('*Dialog.msg.font', 'Arial 10')   
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # создаем виджеты и команды в меню
    mw.menu = Menu(root)
    mw.menu_label_lst = ['Войти в систему', 'Загрузить анкету', 'Начать проверку', 'Загрузить в БД', 'Изменить БД', 'О программе']
    mw.command_lst = [user_login, click_upload, click_check, upload_db, change_db, about_program]
    for n in range(len(mw.command_lst)):
        mw.create_menu(root, mw.menu_label_lst[n], mw.command_lst[n], mw.menu)

    # панель вкладок
    mw.style = ttk.Style()
    mw.style.configure('TNotebook.Tab', font=('Arial', 10))
    mw.tab_control = ttk.Notebook(root)
    mw.tab_control.pack(expand=1, fill='both')

    # вкладка анкеты
    mw.tab_anketa = ttk.Frame(mw.tab_control)
    mw.tab_control.add(mw.tab_anketa, text='Анкета кандидата')

    # создаем название виджетов на вкладке Анкета
    mw.anketa_labeles = ['Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения', 'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН', 'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование', 'Период работы', 'Место работы', 'Период работы', 'Место работы', 'Период работы', 'Место работы']
    for i in range(len(mw.anketa_labeles)):
        mw.create_labeles(mw.tab_anketa, f"{mw.anketa_labeles[i]}", ('Arial', 10), 30, 'w', 10, 5, i, 0)

    # вкладка проверки
    mw.tab_check = ttk.Frame(mw.tab_control)
    mw.tab_control.add(mw.tab_check, text='Проверка кандидата')
    # создаем название виджетов на вкладке Проверки
    mw.txt_chk = ['Проверка статуса самозанятого', 'Проверка ИНН', 'Проверка по списку кандидатов',
            'Проверка по списку дисквалифиции', 'Проверка паспорта']
    for i in range(len(mw.txt_chk)):
        mw.create_labeles(mw.tab_check, f"{mw.txt_chk[i]}", ('Arial', 10), 40, 'w', 10, 5, i, 0) 

    # вкладка базы данных
    mw.tab_db = ttk.Frame(mw.tab_control)
    mw.tab_control.add(mw.tab_db, text='База данных')
    for i in range (3):
        mw.tab_db.columnconfigure(i, weight=1)

    #создаем название видежетов на вкладке База данных
    mw.txt_search = ['Фамилия Имя Отчество', 'Дата рождения']
    for i in range(len(mw.txt_search)):
        mw.create_labeles(mw.tab_db, f"{mw.txt_search[i]}", ('Arial', 10), 30, 'w', 10, 10, i, 0)
    fio_search = StringVar()
    fio_search.set("Фамилия Имя Отчество")
    mw.create_entries(mw.tab_db, fio_search, 40, None, 0, 1)
    dr_search = StringVar()
    dr_search.set("ДД.ММ.ГГГГ")
    mw.create_entries(mw.tab_db, dr_search, 40, None, 1, 1)
    mw.create_labeles(mw.tab_db, 'Найти по условию', ('Arial', 10), 40, 'center', 10, 10, 0, 2)
    mw.create_buttons(mw.tab_db, "Поиск", db_search, 1, 2)
    # поиск по sql запросу
    mw.create_labeles(mw.tab_db, 'Запрос в формате SQL', ('Arial', 10), 30, 'w', 10, 10, 2, 0)
    sql_search = StringVar()
    sql_search.set("Select * from candidates where...")
    mw.create_entries(mw.tab_db, sql_search, 40, None, 2, 1)
    mw.create_buttons(mw.tab_db, "SQL запрос", db_search_where, 2, 2)
    mw.create_buttons(mw.tab_db, "Выгрузить данные", take_info, 3, 2)
    mw.create_labeles(mw.tab_db, 'Результаты поиска', ('Arial', 10), 30, 'w', 10, 10, 3, 0)
    mw.create_buttons(mw.tab_db, "Обновить данные", start_query, 3, 1)


    # фрейм и таблица записей из БД
    frame_table = Frame(mw.tab_db)
    frame_table.grid(row=4, column=0, columnspan=4, rowspan=1, pady=10, padx=20)
    columns = ['id', 'Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения', 'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН', 'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование', 'Период работы на 1-м МР', '1-е место работы', 'Проверка 1-го места работы', 'Период работы на 2-м МР', '2-е место работы', 'Проверка 2-го места работы', 'Период работы на 3-м МР', '3-е место работы', 'Проверка 3-го места работы', 'Проверка паспорта', 'Проверка по списку террористов', 'Проверка на самозанятого', 'Проверка ИНН', 'Проверка долгов', 'Проверка банкротства', 'Проверка по БКИ', 'Проверка аффилированности', 'Проверка дискваилфикации', 'Проверка по БД', 'Проверка Internet', 'Проверка Сronos', 'Проверка Cross', 'Результат', 'Дата проверки', 'Сотрудник', 'Ссылка']
    for col in range(len(columns)):
        frame_table.columnconfigure(col, weight=1)

    # настройки скролбаров
    x_scrollbar = Scrollbar(frame_table, orient='horizontal')
    x_scrollbar.grid(row=1, column=0, columnspan=3, sticky='E'+'W')
    y_scrollbar = Scrollbar(frame_table, orient='vertical')
    y_scrollbar.grid(row=0, column=3, sticky='N'+'S')
    
    # размещение столбцов, строк  и др.
    tree = ttk.Treeview(frame_table, columns=columns, height=5, show="headings", displaycolumns= ['Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Дата рождения', 'Результат', 'Дата проверки'], xscrollcommand=x_scrollbar.set,yscrollcommand=y_scrollbar.set)
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
    frame_select = Frame(mw.tab_db)
    frame_select.grid(row=5, column=0, columnspan=4, rowspan=1, pady=10, padx=20)        
    
    # параметры текстового поля
    editor = Text(frame_select, height=20, wrap = "word")
    editor.grid(column = 0, row = 0, sticky = 'E'+'W')
    
    #  скроллбары текстового поля
    ys = ttk.Scrollbar(frame_select, orient = "vertical", command = editor.yview)
    ys.grid(column = 3, row = 0, sticky = 'N'+'S')
    xs = ttk.Scrollbar(frame_select, orient = "horizontal", command = editor.xview)
    xs.grid(column = 0, row = 1, sticky = 'E'+'W')
    editor["yscrollcommand"] = ys.set
    editor["xscrollcommand"] = xs.set
    
    # запуск главного окна
    root.mainloop()


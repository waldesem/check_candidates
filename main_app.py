from tkinter import Tk, ttk, Menu, Button, Label, StringVar, Entry, messagebox, Frame, Scrollbar
from login_app import user_login
from about_app import about_program
from check_app import response_db
from docx import Document
import check_app
import subprocess


class MainWindow:
    def __init__(self, master, title, geometry):
        self.master = master
        self.title = title
        self.geometry = geometry
        master.title(title)
        master.geometry(geometry)
    
    def create_labeles(self, text, font, width, anchor, padx, pady, row, column):
        self.text = text
        self.font = font
        self.width = width
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.row = row
        self.column = column
        Label(self, text=text, font=font, width=width, anchor=anchor, 
                                    padx=padx, pady=pady).grid(row=row, column=column)

    def create_buttons(self, text, command, row, column):
        self.textvariable = text
        self.command = command
        self.row = row
        self.column = column
        Button(self, text=text, command=command).grid(row=row, column=column)

    def create_entries(self, textvariable, width, show, row, column):
        self.textvariable = textvariable
        self.width = width
        self.show = show
        self.row = row
        self.column = column
        Entry(self, textvariable=textvariable, width=width, show=show).grid(row=row, column=column)  
    
    def create_menu(self, label, command, menu):
        self.menu = menu
        self.label = label
        self.command = command
        menu.add_command(label=label, font=('Arial', 10), command=command)
        self.config(menu=menu)

# запуск по кнопке войти в систему
def click_login():
    user_login()

# запуск по кнопке "Загрузить анкету"
def click_upload():
    # анкетные данные на вкладке Анкета
    anketa_response = check_app.upload()
    for k in range(len(anketa_response)):
        mw.create_labeles(mw.tab_anketa, anketa_response[k], ('Arial', 10), 100, 'w', 8, 5, k, 1)   

# запуск по кнопке "Проверить кандидата"
def click_check():
    response_all = check_app.check()
    for m in range(len(response_all)):
        mw.create_labeles(mw.tab_check, response_all[m], ('Arial', 10), 100, 'w', 8, 5, m, 1)

# клик по кнопке загрузить в БД
def upload_db():
    db_upload = check_app.db_add()
    if len(db_upload):
        messagebox.showinfo(title="Внимание", message="Ошибка записи. Проверьте БД.")
    else:
        messagebox.showinfo(title="Успех", message="Запись внесена в БД")

# клик по кнопке поиск в БД записей по ФИО и дате рождения
def db_search():
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'
    query = ("SELECT * FROM candidates WHERE full_name like "+"'"+fio_search.get()+"'"+' and birthday like '+"'"+dr_search.get()+"'")
    #query2 = ('PRAGMA table_info("Candidates")')
    try:
        search_query = [i for i in response_db(connect, query)]
        for i in tree.get_children():
            tree.delete(i)
        for i in range(len(search_query)):
            tree.insert('', 'end', values=search_query[i])
        #db_col = [i[1] for i in response_db(connect, query2)]
    except IndexError:
        messagebox.showinfo(title="Результат проверки", message="Запись в БД не найдена")
    #search_query.extend([db_col, db_row])
    return search_query

# клик по кнопке Выгрузка информации из БД
def take_info():
    file_query = '/home/semenenko/Загрузки/yourfile.docx'
    document = Document()
    table = document.add_table(rows=len(search_query), cols=1)
    table.style = 'Table Grid'
    for i in range(len(search_query)):
        table.rows[i].cells[0].text = str(search_query[i])
    document.save(file_query)
    subprocess.call(["xdg-open", file_query])

# общий запрос в БД перед стартом программы
def start_query():
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/candidates_db.db'
    query = ("SELECT * FROM candidates ORDER BY date_check DESC LIMIT 10")
    try:
        search_query = [i for i in response_db(connect, query)]
    except IndexError:
        messagebox.showinfo(title="Ошибка", message="БД не подключена")
    return search_query

# клик по кнопке открыть БД
def open_db():
    pass

# клик по кнопке "О программе"
def about_pro():
    about_program()

# главное окно приложения
if __name__ == '__main__':
    root = Tk()
    mw = MainWindow
    mw(root,'Кадровая безопасность', '1080x880')
    # mw(root,'Кадровая безопасность', '1920x1080')
    # окно сообщений
    root.option_add('*Dialog.msg.font', 'Arial 10')   

    # создаем виджеты и команды в меню
    mw.menu = Menu(root)
    mw.menu_label_lst = ['Войти в систему', 'Загрузить анкету', 'Начать проверку', 'Загрузить в БД', 'Открыть БД', 'О программе']
    mw.command_lst = [click_login, click_upload, click_check, upload_db, open_db, about_pro]
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
    # поиск по sql запросу (функция не прописана)
    mw.create_labeles(mw.tab_db, 'Или запрос в формате SQL', ('Arial', 10), 30, 'w', 10, 10, 2, 0)
    sql_search = StringVar()
    sql_search.set("Select * from candidates where...")
    mw.create_entries(mw.tab_db, sql_search, 40, None, 2, 1)
    mw.create_buttons(mw.tab_db, "SQL запрос", 'db_search', 2, 2)
    mw.create_labeles(mw.tab_db, 'Результаты поиска', ('Arial', 10), 30, 'w', 10, 10, 3, 1)
    mw.create_buttons(mw.tab_db, "Выгрузить данные", 'take_info', 6, 2)

    # таблица записей из БД
    frame_table = Frame(mw.tab_db)
    frame_table.grid(row=4, column=0, columnspan=3, rowspan=4, pady=20, padx=5)
    columns = ['id','staff', 'department', 'full_name', 'last_name', 'birthday', 'birth_place', 'country'] #'serie_passport', 'number_passport', 'date_given', 'snils', 'inn', 'reg_address', 'live_address', 'phone', 'email', 'education', 'first_time_work', 'first_place_work', 'check_first_place', 'second_time_work', 'second_place_work', 'check_second_place', 'third_time_work', 'third_place_work', 'check_third_place', 'check_passport', 'check_terror', 'check_selfwork', 'check_inn', 'check_debt', 'check_bancrupcy', 'check_bki', 'check_affilate', 'check_disqual', 'check_db', 'check_internet', 'check_cronos', 'check_cross', 'resume', 'date_check', 'officer', 'url']
    # настройки скролбаров
    x_scrollbar = Scrollbar(mw.tab_db, orient='horizontal')
    x_scrollbar.grid(row=5, column=0, columnspan=3, padx=10, sticky='N'+'S'+'E'+'W')
    y_scrollbar = Scrollbar(mw.tab_db, orient='vertical')
    y_scrollbar.grid(row=4, column=4, sticky='N'+'S'+'E'+'W')
    # размещенение столбцов, строк  и др.
    tree = ttk.Treeview(mw.tab_db, columns=columns, height=10, show="headings", xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    tree.grid(row=4, column=0, columnspan=3, padx=10, sticky='N'+'S'+'E'+'W')
    # использование скролбаров
    x_scrollbar['command'] = tree.xview
    y_scrollbar['command'] = tree.yview
    # настройка заголовков
    for col in tree['columns']:
            tree.heading(col, text=f"{col}", anchor='center')
            tree.column(col, anchor='center', width=180)
    # загрузка записей по умолчанию на старте программы
    search_query = start_query()
    for i in range(len(search_query)):
        tree.insert('', 'end', values=search_query[i])

    # запуск главного окна
    root.mainloop()


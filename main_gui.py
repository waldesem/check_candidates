import sqlite3
from tkinter import Tk, Button, Label, StringVar, Entry, ttk, Menu, messagebox as mb
import files_check
import check_info
import sqlite3
import webbrowser

class Window:
    def __init__(self, master, title, geometry):
        self.master = master
        self.title = title
        self.geometry = geometry
        master.title(title)
        master.geometry(geometry)
    
    def create_labeles(self, text, width, anchor, padx, pady, row, column):
        self.text = text
        self.width = width
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.row = row
        self.column = column
        Label(self, text=text, font=('Arial', 10), width=width, anchor=anchor, 
                                    padx=padx, pady=pady).grid(row=row, column=column)
    
    def create_entries(self, textvariable, show, row, column):
        self.textvariable = textvariable
        self.show = show
        self.row = row
        self.column = column
        Entry(self, textvariable=textvariable, show=show).grid(row=row, column=column)  

    def create_buttons(self, text, command, row, column):
        self.textvariable = text
        self.command = command
        self.row = row
        self.column = column
        Button(self, text=text, command=command).grid(row=row, column=column)
    
    def create_menu(self, label, command, menu):
        self.menu = menu
        self.label = label
        self.command = command
        menu.add_command(label=label, font=('Arial', 10), command=command)
        self.config(menu=menu)

# запуск по кнопке "Загрузить анкету"
def click_upload():
    # анкетные данные на вкладке Анкета
    anketa_response = files_check.upload()
    for k in range(len(anketa_response)):
        mw.create_labeles(tab_anketa, anketa_response[k], 100, 'w', 8, 5, k, 1)   

# запуск по кнопке "Проверить кандидата"
def click_check():
    response_all = check_info.check()
    for m in range(len(response_all)):
        Label(tab_check, text=response_all[m], font=('Arial', 10), width=100, anchor='w',
                padx=8, pady=5).grid(sticky="w", column=1, row=m)

# поиск в базе данных записей по ФИО и дате рождения
def db_response():
    global record_db
    global column_names
    try:
        sqlite_connection = sqlite3.connect('/home/semenenko/MyProjects/Python/Staff_check/DB_check/kandidates.db')
        cursor_obj = sqlite_connection.cursor()
        cursor_obj.execute("SELECT * FROM Candidates WHERE ФИО like " + "'" + fio_search.get() + 
                            "'" + ' and Датарождения like ' + "'" + dr_search.get() + "'")
        # преобразование полученных записей из кортежа в список
        record_db = [i for i in cursor_obj.fetchall()[0]]
        # получаем название полей в таблице в виде списка
        cursor_obj.execute('PRAGMA table_info("Candidates")')
        column_names = [i[1] for i in cursor_obj.fetchall()]
        try:
            if record_db[1] == fio_search.get() and record_db[2] == dr_search.get():
                for i in range(3):
                    # создаем надписи на вкладке базы данных по итогам поиска
                    mw.create_labeles(tab_db,column_names[i], 40, 'w', 5, 5, i+2, 0)
                    mw.create_labeles(tab_db,record_db[i], 60, 'w', 5, 5, i+2, 1)
        except IndexError:
            mb.showinfo(title="Внимание", message="Запись не найдена")
        cursor_obj.close()
    except sqlite3.Error as error:
        mb.showinfo(title = "Внимание", message = "Ошибка при подключении к sqlite" + error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return record_db

# выгрузка информации по запросу
def take_info():
    query_file = "/home/semenenko/Загрузки/yourfile.txt"
    with open(query_file, 'w') as f:
        for i in range(len(column_names)):
            f.write(str(column_names[i]) + '\t')
            f.write(str(record_db[i]) + '\n')
        mb.showinfo(title = "Успех", message = "Запись выгружена в файл")
    webbrowser.open(query_file)

# клик по кнопке "О программе"
def about_program():
    about_window = Tk()
    aw = Window
    aw(about_window,'О программе', '360x180')
    about_txt = ['Программа "Кадровая безопасность"', 'Разработка: wsemenenko@gmail.com', 
                'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_txt)):
        aw.create_labeles(about_window, f"{about_txt[i]}", 45, 'center', 0, 5, i, 0)

if __name__ == "__main__":
    # главное окно приложения
    root = Tk()
    mw = Window
    mw(root,'Кадровая безопасность', '960x780')
    # окно сообщений
    root.option_add('*Dialog.msg.font', 'Arial 10')   
    # создаем виджеты и команды в меню
    menu = Menu(root)
    menu_label_lst = ['Загрузить анкету', 'Начать проверку', 'Получить заключение', 
                'Искать в БД', 'Выгрузить из БД', 'Изменить запись в БД', 'О программе']
    command_lst = [click_upload, click_check,
                files_check.download_file, db_response, take_info, 'change_db', 
                about_program]
    for n in range(len(command_lst)):
        mw.create_menu(root, menu_label_lst[n], command_lst[n], menu)
    # панель вкладок
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Arial', 10))
    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill='both')
    # вкладка анкеты
    tab_anketa = ttk.Frame(tab_control)
    tab_control.add(tab_anketa, text='Анкета кандидата')
    # создаем название виджетов на вкладке Анкета
    anketa_labeles = ['Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения',
                'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 
                'СНИЛС', 'ИНН', 'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 
                'Образование', 'Период работы', 'Место работы', 'Период работы', 'Место работы', 
                'Период работы', 'Место работы']
    for i in range(len(anketa_labeles)):
        mw.create_labeles(tab_anketa, f"{anketa_labeles[i]}", 40, 'w', 10, 5, i, 0)
    # вкладка проверки
    tab_check = ttk.Frame(tab_control)
    tab_control.add(tab_check, text='Проверка кандидата')
    # создаем название виджетов на вкладке Проверки
    txt_chk = ['Проверка статуса самозанятого', 'Проверка ИНН', 'Проверка по списку кандидатов',
            'Проверка по списку дисквалифиции', 'Проверка паспорта']
    for i in range(len(txt_chk)):
        mw.create_labeles(tab_check, f"{txt_chk[i]}", 40, 'w', 10, 5, i, 0) 
    # вкладка базы данных
    tab_db = ttk.Frame(tab_control)
    tab_control.add(tab_db, text='База данных')
    #создаем название видежетов на вкладке База данных
    txt_search = ['Фамилия Имя Отчество', 'Дата рождения']
    for i in range(len(txt_search)):
        mw.create_labeles(tab_db, f"{txt_search[i]}", 40, 'w', 10, 5, i, 0)
    fio_search = StringVar()
    search_fio = Entry(tab_db, textvariable=fio_search, width = 60, font=('Arial', 10)).grid(sticky="we", pady=5, column=1, row=0)
    dr_search = StringVar()
    search_fio = Entry(tab_db, textvariable=dr_search, width = 60, font=('Arial', 10)).grid(sticky="we", pady=5, column=1, row=1)

    root.mainloop()

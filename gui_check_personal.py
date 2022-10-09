# графический интерфейс для проверки кандидатов на работу
from tkinter import Entry, Tk, Label, Menu, ttk, StringVar, messagebox as mb
import login
import menu_upload
import check_main
import menu_download
import about_me
import sqlite3
import webbrowser

#создание главного  окна программы
def create_window(title, geometry):
    master.title(title)
    master.geometry(geometry)

#создание меню
def create_menu(label, command):
    menu.add_command(label=label, font=('Arial', 10), command=command)
    master.config(menu=menu)

#создание надписей
def create_labels(tab, text, width, column, row):
    Label(tab, text=text, font=('Arial', 10), width=width, anchor='w',
           padx=8, pady=5).grid(sticky="w", column=column, row=row)

# запуск по кнопке "Загрузить анкету"
def click_upload():
    anketa_response = menu_upload.upload()
    # анкетные данные на вкладке Анкета
    for k in range(len(anketa_response)):
        Label(tab_anketa, text=anketa_response[k], font=('Arial', 10), width=100, anchor='w',
                padx=8, pady=5).grid(sticky="w", column=1, row=k)

# запуск по кнопке "Проверить кандидата"
def click_check():
    response_all = check_main.check()
    for m in range(len(response_all)):
        Label(tab_check, text=response_all[m], font=('Arial', 10), width=100, anchor='w',
                padx=8, pady=5).grid(sticky="w", column=1, row=m)

# поиск в базе данных записей по ФИО и дате рождения
def db_response():
    global record_db
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
                    create_labels(tab_db,column_names[i], 40, 0, i+2)
                    create_labels(tab_db,record_db[i], 60, 1, i+2)
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
        for i in record_db:
            f.write(str(i) + '\n')
        mb.showinfo(title = "Успех", message = "Запись выгружена в файл")
    webbrowser.open(query_file)

if __name__ == "__main__":
    #проверка логина и пароля
    if login.auth is True:
        #запуск главного окна
        master = Tk()
        create_window('Кадровая безопасность', '960x780')
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        # окно сообщений
        master.option_add('*Dialog.msg.font', 'Arial 10')
        # панель меню
        menu = Menu(master)
        # создаем виджеты и команды в меню
        menu_label_lst = ['Загрузить анкету', 'Начать проверку', 'Получить заключение', 
                        'Искать в БД', 'Выгрузить из БД', 'Изменить запись в БД', 'О программе']
        command_lst = [click_upload, click_check,
                        menu_download.download_file, db_response, take_info, 'change_db', 
                        about_me.about_program]
        for n in range(len(command_lst)):
            create_menu(menu_label_lst[n], command_lst[n])

        # панель вкладок
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 10))
        tab_control = ttk.Notebook(master)
        # вкладка анкеты
        tab_anketa = ttk.Frame(tab_control)
        tab_control.add(tab_anketa, text='Анкета кандидата')
        tab_control.pack(expand=1, fill='both')
        # вкладка проверки
        tab_check = ttk.Frame(tab_control)
        tab_control.add(tab_check, text='Проверка кандидата')
        tab_control.pack(expand=1, fill='both')
        # вкладка базы данных
        tab_db = ttk.Frame(tab_control)
        tab_control.add(tab_db, text='База данных')
        tab_control.pack(expand=1, fill='both')

        # создаем название виджетов на вкладке Анкета
        for i in range(len(menu_upload.anketa_labeles)):
            create_labels(tab_anketa, f"{menu_upload.anketa_labeles[i]}", 30, 0, i)

        # создаем название виджетов на вкладке Проверки
        txt_chk = ['Проверка статуса самозанятого', 'Проверка ИНН', 'Проверка по списку кандидатов',
                    'Проверка по списку дисквалифиции', 'Проверка паспорта']
        for i in range(len(txt_chk)):
            create_labels(tab_check, f"{txt_chk[i]}", 40, 0, i) 

        #создаем название видежетов на вкладке База данных
        txt_search = ['Фамилия Имя Отчество', 'Дата рождения']
        for i in range(len(txt_search)):
            create_labels(tab_db, f"{txt_search[i]}", 40, 0, i)
        fio_search = StringVar()
        search_fio = Entry(tab_db, textvariable=fio_search, width = 60, font=('Arial', 10)).grid(sticky="we", pady=5, column=1, row=0)
        dr_search = StringVar()
        search_fio = Entry(tab_db, textvariable=dr_search, width = 60, font=('Arial', 10)).grid(sticky="we", pady=5, column=1, row=1)

        master.mainloop()
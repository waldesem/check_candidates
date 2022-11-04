from tkinter import Tk, ttk, Menu, messagebox, StringVar
from app_window import MainWindow

from login_app import user_login
from about_app import about_program
from check_app import check, upload, db_add
from database_app import COLS


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
    mw.menu_label_lst = ['Войти в систему', 'Загрузить анкету', 'Начать проверку', 'Загрузить в БД', 'Запустить БД', 'Настройки', 'О программе']
    mw.command_lst = [user_login, click_upload, click_check, upload_db, 'open_db', 'settings',  about_program]
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
    mw.anketa_labeles = COLS[1:24]
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
   
    # запуск главного окна
    root.mainloop()


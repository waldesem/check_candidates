#графический интерфейс для проверки персонала
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import check_main
import menu_upload
import menu_download

#запуск по кнопке "Загрузить анкету"
def click_upload():
    anketa_response = menu_upload.upload()
    #анкетные данные на вкладке Анкета
    for k in range (len(anketa_response)):
        tk.Label(tab_anketa, text=anketa_response[k], font=('Arial', 10), width=100, anchor='w', 
                padx=8, pady=5).grid(sticky="w", column=1, row=k)

#запуск по кнопке "Проверить кандидата"
def click_check():
    response_all = check_main.check()
    for m in range (len(response_all)):
        tk.Label(tab_check, text=response_all[m], font=('Arial', 10), width=100, anchor='w', 
                padx=8, pady=5).grid(sticky="w", column=1, row=m)

#запуск по кнопке Получить заключение
def click_download():
    menu_download.download_file()

#создаем виджеты на вкладках
def create_widgets():
    #созадаем переменную с именами полей - виджетов
    txt1 = ['Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения', 'Место рождения', 
            'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН', 'Адрес регистрации',
            'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование', 'Период работы', 'Место работы',
            'Период работы', 'Место работы', 'Период работы', 'Место работы']
    #создаем первую колонку с полями на вкладке Анкета
    for i in range (len(txt1)):
        tk.Label(tab_anketa, text=f"{txt1[i]}", font=('Arial', 10), width=20, anchor='w', 
                padx=8, pady=5).grid(sticky="w", column=0, row=i)

    #виджеты результатов проверки
    txt2 = ['Проверка статуса самозанятого', 'Проверка ИНН', 'Проверка по списку кандидатов',
            'Проверка по списку дисквалифиции', 'Проверка паспорта']
    #создаем первую колонку с полями на вкладкке проверки
    for l in range (len(txt2)):
        tk.Label(tab_check, text=f"{txt2[l]}", font=('Arial', 10), width=40, anchor='w', 
                padx=8, pady=5).grid(sticky="w", column=0, row=l)

#клик по  кнопке "О программе"
def about_me():
    small_window = tk.Tk()
    small_window.title('О программе')
    small_window.geometry('420x240')
    about_lst = ['Программа проверки кандидатов', 'Используются открытые данные органов власти', 
                'Также используются внутренние источники', 'Автор: wsemenenko@gmail.com', 
                'https://github.com/waldesem', 'GNU General Public License, version 3']
    for i in range (len(about_lst)):
        tk.Label(small_window, text=f'{about_lst[i]}', font=('Arial', 10), pady=5).pack()

if __name__ == "__main__":
    #конфигурация окна
    window = tk.Tk()
    window.title('Проверка кандидата на работу в Банк')
    window.geometry('960x780')
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Arial', 10))

    #панель меню
    menu = Menu(window)
    upload_func_lst = [click_upload, click_check, click_download, about_me]
    menu_label_lst = ['Загрузить анкету', 'Начать проверку', 'Получить заключение', 'О программе']
    for n in range (len(upload_func_lst)):
        menu.add_command(label=menu_label_lst[n], font=('Arial', 10), command=upload_func_lst[n])
        window.config(menu=menu)

    #панель вкладок
    tab_control = ttk.Notebook(window)  

    #вкладка анкеты
    tab_anketa = ttk.Frame(tab_control)
    tab_control.add(tab_anketa, text='Анкета кандидата')  
    tab_control.pack(expand=1, fill='both')

    #вкладка проверки
    tab_check = ttk.Frame(tab_control)
    tab_control.add(tab_check, text='Проверка кандидата')  
    tab_control.pack(expand=1, fill='both')
    
    #окно сообщений
    window.option_add('*Dialog.msg.font', 'Arial 10')

    #создание виджетов на вкладках
    create_widgets()

    window.mainloop()


from tkinter import Tk, Label


# клик по кнопке "О программе"
def about_program():
    small_window = Tk()
    small_window.title('О программе')
    small_window.geometry('420x240')
    about_lst = ['Программа проверки кандидатов', 'Используются открытые данные органов власти',
                 'Также используются внутренние источники', 'Автор: wsemenenko@gmail.com',
                 'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_lst)):
        Label(small_window, text=f'{about_lst[i]}', font=('Arial', 10), pady=5).pack()

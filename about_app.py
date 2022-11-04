from tkinter import Toplevel
from app_window import MainWindow


class AboutWin(Toplevel, MainWindow):
    def __init__(self):
        super().__init__()
        self.title('О программе')
        self.geometry('360x180')

# клик по кнопке "О программе"
def about_program():
    aw = AboutWin()
    about_txt = ['Программа "Кадровая безопасность"', 'Разработка: wsemenenko@gmail.com', 'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_txt)):
        aw.create_labeles(f"{about_txt[i]}", ('Arial', 10), 45, 'center', 0, 5, i, 0)

# клик по кнопке "О программе в БД"
def about_db_pro():
    aw = AboutWin()
    about_txt = ['Программа "БД - Кадровая безопасность"', 'Разработка: wsemenenko@gmail.com', 'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_txt)):
        aw.create_labeles(f"{about_txt[i]}", ('Arial', 10), 45, 'center', 0, 5, i, 0)
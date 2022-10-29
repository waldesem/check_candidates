from tkinter import Toplevel, StringVar
from app_window import MainWindow

class LoginWin(Toplevel, MainWindow):
    def __init__(self):
        super().__init__()
        self.title('Вход в базу данных')
        self.geometry('380x120')

	
# login button check
def check_login():
    pass

# login window
def user_login():
    lw = LoginWin()
    # #username label and text entry box
    lw.create_labeles("Пользователь", ('Arial', 10), 15, 'w', 5, 5, 0, 0)
    username = StringVar()
    lw.create_entries(username, 30, None, 0, 1)  
    #password label and password entry box
    lw.create_labeles("Пароль", ('Arial', 10), 15, 'w', 5, 5, 1, 0)
    password = StringVar()
    lw.create_entries(password, 30, '*', 1, 1)  
    #login/cancel button
    lw.create_buttons("Вход", check_login, 2, 0)
    lw.create_buttons("Отмена", lw.destroy, 2, 1)  

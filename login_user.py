from tkinter import Tk, StringVar, messagebox as mb
from main_gui import Window
import check_info

# login button check
def check_login():
    usr = username.get()
    passwd = password.get()
    connect = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/user_db.db'
    query = "SELECT * FROM user_db WHERE login like " + "'" + usr + "'" + ' and password like ' + "'" + passwd + "'"
    resp = True
    noresp = 'messagebox.showinfo(title="Ошибка", message="Неверный логин или пароль")'
    return check_info.db_response(connect, query, resp, noresp)

# login window
window = Tk()
lw = Window
#username and password window
lw(window,'Вход в систему', '380x120')
#username label and text entry box
lw.create_labeles(window, "Пользователь", 15, 'w', 5, 5, 0, 0)
username = StringVar()
lw.create_entries(window, username, None, 0, 1)  
#password label and password entry box
lw.create_labeles(window, "Пароль", 15, 'w', 5, 5, 1, 0)
password = StringVar()
lw.create_entries(window, password, '*', 1, 1)  
#login/cancel button
lw.create_buttons(window, "Вход", check_login, 2, 0)
lw.create_buttons(window, "Отмена", window.destroy, 2, 1)  

window.mainloop()
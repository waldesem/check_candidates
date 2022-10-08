from tkinter import Tk, Label, Entry, StringVar, Button, messagebox as mb
import sqlite3

auth = None

def validateLogin():
    usr = username.get()
    passwd = password.get()
    global auth
    try:
        sqlite_connection = sqlite3.connect('/home/semenenko/MyProjects/Python/Staff_check/DB_check/user_db.db')
        cursor_obj = sqlite_connection.cursor()
        cursor_obj.execute("SELECT * FROM user_db WHERE login like " + "'" + usr + "'" + ' and password like ' 
                            + "'" + passwd + "'")
        record = cursor_obj.fetchall()
        try:
            if record[0][0] == usr and record[0][1] == passwd:
                auth = True
                window.destroy()
        except IndexError:
            mb.showinfo(title="Ошибка", message="Неверный логин или пароль")
        cursor_obj.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return auth
      
#window
window = Tk()  
window.geometry('380x120')  
window.title('Вход в систему проверки')

#username label and text entry box
usernameLabel = Label(window, text="Пользователь", font=('Arial', 10), padx=5, pady=5).grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(window, textvariable=username).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(window,text="Пароль", font=('Arial', 10), padx=5, pady=5).grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(window, textvariable=password, show='*').grid(row=1, column=1)  

#login button
loginButton = Button(window, text="Вход", command=validateLogin, padx=5, pady=5).grid(row=4, column=0)
exitButton = Button(window, text="Отмена", command=window.destroy, padx=5, pady=5).grid(row=4, column=1)  

window.mainloop()


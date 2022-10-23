from tkinter import Toplevel, StringVar, Button, Label, Entry


class LoginWin(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Вход в базу данных')
        self.geometry('380x120')
    
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
    
    def create_entries(self, textvariable, width, show, row, column):
        self.textvariable = textvariable
        self.width = width
        self.show = show
        self.row = row
        self.column = column
        Entry(self, textvariable=textvariable, width=width, show=show).grid(row=row, column=column)  

    def create_buttons(self, text, command, row, column):
        self.textvariable = text
        self.command = command
        self.row = row
        self.column = column
        Button(self, text=text, command=command).grid(row=row, column=column)
	
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

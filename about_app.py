from tkinter import Toplevel, Label

class AboutWin(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('О программе')
        self.geometry('360x180')
    
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

# клик по кнопке "О программе"
def about_program():
    aw = AboutWin()
    about_txt = ['Программа "Кадровая безопасность"', 'Разработка: wsemenenko@gmail.com', 'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_txt)):
        aw.create_labeles(f"{about_txt[i]}", ('Arial', 10), 45, 'center', 0, 5, i, 0)
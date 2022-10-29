from tkinter import Button, Label, Entry

class MainWindow:
    def __init__(self, master, title, geometry):
        self.master = master
        self.title = title
        self.geometry = geometry
        master.title(title)
        master.geometry(geometry)
    
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

    def create_buttons(self, text, command, row, column):
        self.textvariable = text
        self.command = command
        self.row = row
        self.column = column
        Button(self, text=text, command=command).grid(row=row, column=column)

    def create_entries(self, textvariable, width, show, row, column):
        self.textvariable = textvariable
        self.width = width
        self.show = show
        self.row = row
        self.column = column
        Entry(self, textvariable=textvariable, width=width, show=show).grid(row=row, column=column)  
    
    def create_menu(self, label, command, menu):
        self.menu = menu
        self.label = label
        self.command = command
        menu.add_command(label=label, font=('Arial', 10), command=command)
        self.config(menu=menu)
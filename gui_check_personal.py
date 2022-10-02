# графический интерфейс для проверки кандидатов на работу
from tkinter import Tk, Label, Menu, ttk
import about_me
import check_main
import menu_download
import menu_upload
import login


class MainApp:
    def __init__(self, master):
        self.response_all = None
        self.anketa_response = None
        self.master = master
        self.master.title('Проверка кандидата на работу в Банк')
        self.master.geometry('960x780')

        # окно сообщений
        self.master.option_add('*Dialog.msg.font', 'Arial 10')

        # панель меню
        self.menu = Menu(master)

        # панель вкладок
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('Arial', 10))
        self.tab_control = ttk.Notebook(master)

        # вкладка анкеты
        self.tab_anketa = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_anketa, text='Анкета кандидата')
        self.tab_control.pack(expand=1, fill='both')

        # вкладка проверки
        self.tab_check = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_check, text='Проверка кандидата')
        self.tab_control.pack(expand=1, fill='both')

        # создаем виджеты и команды в меню
        self.command_lst = [self.click_upload, self.click_check,
                            menu_download.download_file, about_me.about_program]
        self.menu_label_lst = ['Загрузить анкету', 'Начать проверку', 'Получить заключение', 'О программе']
        for n in range(len(self.command_lst)):
            self.menu.add_command(label=self.menu_label_lst[n], font=('Arial', 10), command=self.command_lst[n])
            self.master.config(menu=self.menu)

        # создаем название виджетов на вкладке Анкета
        for i in range(len(menu_upload.anketa_labeles)):
            Label(self.tab_anketa, text=f"{menu_upload.anketa_labeles[i]}", font=('Arial', 10), width=20, anchor='w',
                  padx=8, pady=5).grid(sticky="w", column=0, row=i)

        # создаем название виджетов на вкладке результатов проверки
        self.txt_chk = ['Проверка статуса самозанятого', 'Проверка ИНН', 'Проверка по списку кандидатов',
                        'Проверка по списку дисквалифиции', 'Проверка паспорта']
        for i in range(len(self.txt_chk)):
            Label(self.tab_check, text=f"{self.txt_chk[i]}", font=('Arial', 10), width=40, anchor='w',
                  padx=8, pady=5).grid(sticky="w", column=0, row=i)

    # запуск по кнопке "Загрузить анкету"
    def click_upload(self):
        self.anketa_response = menu_upload.upload()
        # анкетные данные на вкладке Анкета
        for k in range(len(self.anketa_response)):
            Label(self.tab_anketa, text=self.anketa_response[k], font=('Arial', 10), width=100, anchor='w',
                  padx=8, pady=5).grid(sticky="w", column=1, row=k)

    # запуск по кнопке "Проверить кандидата"
    def click_check(self):
        self.response_all = check_main.check()
        for m in range(len(self.response_all)):
            Label(self.tab_check, text=self.response_all[m], font=('Arial', 10), width=100, anchor='w',
                  padx=8, pady=5).grid(sticky="w", column=1, row=m)

if __name__ == "__main__":
    if login.auth is True:
        root = Tk()
        app = MainApp(root)
        root.mainloop()

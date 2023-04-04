import tkinter
import tkinter.messagebox
import sqlite3

class EmployeeDetails:
    """Создание класса сотрудника"""
    def __init__(self):
        # Создать главное окно
        self.main_window = tkinter.Tk()
        # Скомпановать содержимое главного окна
        self.__build_main_window()
        # Запуститить главный цикл
        tkinter.mainloop()
    def __build_main_window(self):
        # Создать надпись с полдсказкой для пользователя
        self.__create_promt_label()

        # Скомпановать рамку виджета
        self.__build_listbox_frame()

        # Создать кнопку выйти
        self.__create_quit_button()

    def __create_promt_label(self):
        '''Создать надпись с подсказкой для пользователя'''
        self.employee_promt_label = tkinter.Label(self.main_window,
                                                  text='Выберите сотрудника')
        self.employee_promt_label.pack(side='top', padx=5, pady=5)

    def __build_listbox_frame(self):
        # создание рамки
        self.listbox_frame = tkinter.Frame(self.main_window)
        # натсроить виджет
        self.__setup_listbox()
        # создать полоску прокрутки
        self.__create_scrollbar()
        # заполнить виджет
        self.__populate_listbox()
        # упаковать рамку виджета
        self.listbox_frame.pack()

    def __setup_listbox(self):
        # Создать виджет Listbox
        self.employee_listbox = tkinter.Listbox(self.listbox_frame,
                                                selectmode=tkinter.SINGLE, height=6)
        #
        self.employee_listbox.bind('<<ListboxSelect>>', self.__get_details)
        self.employee_listbox.pack(side='left', padx=5, pady=5)

    def __create_scrollbar(self):
        self.scrollbar = tkinter.Scrollbar(self.listbox_frame,
                                           orient=tkinter.VERTICAL)
        self.scrollbar.config(command=self.employee_listbox.yview)
        self.employee_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill=tkinter.Y)

    def __populate_listbox(self):
        for employee in self.__get_employees():
            self.employee_listbox.insert(tkinter.END, employee)

    def __create_quit_button(self):
        self.quit_button = tkinter.Button(self.main_window,
                                          text='Выйти',
                                          command=self.main_window.destroy)
        self.quit_button.pack(side='top',padx=10, pady=5)

    def __get_employees(self):
        employee_list = []
        conn = None
        try:
            conn = sqlite3.connect('employees.db')
            cur = conn.cursor()
            cur.execute('SELECT Name FROM Employees')
            employee_list = [n[0] for n in cur.fetchall()]
        except sqlite3.Error as err:
            tkinter.messagebox.showinfo('Ошибка базы данных', err)
        finally:
            if conn != None:
                conn.close()
            return employee_list

    def __get_details(self, event):
        listbox_index = self.employee_listbox.curselection()[0]
        select_emp = self.employee_listbox.get(listbox_index)

        conn = None
        try:
            conn = sqlite3.connect('employees.db')
            cur = conn.cursor()

            cur.execute(
                """SELECT
                Employees.Name,
                Employees.Position,
                Departments.DepartmentName,
                Locations.City
                FROM
                Employees, Departments, Locations
                WHERE
                Employees.Name == ? AND
                Employees.DepartmentID = Departments.DepartmentID AND
                Employees.LocationID == Locations.LocationID""", (select_emp, )
            )
            result = cur.fetchone()
            self.__display_details(name=result[0], position=result[1], department=result[2],
                                   location=result[3])
        except sqlite3.Error as err:
            tkinter.messagebox.showinfo('Ошибка базы данных', err)
        finally:
            if conn != None:
                conn.close()

    def __display_details(self, name, position, department, location):
        tkinter.messagebox.showinfo('Информация о сотруднике',
                                    'Имя: ' + name +
                                    '\nДолжность: ' + position +
                                    '\nОтдел' + department +
                                    '\nМесторасположение: ' + location)

if __name__ == '__main__':
    employee_details = EmployeeDetails()




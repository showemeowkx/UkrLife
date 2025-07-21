'''IMPORTS'''
#імпорт модулю для функцій, які сильно взаємодіють з інтерпретатором
import sys
#імпорт бібліотеки для роботи з файлами
import os
#імпорт функції для генерації рандомного числа
from random import randint 
#імпорт оператора дати для подальшої роботи
from datetime import date
#імпорт бібліотеки для роботи з файлами типу ui
from PyQt5 import uic, QtGui, QtCore, QtSql
#імпорт всіх потрібних елементів для створення інтерфейсу PyQt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QCalendarWidget, QFrame, QInputDialog, QMessageBox, QListWidgetItem, QListView, QComboBox, QAbstractItemView
from PyQt5.QtCore import Qt, QTimer
#імпорт бібліотеки для роботи з базами даних
import sqlite3
#імпорт бібліотеки для роботи з json-файлами
import json


#клас описує головне вікно. наслідується від класу QMainWindow
class MainWin(QMainWindow):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__() #виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_main.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        quotes = ["Тільки не розкисати." ,"Коли проблеми тягнуть вниз, дивись вгору.", "Забути погане – значить впустити хороше.", 
          "На що налаштуєшся – так і зазвучить.", "Не здавайтесь!", "Не поспішайте.", "Відчуйте страх і зробіть це все одно.",
          "Найкраще ще попереду.", "Ніколи не припиняйте мріяти.", "Не мрійте про своє життя, живіть своєю мрією.", "Ніщо не вічне.",
          "Без дощу. Ні квітів.", "Колекціонуйте миттєвості, а не речі.", "Це теж пройде.", "Ви дивовижний! Пам'ятайте це."] #список фраз, які будуть з'являтися на головному екрані
        self.lb_quote.setText(quotes[randint(0, (len(quotes)-1))]) #вибирає випадковий елемент списку quotes та надає його значення тексту елемента lb_qoute
        self.setStyleSheet(open("styles/main_style.css").read()) #підключення css-стилю

        '''CONNECTIONS'''
        self.b_diary.clicked.connect(self.diary_open) #при натисканні на кнопку "Щоденник" виконується функція diary_open
        self.b_notes.clicked.connect(self.notes_open)
        self.b_finance.clicked.connect(self.finance_open)
        self.b_memory.clicked.connect(self.memory_open)

    '''METHODS'''
    #відкриває вікно з інтерфейсом щоденника, закриває основне меню
    def diary_open(self):
        self.hide()
        win_diary.show()

    #відкриває вікно з інтерфейсом заміток, закриває основне меню 
    def notes_open(self):
        self.hide()
        win_notes.show()

    #відкриває вікно з інтерфейсом фінансів, закриває основне меню 
    def finance_open(self):
        self.hide()
        win_finance.show()

    #відкриває вікно з інтерфейсом гри на тренування пам'яті, закриває основне меню 
    def memory_open(self):
        self.hide()
        #блокує ігрові кнопки
        for btn in win_memory.btns:
            btn.setDisabled(True)
        win_memory.show()


#клас описує вікно з інтерфейсом щоденника. наслідується від класу QWidget
class DiaryWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_diary.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/diary_style.css").read()) #підключення css-стилю
        self.calendar_func() #викликає функцію, що записує вибрану дату та оновляє список активностей
        self.calendar.setSelectedDate(date.today()) #показує сьогоднішню дату на віджеті календара
        self.b_act_del.setDisabled(True) #робить кнопку видалення активності недоступною
        
        '''CONNECTIONS'''
        self.b_goback.clicked.connect(self.goback) #при натисканні на кнопку "Повернутися назад"(<-) виконується функція goback
        self.b_act_add.clicked.connect(self.act_menu) #при натисканні на кнопку "Додати активність"(+) виконується функція act_menu
        self.b_act_del.clicked.connect(self.act_del) #при натисканні на кнопку "Видалити активність"(смітник) виконується функція act_del
        self.b_plan_save.clicked.connect(self.plan_save) #при натисканні на кнопку "Зберегти зміни" виконується функція plan_save
        self.calendar.selectionChanged.connect(self.calendar_func) #при зміні вибраної дати на календарі виконується функція calendr_func
        self.lst_diary.currentRowChanged.connect(self.lst_func) #при зміні вибраного елемента списку виконується функція lst_func

    '''METHODS'''
    #функція-обробник взаємодії з календарем
    def calendar_func(self):
        date_chosen = self.calendar.selectedDate().toPyDate().strftime("%d.%m.%Y") #запис вибраної дати, конвертованої у тип даних PyDate, у форматі день.місяць.повний рік
        self.lst_update(date_chosen) #оновлює спсок щоденника, відповідно до обраної дати

    #записує вибраний у списку елемент до змінної
    def lst_func(self):
        if self.lst_diary.currentRow() >= 0:
            self.b_act_del.setDisabled(False) #розблокує кнопку видалення елементу
            self.chosen = self.lst_diary.currentItem().text()

    #оновлює інформацію списку. у фунцію передається оператор self та змінна, що містить обрану на календарі дату date_chosen
    def lst_update(self, date_chosen):
        self.lst_diary.clear() #очищує список щоденника
        diarybase = sqlite3.connect("data/diary/diary.db") #підключає базу даних
        diaryCursor = diarybase.cursor() #створює курсор
        req  = '''SELECT task, done FROM diary WHERE date = ?''' #вибирає всі елементи бази даних, у яких дата = вибраній дані
        row = (date_chosen,) #корсет зі значенням обраної дати
        results = diaryCursor.execute(req, row).fetchall() #курсор виконує запит та результат заноситься в список results за допомогою метода fetchall
        #цикл проходить по всім елементам списку results
        for r in results:
            task = QListWidgetItem(str(r[0])) #елемент списку з індексом 0 несе в собі назву активності, яку коневртуємо в елемент списку та заносимо в змінну task
            task.setFlags(task.flags() | Qt.ItemIsUserCheckable) #призначаємо елементові прапорець
            #перевіряє значення елементу з індексом 1, який несе в собі статус прарорця
            if r[1] == "True": #якщо значення - True, то...
                task.setCheckState(Qt.Checked) #переводить прапорець у статус вибраного
            elif r[1] == "False": #якщо значення - False, то...
                task.setCheckState(Qt.Unchecked) #переводить прапорець у статус не вибраного
            self.lst_diary.addItem(task) #додає елемент до списку

    #обробляє статуси прапорців та зберігає у базу даних
    def plan_save(self):
        diarybase = sqlite3.connect("data/diary/diary.db") #підключає базу даних
        diaryCursor = diarybase.cursor() #створює курсор
        date = self.calendar.selectedDate().toPyDate().strftime("%d.%m.%Y") #запис вибраної дати, конвертованої у тип даних PyDate, у форматі день-місяць-повний рік
        #цикл повторюється для всіх елементів списку щоденника
        for i in range(self.lst_diary.count()):
            item = self.lst_diary.item(i) #зберігає елемнт списку з індексом значення і до змінної
            task = item.text() #зберігає текст елемента до змінної
            #перевіряє статус прапорця елемента
            if item.checkState() == Qt.Checked: #якщо статус прапорця - вибраний, то...
                req = '''UPDATE diary SET done = 'True' WHERE task = ? AND date = ?''' #оновлює значення колонки done на True для вибраного елемента
            else: #інакше...
                req = '''UPDATE diary SET done = 'False' WHERE task = ? AND date = ?''' #оновлює значення колонки done на False для вибраного елемента
            row = (task, date,) #корсет зі значенням назви елементу та обраної дати
            diaryCursor.execute(req, row) #курсор виконує запит
        diarybase.commit() #запис даних до бази

        msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Дані збережено!") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням

    #відкриває основне вікно, закриває вікно щоденника
    def goback(self):
        self.close()
        win_act.close()
        win.show()

    #відкриває меню активностей
    def act_menu(self):
        #перевірка, чи вже відкрите вікно
        if win_act.opened == False: 
            win_act.show()
            win_act.opened == True
        else: pass

    #видаляє елемент зі списку щоденника
    def act_del(self):
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Видалити активність?") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням
        returnValue = msgBox.exec() #фіксує відповідь користувача
        act_names = [] #створює список для подальших дій 
        if returnValue == QMessageBox.Yes: #якщо натиснута кнопка "Yes", то...
            #цикл повторюється для всіх елементів списку щоденника 
            for i in range(self.lst_diary.count()):
                item = self.lst_diary.item(i).text() #записує назву елементу в змінну
                act_names.append(item) #додає змінну до списку назв активностей
            diarybase = sqlite3.connect("data/diary/diary.db") #підключає базу даних
            diaryCursor = diarybase.cursor() #створює курсор
            date = self.calendar.selectedDate().toPyDate().strftime("%d.%m.%Y") #запис вибраної дати, конвертованої у тип даних PyDate, у форматі день-місяць-повний рік
            act_id = self.lst_diary.currentRow() + 1 #записує ідентифікатор елемента в змінну за допомогою індекса вибраного рядка списку щоденника. додається 1, тому що лічба в спискі починається з 0
            act_names.pop(act_id - 1) #видаляє зі списку назв активностей елемент з відповідним ідентифікатором
            req = '''DELETE FROM diary WHERE date = ? AND ID = ?''' #видаляє з бази даних елемент з відповідним ідентифікатором та датою
            row = (date, act_id,) #корсет зі значенням дати та ідентифікатора 
            diaryCursor.execute(req, row) #курсор виконує запит
            #кількість повторень циклу залежить від довжини списку з назвами активностей
            for i in range(len(act_names)):
                req = '''UPDATE diary SET ID = ? WHERE task = ? AND date = ?''' #оновлює ідентифікатор елементу
                row = (i+1, act_names[i], date,) #корсет зі значенням нового ідентифікатора(додається 1, тому що лічба для і починається з 0), назви елемента, вибраної дати
                diaryCursor.execute(req, row) #курсор виконує запит
            diarybase.commit() #запис даних до бази
            self.lst_update(date) #оновлює список щоденника
            self.chosen = None
            self.btnCheck()
        else: pass #інкаше - пропускаємо дію

    #при спробі закрити вікно щоденника закриватиметься меню активностей
    def closeEvent(self, event):
        self.close()
        win_act.close()

    #перевіряє вибраний елемент та робить віджети доступними
    def btnCheck(self):
        if self.chosen == None:
            self.b_act_del.setDisabled(True) #робить кнопку видалення активності недоступною


#клас описує вікно з інтерфейсом меню активностей. наслідується від класу QWidget
class ActWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_activities.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/act_style.css").read()) #підключення css-стилю
        self.opened = False #прапорець для перевірки, чи відкрите вікно
        self.b_act_remove.setDisabled(True) #робить кнопку видалення активності недоступною
        self.b_act_use.setDisabled(True) #робить кнопку використання активності недоступною
        self.lst_act.clear() #очищує віджет списку активностей
        #відкриває json-файл для прочитання
        with open("data/diary/activities.json", "r") as act_file:
            act_data = json.load(act_file) #записує дані з файлу в список
        self.lst_act.addItems(act_data) #додає елементи до списку

        '''CONNECTIONS'''
        self.b_act_create.clicked.connect(self.act_create) #при натисканні на кнопку "Створити активність"(+) виконується функція act_create
        self.b_act_remove.clicked.connect(self.act_remove) #при натисканні на кнопку "Видалити активність"(смітник) виконується функція act_remove
        self.b_act_use.clicked.connect(self.act_use) #при натисканні на кнопку "Використати активність" виконується функція act_use
        self.lst_act.currentRowChanged.connect(self.lst_func) #при зміні вибраного елемента списку виконується функція lst_func

    '''METHODS'''
    #реагує на спробу закрити вікно та перемикає прапорець
    def closeEvent(self, event):
        self.opened = False

    #записує вибраний у списку елемент до змінної
    def lst_func(self):
        if self.lst_act.currentRow() >= 0:
            self.b_act_remove.setDisabled(False) #розблокує кнопку видалення елементу
            self.b_act_use.setDisabled(False) #розблокує кнопку використання елементу
            self.chosen = self.lst_act.currentItem().text()

   #створює нову активність
    def act_create(self):
        act_name, ok = inputDialog.getText(inputDialog, " ", "Введіть назву активності:")  #відкриває діалогове вікно та фіксує введену інформацію
        #відкриває json-файл для прочитання
        with open("data/diary/activities.json", "r") as act_file:
            act_data = json.load(act_file) #записує дані з файлу в список
        #фіксує завершення роботи діалогового вікна при натисканні на кнопку "Ок", перевіряє правильність написання назви
        if ok and act_name != "" and act_name != " ": 
            #перевіряє наявність введеної назви у даних
            if act_name in act_data: #якщо елемент знайдено, то...
                    msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                    msgBox.setText("Активність з такою\nназвою вже існує!") #змінює текст повідомлення
                    msgBox.show() #показує вікно з повідомленням
            else: #якщо елемент не знайдено, то...
                act_data.append(act_name) #додає до списку введений користувачем елемент
                #відкриває json-файл для переписання
                with open("data/diary/activities.json", "w") as act_file:
                    json.dump(act_data, act_file) #переписує json-файл, заміняє новими даними 
                self.lst_act.addItem(act_name) #додає елемент до списку активностей

    #прибирає вибраний елемент зі списку та з json-файлу
    def act_remove(self):
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Видалити активність?") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням
        returnValue = msgBox.exec() #фіксує відповідь користувача
        if returnValue == QMessageBox.Yes: #якщо натиснута кнопка "Yes", то...
            #відкриває json-файл для прочитання
            with open("data/diary/activities.json", "r") as act_file:
                act_data = json.load(act_file) #записує дані з файлу в список
            act_data.remove(self.chosen) #видаляє вибраний елемент зі списку
            #відкриває json-файл для переписання
            with open("data/diary/activities.json", "w") as act_file:
                json.dump(act_data, act_file) #переписує json-файл, заміняє новими даними 
            self.lst_act.clear() #очищує віджет списку активностей
            self.lst_act.addItems(act_data) #заносить до списку нові дані
            self.chosen = None
            self.btnCheck()
        else: pass

    #бере елемент списку активностей та заносить його до списку щоденника
    def act_use(self):
        diarybase = sqlite3.connect("data/diary/diary.db") #підключає базу даних
        diaryCursor = diarybase.cursor() #створює курсор
        date = win_diary.calendar.selectedDate().toPyDate().strftime("%d.%m.%Y") #запис вибраної дати, конвертованої у тип даних PyDate, у форматі день-місяць-повний рік
        act_names = [] #створює список для подальших дій 
        req = '''SELECT COUNT(task) FROM diary WHERE date = ?''' #рахує кількість елементів бази даних, що мають однакове значення дати
        row = (date,) #корсет зі змінною вбраної дати
        idValue = diaryCursor.execute(req, row).fetchall() #курсор виконує запит та результат заноситься в список idValue за допомогою метода fetchall
        act_id = str(idValue[0]) #записує перший елемент списку в змінну ідентифікатора елемента
        #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
        act_id = act_id.replace("(", "") #заміняє символ "(" на пустий 
        act_id = act_id.replace(")", "") #заміняє символ ")" на пустий
        act_id = act_id.replace(",", "") #заміняє символ "," на пустий
        act_id = eval(act_id) + 1 #записує остаточний індентифікатор нового елемента(використовується метод eval, щоб надати формату строки змогу проводити над ним обчислення; додаємо 1, так як елемент новий і потрібно дати йому новий ідентифікатор)
        req = '''INSERT INTO diary(task, done, date, ID) VALUES(?,?,?,?)''' #створює новий елемент в базі даних
        #цикл повторюється для всіх елементів списку щоденника
        for i in range(win_diary.lst_diary.count()):
            item = win_diary.lst_diary.item(i).text() #записує назву елементу в змінну
            act_names.append(item) #додає змінну до списку назв активностей
        #перевіряє наявність вибраної активності у списку назв вже існуючих одиниць
        if self.chosen in act_names: #якщо такий елемент знайдено, то...
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Активність з такою назвою\nвже записана у плані!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням
        else: #інакше...
            row = (self.chosen, "False", date, act_id) #корсет зі значеннями назви нового елементу, статусу прапорця(за змовчуванням False), вибраної дати, ідентифікатора нового елементу
            diaryCursor.execute(req, row) #курсор виконує запит
            diarybase.commit() #запис даних до бази
            win_diary.lst_update(date) #оновлює список щоденника відповідно до вибраної дати
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Активність успішно додано!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням

    #перевіряє вибраний елемент та робить віджети доступними
    def btnCheck(self):
        if self.chosen == None:
            self.b_act_remove.setDisabled(True) #робить кнопку видалення активності недоступною
            self.b_act_use.setDisabled(True) #робить кнопку використання активності недоступною


#клас описує вікно з інтерфейсом меню заміток. наслідується від класу QWidget
class NotesWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_notes.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/notes_style.css").read()) #підключення css-стилю
        self.lst_notes_update() #оновлює список заміток
        self.notes_txtEdit.setDisabled(True) #робить основне текстове поле недоступним
        self.b_note_delete.setDisabled(True) #робить кнопку видалення замітки недоступною
        self.b_note_save.setDisabled(True) #робить кнопку збереження замітки недоступною
        self.lst_tags.setDisabled(True) #робить список тегів недоступним
        self.b_tag_pin.setDisabled(True) #робить кнопку прикріплення тегу недоступною
        self.b_tag_unpin.setDisabled(True) #робить кнопку відкріплення тегу недоступною
        self.b_tag_search.setDisabled(True) #робить кнопку пошуку по тегу недоступною

        '''CONNECTIONS'''
        self.b_goback.clicked.connect(self.goback) #при натисканні на кнопку "Повернутися назад"(<-) виконується функція goback
        self.b_note_create.clicked.connect(self.note_create) #при натисканні на кнопку "Створити замітку"(+) виконується функція note_create
        self.b_note_delete.clicked.connect(self.note_delete) #при натисканні на кнопку "Видалити замітку"(смітник) виконується функція note_delete
        self.b_note_save.clicked.connect(self.note_save) #при натисканні на кнопку "Зберегти замітку"(дискета) виконується функція note_save
        self.b_tag_pin.clicked.connect(self.tag_pin) #при натисканні на кнопку "Додати тег"(канцелярська кнопка) виконується функція tag_pin
        self.b_tag_unpin.clicked.connect(self.tag_unpin) #при натисканні на кнопку "Вилучити тег"(переклеслена канцелярська кнопка) виконується функція tag_unpin
        self.b_tag_search.clicked.connect(self.tag_search) #при натисканні на кнопку "Пошук по тегу"(лупа) виконується функція tag_search
        self.lst_notes.currentRowChanged.connect(self.lst_notes_func) #при зміні вибраного елемента списку виконується функція lst_notes_func
        self.searchLine.textChanged.connect(self.lst_tags_func) #при зміні тексту в полі для вводу виконується функція lst_tags_func

    '''METHODS'''
    #відкриває основне вікно, закриває вікно заміток
    def goback(self):
        self.close()
        win.show()

    #створює нову замітку
    def note_create(self):
        note_name, ok = inputDialog.getText(inputDialog, ' ', "Введіть назву замітки") #відкриває діалогове вікно та фіксує введену інформацію
        #відкриває json-файл для прочитання
        with open("data/notes/notes.json", "r") as note_file:
            notes = json.load(note_file) #записує дані з файлу в змінну
        #фіксує завершення роботи діалогового вікна при натисканні на кнопку "Ок", перевіряє правильність написання назви
        if ok and note_name != "" and note_name != " ":
            #перевіряє наявність введеної назви в спискові
            if note_name not in notes: #якщо такого елементу не знайдено, то...
                    #перевіряє кількість елемнтів у списку заміток
                    if self.lst_notes.count()-1 >=0: #якщо більше 0, то...
                        self.lst_notes.setCurrentRow(self.lst_notes.count()-1) #виставляє останній рядок на списку заміток
                        lastItem = self.lst_notes.currentItem().text() #записує текст елменту до зиінної
                        last_fileName = notes[lastItem][0] #бере значення імені файла останнього елемента списку заміток
                        #(пояснення: структура даних заміток вигляає як json файл з інформацією про назву самої замітки, тегів, а також назви txt-файлу, що містить текст замітки. визначається назва останнього файла для того, щоб назви не були однаковими та замітки можна було називате кирилицею)
                        note_fileName = str(eval(last_fileName)+1) #створення нової назви файлу шляхом зміни номера на +1
                    else: #інакше
                        note_fileName = str(1) #надає назві нового файлу значення 1
                    note = {note_name : [note_fileName, []]} #створення словника для подальшого додавання в json
                    notes.update(note) #додавання нової частини у повний словник
                    open("data/notes/files/"+str(note_fileName)+".txt", "x") #створення файла замітки з новим ім'ям
                    #відкриває json-файл для переписання
                    with open("data/notes/notes.json", "w") as note_file:
                        json.dump(notes, note_file) #переписує json-файл, заміняє новими даними 
                    self.lst_notes_update() #оновлює список заміток
                    self.chosen = None #надає значення None змінній вибраного елемента в спискі заміток
                    self.btnCheck() #блокує деякі віджети
            else: #інакше...
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Замітка з такою назвою\nвже існує!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
                
    #видаляє замітку зі списку заміток та json-файлу
    def note_delete(self):
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Видалити замітку?") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням
        returnValue = msgBox.exec() #фіксує відповідь користувача
        if returnValue == QMessageBox.Yes: #якщо натиснута кнопка "Yes", то...
            #відкриває json-файл для прочитання
            with open("data/notes/notes.json", "r") as notes_file:
                notes = json.load(notes_file) #записує дані з файлу в змінну
            os.remove("data/notes/files/"+str(notes[self.chosen][0])+".txt") #видаляє файл з відповідним до вибраної замітки ім'ям
            notes.pop(self.chosen) #видаляє замітку зі словника
            #відкриває json-файл для переписання
            with open("data/notes/notes.json", "w") as notes_file:
                json.dump(notes, notes_file) #переписує json-файл, заміняє новими даними 
            self.lst_notes_update() #оновлює список заміток
            self.notes_txtEdit.setText('') #очищає основне текстове поле
            self.lst_tags.clear() #очищає список тегів
            self.chosen = None #надає значення None змінній вибраного елемента в спискі заміток
            self.btnCheck() #блокує деякі віджети
        else: pass

    #зберігає текст замітки у файл
    def note_save(self):
        txt = self.notes_txtEdit.toPlainText() #записує текст з основного текстового поля у змінну
        #відкриває json-файл для прочитання
        with open("data/notes/notes.json", "r") as notes_file:
            notes = json.load(notes_file) #записує дані з файлу в змінну
        note_fileName = str(notes[self.chosen][0]) #записує назву файлу вибраної замітки до змінної
        #відкриває txt-файл вибраної замітки для переписання
        with open("data/notes/files/"+note_fileName+".txt", "w") as note_txtFile:
            note_txtFile.writelines(str(txt)) #записує значення змінної тексту до файлу
        msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Замітку збережено!") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням
    
    #записує вибраний у списку елемент до змінної та текст замітки до основного текстового поля
    def lst_notes_func(self):
        if self.lst_notes.currentRow() >= 0:
            self.b_note_delete.setDisabled(False) #розблокує кнопку видалення елементу
            self.b_note_save.setDisabled(False) #розблокує кнопку збереження елементу
            self.notes_txtEdit.setDisabled(False) #розблокує основне текстове поле
            self.chosen = self.lst_notes.currentItem().text()
            #відкриває json-файл для прочитання
            with open("data/notes/notes.json", "r") as notes_file:
                notes = json.load(notes_file) #записує дані з файлу в змінну
            note_fileName = str(notes[self.chosen][0]) #записує назву файлу вибраної замітки до змінної
            #відкриває txt-файл вибраної замітки для прочитання
            with open("data/notes/files/"+note_fileName+".txt", "r") as note_txtFile:
                note_txt = note_txtFile.read() #записує текст файлу вибраної замітки до змінної
            self.notes_txtEdit.setText(note_txt) #записує текст замітки до основного текстового поля
            self.lst_tags_update() #оновлює список тегів

    #записує вписаний тег до змінної та блокує/розблокує деякі віджети
    def lst_tags_func(self):
        #перевіряє правильність введеного тексту
        if self.searchLine.text() != "" and self.searchLine.text() != " ":
            self.b_tag_pin.setDisabled(False) #розблокує кнопку видалення елементу
            self.b_tag_unpin.setDisabled(False) #розблокує кнопку збереження елементу
            self.b_tag_search.setDisabled(False) #розблокує кнопку пошуку по тегу
            self.tag = self.searchLine.text() #записує значення введеного тексту до змінної
        else: 
            self.b_tag_pin.setDisabled(True) #блокує кнопку видалення елементу
            self.b_tag_unpin.setDisabled(True) #блокує кнопку збереження елементу
            self.b_tag_search.setDisabled(True) #блокує кнопку пошуку по тегу
 
    #оновлює список заміток
    def lst_notes_update(self):
        self.lst_notes.clear() #очищає список заміток
        #відкриває json-файл для прочитання
        with open("data/notes/notes.json", "r") as note_file:
            notes = json.load(note_file) #записує дані з файлу в змінну
            #цикл повторюється для всіх елементів словника
            for n in notes:
                self.lst_notes.addItem(n) #додає елемент до списку заміток

    #оновлює список тегів
    def lst_tags_update(self):
        self.lst_tags.clear() #очищає список тегів
        #відкриває json-файл для прочитання
        with open("data/notes/notes.json", "r") as note_file:
            notes = json.load(note_file) #записує дані з файлу в змінну
            tags = notes[self.chosen][1] #записує список тегів в змінну
            #перевіряє, чи має вибрана замітка теги
            if tags != None: #якщо список тегів не пустий, то...
                #цикл повторюється для всіх елементів списку
                for t in tags:
                    self.lst_tags.addItem(t) #додає елемент до списку тегів

    #надає вибраній замітці тег
    def tag_pin(self):
        #робить спробу прикріпити тег до замітки
        try:
            #відкриває json-файл для прочитання
            with open("data/notes/notes.json", "r") as note_file:
                notes = json.load(note_file) #записує дані з файлу в змінну
                tags = notes[self.chosen][1] #записує список тегів в змінну
            #перевіряє наявність введеного тегу в списку тегів
            if self.tag not in tags: #якщо не знайдкно, то...
                tags.append(self.tag) #додає новий тег до списку тегів
                notes[self.chosen][1] = tags #переписує старий список тегів вибраної замітки на новий
                #відкриває json-файл для переписання
                with open("data/notes/notes.json", "w") as note_file:
                    json.dump(notes, note_file)  #переписує json-файл, заміняє новими даними 
                self.lst_tags_update() #оновлює список тегів
            else: #інакше...
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Такий тег вже існує!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
        #у випадку помилки AttributeError або KeyError(замітка не вибрана):
        except (AttributeError, KeyError):
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Виберіть замітку!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням

    #прибирає у вибраної замітки тег
    def tag_unpin(self):
        #робить спробу прикріпити тег до замітки
        try:
            #відкриває json-файл для прочитання
            with open("data/notes/notes.json", "r") as note_file:
                notes = json.load(note_file) #записує дані з файлу в змінну
                tags = notes[self.chosen][1] #записує список тегів в змінну
            #перевіряє наявність введеного тегу в списку тегів
            if self.tag in tags: #якщо знайдено, то...
                tags.remove(self.tag) #видаляє введений тег зі списку тегів
                notes[self.chosen][1] = tags #переписує старий список тегів вибраної замітки на новий
                #відкриває json-файл для переписання
                with open("data/notes/notes.json", "w") as note_file:
                    json.dump(notes, note_file) #переписує json-файл, заміняє новими даними 
                self.lst_tags_update() #оновлює список тегів
            else: #інакше...
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Такого тегу не існує!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
        #у випадку помилки AttributeError або KeyError(замітка не вибрана):
        except (AttributeError, KeyError):
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Виберіть замітку!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням

    #шукає та вибирає замітку, що містить вибраний тег
    def tag_search(self):
        #відкриває json-файл для прочитання
        with open("data/notes/notes.json", "r") as note_file:
            notes = json.load(note_file) #записує дані з файлу в змінну
            #цикл повторюється для всіх елементів словника
            for n in notes:
                #перевіряє наявність введеного тегу в елементі
                if self.tag in notes[n][1]: #якщо тег наявний, то...
                    note_tagFound = n #записує назву замітки, що містить введений тег
                    #кількість повторень цикла залежить від довжини списка заміток
                    for i in range(self.lst_notes.count()):
                        self.lst_notes.setCurrentRow(i) #вибирає по черзі кожен рядорк списку
                        #перевіряє чи текст вибраного елемента списку заміток = назві замітки, що містить введений тег
                        if self.lst_notes.currentItem().text() == note_tagFound: #якщо так, то...
                            self.chosen = self.lst_notes.currentItem().text() #записує вибраний у списку елемент до змінної
                            break #закінчує цикл
                    self.lst_notes_func() #оновлює список заміток
                    self.lst_tags_update() #оновлює список тегів

    #перевіряє вибраний елемент та робить віджети доступними
    def btnCheck(self):
        if self.chosen == None:
            self.notes_txtEdit.setDisabled(True) #робить основне текстове поле недоступним
            self.notes_txtEdit.clear() #очищає основне текстове поле
            self.b_note_delete.setDisabled(True) #робить кнопку видалення замітки недоступною
            self.b_note_save.setDisabled(True) #робить кнопку збереження замітки недоступною


#клас описує вікно з інтерфейсом меню фінансів. наслідується від класу QWidget
class FinanceWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_finance.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/finance_style.css").read()) #підключення css-стилю
        self.b_fin_edit.setDisabled(True) #робить кнопку редагування транзакції недоступною
        self.b_fin_delete.setDisabled(True) #робить кнопку видалення транзакції недоступною
        self.table_fin.clicked.connect(self.table_func) #при натисканні на таблицю записує ідентифікатор вибраного рядка таблиці
        self.data_update() #оновлює підрахунки на екрані

        '''CONNECTIONS'''
        self.b_goback.clicked.connect(self.goback) #при натисканні на кнопку "Повернутися назад"(<-) виконується функція goback
        self.b_fin_add.clicked.connect(self.trans_add) #при натисканні на кнопку "Додати транзакцію"(+) виконується функція trans_add
        self.b_settings.clicked.connect(self.settings) #при натисканні на кнопку "Налаштування"(шестреня) виконується функція settings
        self.b_fin_delete.clicked.connect(self.trans_del) #при натисканні на кнопку "Налаштування"(смітнк) виконується функція trans_del
        self.b_fin_edit.clicked.connect(self.trans_edit) #при натисканні на кнопку "Налаштування"(олівець) виконується функція trans_edit

    '''METHODS'''
    #відкриває базу даних та заносить її до таблиці
    def openDB(self):
        self.db  = QtSql.QSqlDatabase.addDatabase("QSQLITE") #створює об'єкт бази даних за допомогою QtSql 
        self.db.setDatabaseName("data/finance/finance.db") #створює базу даних
        #якщо базу даних не вдалося відкрити
        if not self.db.open():
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Не вдалося відкрити базу даних!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням
        model = QtSql.QSqlTableModel() #створює модель бази даних
        model.setTable("Finance") #змінює назву модельної таблиці
        model.select()
        self.table_fin.setModel(model) #надає таблиці модель бази даних
        self.table_fin.show() #показує таблицю

    #відкриває меню транзакцій
    def trans_add(self):
        #перевірка, чи вже відкрите вікно
        if win_trans.opened == False:
            win_trans.opened = True #перемикає прапорець відкритого вікна
            self.edit = True #перемикає прапорець редагування транзакції
            win_trans.label.setText("Нова транзакція") #змінює текст напису
            win_trans.b_trans_add.setText("Додати транзакцію") #змінює текст кнопки
            win_trans.show() #відкриває вікно
        else: pass

    #відкриває меню транзакцій
    def trans_edit(self):
        #перевірка, чи вже відкрите вікно
        if win_trans.opened == False:
            win_trans.opened = True #перемикає прапорець відкритого вікна
            self.edit = False #перемикає прапорець редагування транзакції
            win_trans.label.setText("Редагувати транзакцію") #змінює текст напису
            win_trans.b_trans_add.setText("Редагувати") #змінює текст кнопки
            win_trans.show() #відкриває вікно
        else: pass

    #видаляє транзакцію з бази даних і таблиці
    def trans_del(self):
        financebase = sqlite3.connect("data/finance/finance.db") #підключає базу даних
        finCursor = financebase.cursor() #створює курсор
        req = '''DELETE FROM finance WHERE ID = ?''' #видаляє рядок відповідно до ідентифікатора
        row = (self.chosen,) #корсет зі змінною ідентифікатора вибраної транзакції
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No) #виставляє вікну повідомлення стандартні кнопки
        msgBox.setText("Видалити транзакцію?") #змінює текст повідомлення
        msgBox.show() #показує вікно з повідомленням
        returnValue = msgBox.exec() #фіксує відповідь користувача
        if returnValue == QMessageBox.Yes: #якщо натиснута кнопка "Yes", то...
            finCursor.execute(req, row) #курсор виконує запит
            financebase.commit() #запис даних до бази
            self.openDB() #записує нову базу даних до таблиці
            self.data_update() #оновлює підрахунки на екрані
            self.index = None  #надає значення None індексу вибраного рядка в таблиці
            self.btnCheck() #блокує деякі віджети

    #відкриває налашутвання
    def settings(self):
        #перевірка, чи вже відкрите вікно
        if win_fin_set.opened == False:
            win_fin_set.opened = True
            win_fin_set.show()
        else: pass

    #оновлює підрахунки на екрані
    def data_update(self):
        #відкриває json-файл для прочитання
        with open("data/finance/settings.json", "r") as set_file:
            settings = json.load(set_file) #записує дані з файлу в змінну
        self.currency = settings["currency"] #записує значення елемента currency в змінну
        self.balance = settings["balance"] #записує значення елемента balance в змінну
        allTrans = [] #список для всіх транзакцій
        incTrans = [] #список для доходів 
        outTrans = [] #список для витрат 
        grocTrans = [] #список для транзакцій категорії "Продукти"
        transTrans = [] #список для транзакцій категорії "Транспорт"
        entTrans = [] #список для транзакцій категорії "Розваги"
        otherTrans = [] #список для транзакцій категорії "Інше"
        financebase = sqlite3.connect("data/finance/finance.db") #підключає базу даних
        finCursor = financebase.cursor() #створює курсор
        req = '''SELECT Баланс FROM finance'''#вибирає колонку "Баланс" з усіх елементів
        trAll = finCursor.execute(req).fetchall() #курсор виконує запит та результат заноситься в список trAll за допомогою метода fetchall
        #цикл повторюється для всіх елементів списку
        for tr in trAll:
            tr = str(tr) #конвертує елемнт в текстовий тип даних
            #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
            tr = tr.replace("(", " ")#заміняє символ "(" на пустий
            tr = tr.replace(")", " ")#заміняє символ ")" на пустий
            tr = tr.replace(",", " ")#заміняє символ "," на пустий
            tr = int(eval(tr)) #конвертує елемнт в числовий тип даних
            allTrans.append(tr) #додає елемнт в список всіх транзакцій
            #перевіряє елмент на наявність мінуса
            if "-" in str(tr): #якщо мінус присутній, то...
                tr = str(tr) #конвертує елемнт в текстовий тип даних
                tr = tr.replace("-", " ")#заміняє символ "-" на пустий
                tr = int(eval(str(tr)))#конвертує елемнт в числовий тип даних
                outTrans.append(tr)#додає елемнт в список витрат
            else: #інакше...
                tr = int(eval(str(tr))) #конвертує елемнт в числовий тип даних
                incTrans.append(tr)#додає елемнт в список доходів
        #робить спробу додати всі елементи списку між собою
        try: 
            allSum = sum(allTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            allSum = 0
        #робить спробу додати всі елементи списку між собою
        try:
            incSum = sum(incTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            incSum = 0
        #робить спробу додати всі елементи списку між собою
        try:
            outSum = sum(outTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            outSum = 0
        req = '''SELECT Баланс FROM finance WHERE Категорія = "Продукти"''' #вибирає всі зміни балансу з категорії "Продукти"
        groc = finCursor.execute(req).fetchall() #курсор виконує запит та результат заноситься в список groc за допомогою метода fetchall
        #цикл повторюється для всіх елементів списку
        for g in groc:
            g = str(g) #конвертує елемнт в текстовий тип даних
            #перевіряє елемент на наявність мінуса
            if "-"in g: #якщо мінус присутній, то...
                #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
                g = g.replace("(", " ") #заміняє символ "(" на пустий
                g = g.replace(")", " ") #заміняє символ ")" на пустий
                g = g.replace(",", " ") #заміняє символ "," на пустий
                g = g.replace("-", " ") #заміняє символ "-" на пустий
                g = int(eval(g)) #конвертує елемнт в числовий тип даних
                grocTrans.append(g) #додає елемнт в список витрат по категорії "Продукти"
        #робить спробу додати всі елементи списку між собою
        try:
            grocSum = sum(grocTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            grocSum = 0
        req = '''SELECT Баланс FROM finance WHERE Категорія = "Транспорт"''' #вибирає всі зміни балансу з категорії "Транспорт"
        trans = finCursor.execute(req).fetchall() #курсор виконує запит та результат заноситься в список trans за допомогою метода fetchall
        #цикл повторюється для всіх елементів списку
        for t in trans:
            t = str(t) #конвертує елемнт в текстовий тип даних
            #перевіряє елемент на наявність мінуса
            if "-"in t: #якщо мінус присутній, то...
                #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
                t = t.replace("(", " ") #заміняє символ "(" на пустий
                t = t.replace(")", " ") #заміняє символ ")" на пустий
                t = t.replace(",", " ") #заміняє символ "," на пустий
                t = t.replace("-", " ") #заміняє символ "-" на пустий
                t = int(eval(t)) #конвертує елемнт в числовий тип даних
                transTrans.append(t) #додає елемнт в список витрат по категорії "Транпорт"
        #робить спробу додати всі елементи списку між собою
        try:
            transSum = sum(transTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            transSum = 0
        req = '''SELECT Баланс FROM finance WHERE Категорія = "Розваги"''' #вибирає всі зміни балансу з категорії "Розваги"
        ents = finCursor.execute(req).fetchall() #курсор виконує запит та результат заноситься в список ents за допомогою метода fetchall
        #цикл повторюється для всіх елементів списку
        for e in ents:
            e = str(e) #конвертує елемнт в текстовий тип даних
            #перевіряє елемент на наявність мінуса
            if "-"in e: #якщо мінус присутній, то...
                #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
                e = e.replace("(", " ") #заміняє символ "(" на пустий
                e = e.replace(")", " ") #заміняє символ ")" на пустий
                e = e.replace(",", " ") #заміняє символ "," на пустий
                e = e.replace("-", " ") #заміняє символ "," на пустий
                e = int(eval(e)) #конвертує елемнт в числовий тип даних
                entTrans.append(e) #додає елемнт в список витрат по категорії "Розаги"
        #робить спробу додати всі елементи списку між собою
        try:
            entSum = sum(entTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            entSum = 0
        req = '''SELECT Баланс FROM finance WHERE Категорія = "Інше"''' #вибирає всі зміни балансу з категорії "Інше"
        others = finCursor.execute(req).fetchall() #курсор виконує запит та результат заноситься в список others за допомогою метода fetchall
        #цикл повторюється для всіх елементів списку
        for o in others:
            o = str(o) #конвертує елемнт в текстовий тип даних
            #перевіряє елемент на наявність мінуса
            if "-" in o:
                #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
                o = o.replace("(", " ") #заміняє символ "(" на пустий
                o = o.replace(")", " ") #заміняє символ ")" на пустий
                o = o.replace(",", " ") #заміняє символ "," на пустий
                o = o.replace("-", " ") #заміняє символ "-" на пустий
                o = int(eval(o)) #конвертує елемнт в числовий тип даних
                otherTrans.append(o) #додає елемнт в список витрат по категорії "Інше"
        #робить спробу додати всі елементи списку між собою
        try:
            otherSum = sum(otherTrans)
        #у випадку помилки UnboundLocalError(список пустий), сумі надається значення 0
        except UnboundLocalError:
            otherSum = 0
        curBalance = self.balance + allSum #обчислює поточний баланс
        self.lb_balance.setText(str(curBalance)+" "+self.currency) #змінює текст напису про баланс
        self.lb_income.setText(str(incSum)+" "+self.currency) #змінює текст напису про доходи
        self.lb_outcome.setText(str(outSum)+" "+self.currency) #змінює текст напису про витрати
        self.lb_groceries.setText(str(grocSum)+" "+self.currency) #змінює текст напису про витрати по категорії "Продукти"
        self.lb_entertaiment.setText(str(entSum)+" "+self.currency) #змінює текст напису про витрати по категорії "Розваги"
        self.lb_transport.setText(str(transSum)+" "+self.currency) #змінює текст напису про витрати по категорії "Транспорт"
        self.lb_other.setText(str(otherSum)+" "+self.currency) #змінює текст напису про витрати по категорії "Інше"

    #записує ідентифікатор вибраної транзакції до змінної та блокує/розблокує деякі віджети
    def table_func(self):
        if self.table_fin.selectedIndexes() != None:
            self.index = self.table_fin.selectedIndexes()[0] #фіксує індекс вибраного рядка
            self.chosen = self.table_fin.model().data(self.index)
            self.b_fin_edit.setDisabled(False) #розблокує кнопку редагування елементу
            self.b_fin_delete.setDisabled(False) #розблокує кнопку видалення елементу
        else:
            self.b_fin_edit.setDisabled(True) #блокує кнопку редагування елементу
            self.b_fin_delete.setDisabled(True) #блокує кнопку видалення елементу

    #відкриває основне вікно, закриває вікно фінансів
    def goback(self):
        self.close()
        win_act.close()
        win.show()

    #при спробі закрити вікно фінансів закриватимуться налаштування та меню транзакцій
    def closeEvent(self, event):
        self.close()
        win_trans.close()
        win_fin_set.close()

    #перевіряє вибраний елемент та робить віджети доступними
    def btnCheck(self):
        if self.index == None:
            self.b_fin_edit.setDisabled(True) #блокує кнопку редагування елементу
            self.b_fin_delete.setDisabled(True) #блокує кнопку видалення елементу


#клас описує вікно з інтерфейсом меню транзакцій. наслідується від класу QWidget
class TransWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_transaction.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/trans_style.css").read()) #підключення css-стилю
        self.opened = False #прапорець для перевірки, чи відкрите вікно
        self.dE_date.setDate(date.today()) #виставляє сьогоднішню дату на віджеті QDateEdit

        '''CONNECTIONS'''
        self.b_trans_add.clicked.connect(self.addXedit_transaction) #при натисканні на кнопку "Додати транзакцію/Редагувати" виконується функція addXedit_transaction

    '''METHODS'''
    #додає нову транзакцію до бази даних або редагує вибрану
    def addXedit_transaction(self):
        financebase = sqlite3.connect("data/finance/finance.db") #підключає базу даних
        finCursor = financebase.cursor() #створює курсор
        #перевіряє прапорець редагування транзакції
        if win_finance.edit == True: #якщо True, то...
            req = '''SELECT ID FROM finance ORDER BY ID DESC'''#вибирає значення ідентифікаторів та записує їх в порядку спадання
            lastID = finCursor.execute(req).fetchone() #курсор виконує запит та перший елемент списку заноситься в змінну lastID за допомогою метода fetchone
            lastID = str(lastID) #конвертує елемнт в текстовий тип даних
            #так як дані збереглися у вигляді корсету, для подільшої роботи необхідно "почитстити" його від деяких символів:
            lastID = lastID.replace("(", "") #заміняє символ "(" на пустий
            lastID = lastID.replace(")", "") #заміняє символ ")" на пустий
            lastID = lastID.replace(",", "") #заміняє символ "," на пустий
            #робить спробу додати до значення останнього ідентифікатора 1
            try:
                newID = eval(lastID) + 1
            #у випадку помилки TypeError(ідентифіактора не існує), надається значення 1
            except TypeError:
                newID = 1
            itemID = newID #запис нового ідентифікатора до змінної
            itemDate = self.dE_date.text() #запис вибраної дати до зінної
            itemCategorie = self.cBox_categories.currentText() #записує в змінну текст вибраного елементу на комбо-боксі категорій 
            itemDesc = self.descLine.text() #записує в змінну введений текст в поле опису
            if itemDesc == None or itemDesc == '' or itemDesc == " ": #якщо в поле нічого не вписано, то...
                itemDesc = "-" #надає змінній опису транзакції значення "-"
            itemStatus = self.cBox_status.currentText() #записує в змінну текст вибраного елементу на комбо-боксі статусу
            #перевіряє правильність написання суми
            if self.sumLine.text() != None or self.sumLine.text() != '' or self.sumLine.text() != " ": 
                itemBalance = str(self.sumLine.text()) #записує в змінну введений текст в поле суми
            #робить спробу підрахувати суму та продовжити роботу 
            try:
                itemBalance = eval(itemBalance)
                #перевіряє значення статусу
                if itemStatus == "Дохід": #якщо значення статусу - "Дохід", то...
                    itemBalance = eval(self.sumLine.text()) #записує в змінну введений текст в поле суми
                else: #інакше...
                    itemBalance = eval("- "+self.sumLine.text()) #записує в змінну введений текст в поле суми та додає попереду "-"
                req = '''INSERT INTO finance (ID, Дата, Категорія, Опис, Статус, Баланс) VALUES (?,?,?,?,?,?);''' #створює новий елемент в базі даних
                row = (itemID, itemDate, itemCategorie, itemDesc, itemStatus, itemBalance,) #корсет зі змінними, необхідними для новго елемента
                finCursor.execute(req, row) #курсор виконує запит
                financebase.commit() #запис даних до бази
                win_finance.openDB() #записує нову базу даних до таблиці
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Транзакцію додано!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
            #у випадку помилки NameError та SyntaxError(введено текст, а не число):
            except (NameError, SyntaxError):
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Суму введено невірно!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
        else: #інакше...
            itemDate = self.dE_date.text() #запис вибраної дати до зінної
            itemCategorie = self.cBox_categories.currentText() #записує в змінну текст вибраного елементу на комбо-боксі категорій
            itemDesc = self.descLine.text() #записує в змінну введений текст в поле опису
            if itemDesc == None or itemDesc == '' or itemDesc == " ": #якщо в поле нічого не вписано, то..
                itemDesc = "-" #надає змінній опису транзакції значення "-"
            itemStatus = self.cBox_status.currentText() #записує в змінну текст вибраного елементу на комбо-боксі статусу
            #перевіряє правильність написання суми
            if self.sumLine.text() != None or self.sumLine.text() != '' or self.sumLine.text() != " ":
                itemBalance = str(self.sumLine.text()) #записує в змінну введений текст в поле суми
            #робить спробу підрахувати суму та продовжити роботу 
            try:
                #перевіряє значення статусу
                itemBalance = eval(itemBalance)
                if itemStatus == "Дохід": #якщо значення статусу - "Дохід", то...
                    itemBalance = eval(self.sumLine.text()) #записує в змінну введений текст в поле суми
                else: #інакше...
                    itemBalance = eval("- "+self.sumLine.text()) #записує в змінну введений текст в поле суми та додає попереду "-"
                req = '''UPDATE finance SET Дата = ?, Категорія = ?, Опис = ?, Статус = ?, Баланс = ? WHERE ID = ?'''#оновлює дані в базі відповідно до вибраного ідентифікатора транзакції
                row = (itemDate, itemCategorie, itemDesc, itemStatus, itemBalance, win_finance.chosen,)#корсет зі змінними, необхідними для оновлення елемента та його ідентифікатор
                finCursor.execute(req, row) #курсор виконує запит
                financebase.commit() #запис даних до бази
                win_finance.openDB() #записує нову базу даних до таблиці
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Транзакцію редаговано!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
            #у випадку помилки NameError та SyntaxError(введено текст, а не число):
            except (NameError, SyntaxError):
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Суму введено невірно!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
        win_finance.data_update() #оновлює підрахунки на екрані
        win_finance.index = None #надає значення None індексу вибраного рядка в таблиці
        win_finance.btnCheck() #блокує деякі віджети

    #реагує на спробу закрити вікно та перемикає прапорець
    def closeEvent(self, event):
        self.opened = False


#клас описує вікно з інтерфейсом налаштування меню фінансів. наслідується від класу QWidgets  
class FinSetWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_fin_settings.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/settings_style.css").read()) #підключення css-стилю
        self.opened = False #прапорець для перевірки, чи відкрите вікно

        '''CONNECTIONS'''
        self.b_fin_set_save.clicked.connect(self.save_changes) #при натисканні на кнопку "Зберегти зміни" виконується функція save_changes

    '''METHODS'''
    #реагує на спробу закрити вікно та перемикає прапорець
    def closeEvent(self, event):
        self.opened = False

    #зберігає налаштування
    def save_changes(self):
        self.currency = self.cBox_curency.currentText() #записує в змінну текст вибраного елементу на комбо-боксі грошової одиниці
        self.balance = self.balanceLine.text() #записує в змінну введений текст в поле початкового балансу балансу
        #робить спробу підрахувати баланс 
        try:
            if self.balance == None or self.balance == "" or self.balance == " ": #якщо в поле нічого не введено, то...
                self.balance = 0 #надає змінній початкового балансу значення 0
            self.balance = eval(self.balance)
        #у випадку помилки NameError та TypeError(введено текст, а не число):
        except NameError or TypeError:
            self.balance = 0 #надає змінній початкового балансу значення 0
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Баланс введено невірно!") #змінює текст повідомлення
            msgBox.show() #показує вікно з повідомленням
        else:
            msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
            msgBox.setText("Зміни збережено!") #змінює текст повідомлення
            #перевіряє значення тексту вибрангого елемента комбо-боксу та надає змінній грошової одиниці відповідного значення
            if self.currency == "Долар":
                self.currency = "$"
                msgBox.show() #показує вікно з повідомленням
            elif self.currency == "Євро":
                self.currency = "€"
                msgBox.show() #показує вікно з повідомленням
            elif self.currency == "Гривня":
                self.currency = "₴"
                msgBox.show() #показує вікно з повідомленням
            elif self.currency == "Біткоін":
                self.currency = "₿"
                msgBox.show() #показує вікно з повідомленням
            else: #якщо вибрано рубль, то...
                self.currency = "$"#надає змінній грошової одиниці відповідного значення "$"
                msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
                msgBox.setText("Рубля більше не існує!\nВиберіть іншу грошову одиницю!") #змінює текст повідомлення
                msgBox.show() #показує вікно з повідомленням
            new_settings = {"currency" : str(self.currency), "balance" : self.balance} #створює словник з новими данними
            #відкриває json-файл для переписання
            with open("data/finance/settings.json", "w") as set_file:
                json.dump(new_settings, set_file) #переписує файл з новими даними
            win_finance.data_update() #оновлює підрахунки на екрані


#клас описує вікно з інтерфейсом гри на тренування пам'яті. наслідується від класу QWidgets  
class MemoryWin(QWidget):
    #ініціалізує клас, створює властивості
    def __init__(self):
        super().__init__()#виклик конструктора батьківського класу
        uic.loadUi('layouts/layout_memory.ui', self) #обробляє ui-файл та зчитує інтерфейс для подальшого використання

        '''PRE-RUN SETTINGS'''
        self.setStyleSheet(open("styles/memory_style.css").read()) #підключення css-стилю
        self.b_mem_start.setText("Почати гру") #змінює текст кнопки початку гри
        self.b_mem_start.setDisabled(False) #розблокує кнопку початку гри
        self.timer = QTimer() #створює таймер 
        self.btns = [] #список для ігрових кнопок
        #цикл повторюється 3 рази
        for i in range(1, 4):
            btn = QPushButton(str(i)) #створює кнопку з поряковим номером
            btn.setFixedSize(80, 80) #задає фіксований розмір кнопці
            btn.clicked.connect(self.bCheck) #при натисканні на кнопку виконується функція bCheck
            self.btns.append(btn) #додає кнопку до списку ігрових кнопок
            self.gridBox.addWidget(btn, 0, i-1) #додає кнопку на сітчатий лейаут. 1 аргумент - об'єкт кнопки, 2 аргумент - рядок лейаута, 3 аргумент - колонка лейаута
        #цикл повторюється 3 рази
        for i in range(3):
            btn = QPushButton(str(i+4)) #створює кнопку з поряковим номером(додається 4, так як 3 кнопки вже створено)
            btn.setFixedSize(80, 80) #задає фіксований розмір кнопці
            btn.clicked.connect(self.bCheck) #при натисканні на кнопку виконується функція bCheck
            self.btns.append(btn) #додає кнопку до списку ігрових кнопок
            self.gridBox.addWidget(btn, 2, i) #додає кнопку на сітчатий лейаут. 1 аргумент - об'єкт кнопки, 2 аргумент - рядок лейаута, 3 аргумент - колонка лейаута
        #цикл повторюється 3 рази
        for i in range(3):
            btn = QPushButton(str(i+7)) #створює кнопку з поряковим номером(додається 7, так як 6 кнопок вже створено)
            btn.setFixedSize(80, 80) #задає фіксований розмір кнопці
            btn.clicked.connect(self.bCheck) #при натисканні на кнопку виконується функція bCheck
            self.btns.append(btn) #додає кнопку до списку ігрових кнопок
            self.gridBox.addWidget(btn, 3, i) #додає кнопку на сітчатий лейаут. 1 аргумент - об'єкт кнопки, 2 аргумент - рядок лейаута, 3 аргумент - колонка лейаута
        #цкил повторюється для кожної кнопки та блокує її:
        for btn in self.btns:
            btn.setDisabled(True)

        '''CONNECTIONS'''
        self.b_goback.clicked.connect(self.goback) #при натисканні на кнопку "Повернутися назад"(<-) виконується функція goback
        self.b_mem_start.clicked.connect(self.start) #при натисканні на кнопку "Почати гру" виконується функція start

    '''METHODS'''
    #проводить операції з кнопкою початку, запускає гру
    def start(self):
        self.b_mem_start.setDisabled(True) #блокує кнопку початку гри
        self.b_mem_start.setText("Гру розпочато!") #змінює текст кнопки початку гри
        self.stage = 1 #надає змінній рівня гри значення 1
        self.step = 0 #надає змінній числа дій значення 0
        self.render() #генерує комбінації
        self.game() #запускає гру

    #генерує послідовність
    def render(self):
        self.order = {"stage1" : [], "stage2" : [], "stage3" : [], "stage4" : [], "stage5" : [], "stage6" : [], "stage7" : [], "stage8" : [], "stage9" : []} #словник з ключами рівнів гри для подальшого використання
        # prev = 0 #надає змінній попереднього числа значення 0
        #цикл повторюється 9 разів
        for i in range(1, 10):
            #так як з кожним рівнем кількість чисел в комбінації збільшується на 1, необхідно застосувати ще один цикл, кількість повторень якого залежить від кількості повторень основного цикла
            for t in range(i):
                num = randint(1, 9) #генерує випадкове число від 1 до 9 та записує його в змінну
                #перевіряє наявність числа в комбінації відповідного рівня
                if num in self.order["stage"+str(i)]: #якщо таке число знайдено, то...
                    #цикл виконуватиметься поки випадкове число матиме однакове значення з одним із чисел комбінації відповідного рівня
                    while num in self.order["stage"+str(i)]:       
                        num = randint(1, 9) #повторно генерує впадкове число від 1 до 9 та записує його в змінну
                    self.order["stage"+str(i)].append(num) #по заершенню цикла записує число до списку комбінації відповідного рівня
                else: #інакше...
                    self.order["stage"+str(i)].append(num) #записує число до списку комбінації відповідного рівня

    #логіка гри
    def game(self):
        #цкил повторюється для кожної кнопки зі списка кнопок та блокує її:
        for btn in self.btns:
            btn.setDisabled(True)
        #так як гра працює таким чином, що номер рівня = кількості чисел в комбінації, то необхідно перевірити рівність кількості дій та поточного рівня
        if self.step < self.stage: #якщо кількість дій менша, то...
            self.btnNum = self.order["stage"+str(self.stage)] #числа поточної комбінації записуються до списку 
            self.btn = self.btns[self.btnNum[self.step] - 1] #зі списка кнопок обирається кнопка, що відповідає числу на поточній дії
            self.btn.setStyleSheet("background-color: rgb(255,255,0); color: black") #дана кнопка змінює колір заднього фону на жовтий
            self.step += 1 #кількість дій збільшується на 1
            self.timer.singleShot(1000, self.game) #запускає функцію таймера. 1 аргумент - кількість мілісекунд, 2 аргумент - функція, що виконується після введеного часу
        else: #інакше...
            self.step = 0 #надає змінній числа дій значення 0
            #цкил повторюється для кожної кнопки зі списка кнопок
            for btn in self.btns:
                btn.setDisabled(False) #розблокує кнопки
                btn.setStyleSheet('''background-color: rgb(153,153,153); color: white
                QPushButton:hover:pressed {background-color: rgb(91, 91, 91);}''') #змінює всім кнопкам колір заднього фону на сірий, додає анімацію натискання

    #кінець гри
    def end(self):
        #перевіряє значення прапорця програшу
        if self.lost == True: #якщо True, то...
            msgBox.setText("Помилка! Ви програли!\nВи були на "+str(self.stage)+" рівні.") #змінює текст повідомлення
        else: #інакше
            msgBox.setText("Чудово! Все вірно!") #змінює текст повідомлення
        msgBox.setStandardButtons(QMessageBox.Ok) #виставляє вікну повідомлення стандартні кнопки
        msgBox.show() #показує вікно з повідомленням
        #цкил повторюється для кожної кнопки зі списка кнопок та блокує її:
        for btn in self.btns:
            btn.setDisabled(True)
        self.b_mem_start.setDisabled(False) #блокує кнопку початку гри
        self.b_mem_start.setText("Почати гру") #змінює текст кнопки початку гри
        self.stage = 1 #надає змінній рівня гри значення 1
        self.step = 0 #надає змінній числа дій значення 0
    
    #перевіряє, чи правильна кнопка натиснута
    def bCheck(self):
        btnClicked = int(self.sender().text()) #записує значення тексту натиснутої кнопки до змінної
        #перевіряє відповідність числа натиснутої кнопки до числа з поточної дії комбінації
        if btnClicked == self.btnNum[self.step]: #якщо дані рівні, то...
            self.step += 1 #кількість дій збільшується на 1
            #перевіряє рівність кількості дій та поточного рівня
            if self.step == self.stage: #якщо дані рівні, то...
                #перевіряє, чи знаходить гравець на останньому рівні
                if self.stage != 9: #якщо ні, то...
                    self.stage += 1 #рівень збільшується на 1
                    self.step = 0 #надає змінній числа дій значення 0
                    self.game() #запускає гру, але вже з новим значенням рівня
                else: #інакше...
                    self.lost = False #перемикає прапорець програшу на False
                    self.end() #завершує гру
        else: #інакше...
            self.lost = True #перемикає прапорець програшу на True
            self.end() #завершує гру

    #відкриває основне вікно, закриває вікно тренування пам'яті та повертає вигляд гри на початковий
    def goback(self):
        self.b_mem_start.setDisabled(False) #блокує кнопку початку гри
        self.b_mem_start.setText("Почати гру") #змінює текст кнопки початку гри
        self.stage = 0
        self.close()
        win.show()


'''APP-RUN'''
if __name__ == '__main__':
    #створення основних віджетів:
    app = QApplication(sys.argv)  #створення додатку
    win = MainWin() #створення екземпляру класу MainWin
    win_diary = DiaryWin() #створення екземпляру класу DiaryWin
    win_act = ActWin() #створення екземпляру класу ActWin
    win_notes = NotesWin() #створення екземпляру класу NotesWin
    win_finance = FinanceWin() #створення екземпляру класу FinanceWin
    win_trans = TransWin() #створення екземпляру класу TransWin
    win_fin_set = FinSetWin() #створення екземпляру класу FinSetWin
    win_memory = MemoryWin() #створення екземпляру класу MemoryWin
    inputDialog = QInputDialog() #створення діалогового вікна
    inputDialog.setStyleSheet(open("styles/inputDialog.css").read()) #підключення сss-стилю
    inputDialog.setWindowIcon(QtGui.QIcon("images/icons/icon.ico")) #надання діалоговому вікна значка
    msgBox = QMessageBox() #створення вікна оповіщення
    msgBox.setStyleSheet(open("styles/inputDialog.css").read()) #підключення сss-стилю
    msgBox.setWindowIcon(QtGui.QIcon("images/icons/icon.ico")) #надання діалоговому вікна значка
    msgBox.setWindowTitle(" ") #видалення заголовку вікна
    win_finance.openDB() #записує базу даних фінансів до таблиці

    #параметри запуска, запуск програми:
    win.show() #показує головне вікно
    sys.exit(app.exec()) #запускає додаток
import requests
import json
import re
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

DEBUG_URL = "http://localhost:8081"
HEROKU_URL = "https://simple-english-app.herokuapp.com"

ACTIVE_URL = HEROKU_URL

def tp_change(index, value, op):
    if field_type.get() == "Чтение" or field_type.get() == "Теория":
        answers.grid_remove()
        field_answers.grid_remove()
        correct_answers.grid_remove()
        field_correct_answers.grid_remove()
        questions.grid_remove()
        field_questions.grid_remove()
        music.grid_remove()
        field_music.grid_remove()
    elif field_type.get() == "Вставьте слова":
        answers.grid()
        field_answers.grid()
        correct_answers.grid()
        field_correct_answers.grid()
        questions.grid_remove()
        field_questions.grid_remove()
        music.grid_remove()
        field_music.grid_remove()
    elif field_type.get() == "Аудирование":
        answers.grid()
        field_answers.grid()
        correct_answers.grid()
        field_correct_answers.grid()
        questions.grid()
        field_questions.grid()
        music.grid()
        field_music.grid()

def tab_change(index, value, op):
    optional.grid()
    id.grid()
    field_id.grid()
    btn.grid()
    if combo_t.get() == "Пользователи":
        login.grid()
        field_login.grid()
        passw.grid()
        field_passw.grid()
        secret.grid()
        field_secret.grid()
        secret_type.grid()
        field_secret_type.grid()
        type.grid_remove()
        field_type.grid_remove()
        xp.grid_remove()
        field_xp.grid_remove()
        descr.grid_remove()
        field_descr.grid_remove()
        text.grid_remove()
        field_text.grid_remove()
    elif combo_t.get() == "Заголовки заданий":
        login.grid_remove()
        field_login.grid_remove()
        passw.grid_remove()
        field_passw.grid_remove()
        secret.grid_remove()
        field_secret.grid_remove()
        secret_type.grid_remove()
        field_secret_type.grid_remove()
        type.grid()
        field_type.grid()
        xp.grid()
        field_xp.grid()
        descr.grid()
        field_descr.grid()
        text.grid()
        field_text.grid()
    elif combo_t.get() == "Содержание заданий":
        login.grid_remove()
        field_login.grid_remove()
        passw.grid_remove()
        field_passw.grid_remove()
        secret.grid_remove()
        field_secret.grid_remove()
        secret_type.grid_remove()
        field_secret_type.grid_remove()
        type.grid()
        field_type.grid()
        xp.grid_remove()
        field_xp.grid_remove()
        descr.grid_remove()
        field_descr.grid_remove()
        text.grid()
        field_text.grid()

def analyse_headers():
    if field_descr.get() == "":
        showwarning("Пустое описание", "Введите описание.")
        return 0
    if field_xp.get() == "0":
        showwarning("Нет опыта", "Введите начисляемый опыт.")
        return 0
    return 1

def analyse_fields():
    if field_text.get() == "":
        showwarning("Нет содержимого", "Введите содержимое.")
        return 0
    return 1

def analyse_fields_insert():
    if analyse_fields():
        if field_answers.get() == "":
            showwarning("Нет ответов", "Введите варианты ответов.")
            return 0
        elif field_correct_answers.get() == "":
            showwarning("Нет правильных ответов", "Введите правильные варианты ответов.")
            return 0
        return 1
    else:
        return 0

def analyse_fields_audio():
    if analyse_fields_insert():
        if field_questions.get() == "":
            showwarning("Нет вопросов", "Введите вопросы.")
            return 0
        elif field_music.get() == "":
            showwarning("Нет ссылки на музыку", "Введите ссылку на музыку.")
            return 0
        return 1
    else:
        return 0

def analyse_result(result):
    if combo_m.get() == "":
        showwarning("Пустой метод", "Выберите метод.")
    if result == "Что-то пошло не так...":
        print("ну ок")
    elif result.status_code == 200:
        msg = "Запрос выполнен.\n\n\nРезультат запроса:\n" + result.text
        showinfo("Информация", msg)
    else:
        if result.status_code == 500 and combo_t == "Пользователи":
            showerror("Ошибка изменения БД", "Запрос не выполнен.\nВведите другой логин.")
        elif result.status_code == 500:
            showerror("Ошибка изменения БД", "Запрос не выполнен.\nВведите другой ID.")
        elif result.status_code == 404:
            showerror("Не найдено", "Запрос не выполнен.\nВведите существующий ID.")
        elif result.status_code == 400:
            showerror("Невозможный запрос", "Запрос не выполнен.\nВведите существующий ID.")
        else:
            print(result.text)


def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return 1
    return 0

def analyse_correct_answers():
    arr = []
    str = field_correct_answers.get()
    buf = ""
    for c in str:
        if c == ";":
            arr.append(buf)
            buf = ""
        else:
            buf += c
    return arr

def analyse_answers():
    arr = []
    str = field_answers.get()
    buf = ""
    buf_arr = []
    for c in str:
        if c == ";":
            buf_arr.append(buf)
            buf = ""
            arr.append(buf_arr)
            buf_arr = []
        elif c == ",":
            buf_arr.append(buf)
            buf = ""
        else:
            buf += c
    return arr

def analyse_questions():
    arr = []
    str = field_questions.get()
    buf = ""
    for c in str:
        if c == ";":
            arr.append(buf)
            buf = ""
        else:
            buf += c
    return arr

def clicked():
    result = "Что-то пошло не так..."
    if combo_t.get() == "Пользователи":
        if combo_m.get() == "Добавление":
            if field_passw.get() == "":
                showerror("Ошибка", "Введите не пустой пароль.")
            elif not isValid(field_login.get()):
                showerror("Ошибка", "Введите корректную почту.")
            else:
                result = requests.post(ACTIVE_URL + "/add_user",
                                data={"username": field_login.get(), "password": field_passw.get(),
                                      "secretWord": field_secret.get(), "secretWordType": "Другое"})
        elif combo_m.get() == "Удаление":
            result = requests.delete(ACTIVE_URL + "/destroy_user", data={"id": field_id.get()})
        elif combo_m.get() == "Посмотреть все":
            result = requests.get(ACTIVE_URL + "/get_all_users")
    if combo_t.get() == "Заголовки заданий":
        t_r = {
            "taskType": field_type.get(),
            "pointsXP": int(field_xp.get()),
            "description": field_descr.get(),
            "content": {
                "taskText": field_text.get(),
                "taskVariants": None,
                "correctVariants": None,
                "questions": None,
                "musicURL": None,
                "memLastUpdate": None,
                "nextNoticeIn": None
            }
        }
        insert_task = {
            "taskType": "Вставьте слова",
            "pointsXP": int(field_xp.get()),
            "description": field_descr.get(),
            "content": {
                "taskText": field_text.get(),
                "taskVariants": analyse_answers(),
                "correctVariants": analyse_correct_answers(),
                "questions": None,
                "musicURL": None,
                "memLastUpdate": None,
                "nextNoticeIn": None
            }
        }

        audio_task = {
            "taskType": "Аудирование",
            "pointsXP": int(field_xp.get()),
            "description": field_descr.get(),
            "content": {
                "taskText": None,
                "taskVariants": analyse_answers(),
                "correctVariants": analyse_correct_answers(),
                "questions": analyse_questions(),
                "musicURL": field_music.get(),
                "memLastUpdate": None,
                "nextNoticeIn": None
            }
        }
        json_task_t_r = json.dumps(t_r)
        json_task_audio = json.dumps(audio_task)
        json_task_insert = json.dumps(insert_task)
        if combo_m.get() == "Добавление":
            if analyse_headers():
                if field_type.get() == "":
                    showwarning("Пустой тип", "Введите тип задания.")
                elif field_type.get() == "Чтение" or field_type.get() == "Теория":
                    if analyse_fields():
                        result = requests.post(ACTIVE_URL + "/add_task_header", data={"stringTaskHeader": json_task_t_r})
                elif field_type.get() == "Вставьте слова":
                    if analyse_fields_insert():
                        result = requests.post(ACTIVE_URL + "/add_task_header", data={"stringTaskHeader": json_task_insert})
                elif field_type.get() == "Аудирование":
                    if analyse_fields_audio():
                        result = requests.post(ACTIVE_URL + "/add_task_header", data={"stringTaskHeader": json_task_audio})
        elif combo_m.get() == "Удаление":
            result = requests.delete(ACTIVE_URL + "/delete_task_header_by_id", data={"id": field_id.get()})
        elif combo_m.get() == "Посмотреть все":
            result = requests.get(ACTIVE_URL + "/get_all_task_headers")

    if combo_t.get() == "Содержание заданий":
        content_t_r = {
            "taskText": field_text.get(),
            "taskVariants": None,
            "correctVariants": None,
            "questions": None,
            "memLastUpdate": None,
            "nextNoticeIn": None,
            "musicURL": None
        }
        content_audio = {
            "taskText": None,
            "taskVariants": analyse_answers(),
            "correctVariants": analyse_correct_answers(),
            "questions": analyse_questions(),
            "musicURL": field_music.get()
        }

        content_insert = {
            "taskText": field_text.get(),
            "taskVariants": analyse_answers(),
            "correctVariants": analyse_correct_answers(),
            "questions": None,
            "musicURL": None
        }
        json_task_content_text = json.dumps(content_t_r)
        json_task_content_insert = json.dumps(content_insert)
        json_task_content_audio = json.dumps(content_audio)
        if combo_m.get() == "Добавление":
            if field_type.get() == "":
                showerror("Ошибка", "Введите тип задания.")
            elif field_id.get() == "":
                showerror("Ошибка", "Введите ID.")
            elif field_type.get() == "Чтение" or field_type.get() == "Теория":
                if analyse_fields():
                    result = requests.put(ACTIVE_URL + "/update_task_content_by_id",
                                   data={"id": field_id.get(), "stringTask": json_task_content_text})
            elif field_type.get() == "Вставьте слова":
                if analyse_fields_insert():
                    result = requests.put(ACTIVE_URL + "/update_task_content_by_id",
                                      data={"id": field_id.get(), "stringTask": json_task_content_insert})
            elif field_type.get() == "Аудирование":
                if analyse_fields_audio():
                    result = requests.put(ACTIVE_URL + "/update_task_content_by_id",
                                      data={"id": field_id.get(), "stringTask": json_task_content_audio})
        elif combo_m.get() == "Удаление":
            showinfo("Информация", "Удаление содержимого невозможно, перейдите в таблицу \"Заголовки заданий\" для полного удаления.")
        elif combo_m.get() == "Посмотреть все":
            result = requests.get(ACTIVE_URL + "/get_all_task_contents")
    analyse_result(result)

window = Tk()
window.title("САБД")
window.geometry('900x400')

hello = Label(window, text="Система администрирования базы данных")
hello.grid(column=0, row=0)

table = Label(window, text="Выберите таблицу")
table.grid(column=0, row=1)

tab = StringVar()
tab.trace('w', tab_change)
combo_t = Combobox(window, textvar=tab, values=["Пользователи", "Заголовки заданий", "Содержание заданий"])
combo_t.grid(column=1, row=1)

method = Label(window, text="Выберите метод")
method.grid(column=2, row=1)

met = StringVar()
combo_m = Combobox(window, textvar=met, values=["Добавление", "Удаление", "Посмотреть все"])
combo_m.grid(column=3, row=1)

optional = Label(window, text="Опциональные поля")
optional.grid(column=0, row=2)

id = Label(window, text="ID")
id.grid(column=0, row=3)

field_id = Entry(window, width=60)
field_id.grid(column=1, row=3)

login = Label(window, text="Логин")
login.grid(column=0, row=4)

field_login = Entry(window, width=60)
field_login.grid(column=1, row=4)

passw = Label(window, text="Пароль")
passw.grid(column=0, row=5)

field_passw = Entry(window, width=60)
field_passw.grid(column=1, row=5)

secret = Label(window, text="Секретное слово")
secret.grid(column=0, row=6)

field_secret = Entry(window, width=60)
field_secret.grid(column=1, row=6)

secret_type = Label(window, text="Тип секретного слова")
secret_type.grid(column=0, row=7)

field_secret_type = Combobox(window, width=57)
field_secret_type['values'] = ("Кличка вашего питомца", "Марка вашей машины", "Ваше счастливое число", "Ваш знак зодиака", "Другое")
field_secret_type.grid(column=1, row=7)

type = Label(window, text="Тип задания")
type.grid(column=0, row=8)

tp = StringVar()
tp.trace('w', tp_change)
field_type = Combobox(window, width=57, textvar=tp, values=["Теория", "Чтение", "Вставьте слова", "Аудирование"])
field_type.grid(column=1, row=8)

xp = Label(window, text="Опыт")
xp.grid(column=0, row=9)

field_xp = Entry(window, width=60)
field_xp.grid(column=1, row=9)
field_xp.insert(END, "0")

descr = Label(window, text="Описание")
descr.grid(column=0, row=10)

field_descr = Entry(window, width=60)
field_descr.grid(column=1, row=10)

text = Label(window, text="Текст")
text.grid(column=0, row=11)

field_text = Entry(window, width=60)
field_text.grid(column=1, row=11)

answers = Label(window, text="Варианты ответов")
answers.grid(column=0, row=12)

field_answers = Entry(window, width=60)
field_answers.grid(column=1, row=12)

correct_answers = Label(window, text="Правильные ответы")
correct_answers.grid(column=0, row=13)

field_correct_answers = Entry(window, width=60)
field_correct_answers.grid(column=1, row=13)

questions = Label(window, text="Вопросы")
questions.grid(column=0, row=14)

field_questions = Entry(window, width=60)
field_questions.grid(column=1, row=14)

music = Label(window, text="Музыка")
music.grid(column=0, row=15)

field_music = Entry(window, width=60)
field_music.grid(column=1, row=15)

btn = Button(window, text="Выполнить", command=clicked)
btn.grid(column=1, row=16)

id.grid_remove()
field_id.grid_remove()
login.grid_remove()
field_login.grid_remove()
passw.grid_remove()
field_passw.grid_remove()
secret.grid_remove()
field_secret.grid_remove()
secret_type.grid_remove()
field_secret_type.grid_remove()
type.grid_remove()
field_type.grid_remove()
xp.grid_remove()
field_xp.grid_remove()
descr.grid_remove()
field_descr.grid_remove()
text.grid_remove()
field_text.grid_remove()
answers.grid_remove()
field_answers.grid_remove()
correct_answers.grid_remove()
field_correct_answers.grid_remove()
questions.grid_remove()
field_questions.grid_remove()
music.grid_remove()
field_music.grid_remove()
optional.grid_remove()
btn.grid_remove()

window.mainloop()
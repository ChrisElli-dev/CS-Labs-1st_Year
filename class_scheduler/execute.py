import psycopg2

conn = psycopg2.connect(database="telegram_bot_db",
                        user="postgres",
                        password="12345",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

weekday = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

#данная функция получает данные из таблицы расписания на основе выбранной недели и дня недели,
# и затем возвращает список списков, содержащий информацию о каждом уроке на выбранном дне.
def get_day(week, day):
    timetable = [0] * 5
    cursor.execute(f'SELECT class, class_time, room_number FROM timetable WHERE week = {week} AND day = {day}')
    classrooms = cursor.fetchall() #это метод для получения следующей строки (записи) из результата выполнения SQL-запроса
    print(classrooms)
    for classroom in classrooms:
        day1 = []
        cursor.execute(f'SELECT subject, subject_type FROM class WHERE id = {classroom[0]}')
        subjects = cursor.fetchall()
        subject = subjects[0][0]
        subject_type = subjects[0][1]

        cursor.execute(f'SELECT start_time FROM time WHERE id = {classroom[1]}')
        time = cursor.fetchone()[0]
        day1.append(time) # append это метод в Python, который используется для добавления элемента в конец списка или массива.

        cursor.execute(f'SELECT name FROM subject WHERE id = {subject}')
        subj = cursor.fetchone()[0]
        day1.append(subj)

        cursor.execute(f'SELECT teacher FROM teacher_subject WHERE class = {classroom[0]}')
        teacher_id = cursor.fetchone()[0]

        cursor.execute(f'SELECT full_name FROM teacher WHERE id = {teacher_id}')
        teacher = cursor.fetchone()[0]
        day1.append(teacher)

        cursor.execute(f'SELECT name FROM subject_type WHERE id = {subject_type}')
        subject_type_name = cursor.fetchone()[0]
        day1.append(subject_type_name)
        day1.append(classroom[2])
        timetable[classroom[1] - 1] = day1
        print(timetable)
    return timetable

# форматирует список списков, полученный из get_day(), в виде строки, которая будет использоваться для отправки
# сообщения в телеграм-боте. Функция форматирует данные таким образом, чтобы они отображались в виде таблицы,
# содержащей информацию о времени, предмете, преподавателе, типе урока и номере кабинета для каждого урока.
def get_day_formatting(week, day):
    timetable = get_day(week, day)
    s = f'<b>{weekday[day - 1]}</b>\n'
    for day1 in range(1, 6): # перебираются дни с понедельника до пятницы
        if timetable[day1 - 1] == 0: # timetable представляетсписок, содержащий расписание пар на конкретный день недели.
            s += f'—————————\n{day1}. Нет пары\n'
        else:
            s += f'—————————\n{day1}. {timetable[day1 - 1][0]}\n{timetable[day1 - 1][1]}\n{timetable[day1 - 1][3]}\n' \
                 f'{timetable[day1 - 1][2]} | {timetable[day1 - 1][4]}\n'
    return s


def get_week_formatting(week):
    s = ''
    for day in range(1, 7):
        s += get_day_formatting(week, day) + '\n'
    return s
# Функция get_week_formatting() использует get_day_formatting() для создания строки, содержащей информацию
# о расписании для каждого дня недели нынешней, либо следующей недели.
# Результат представляет собой форматированный текст, который может быть отправлен в телеграм-боте.
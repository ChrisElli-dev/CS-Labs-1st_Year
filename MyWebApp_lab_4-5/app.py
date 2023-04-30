import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return render_template('login.fhtml')


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=\'{0}\' AND password=\'{1}\';".format(str(username),
                                                                                                          str(password)))
            if username == '' or password == '':
                return render_template("empty_fields.html")
            records = list(cursor.fetchall())

            if not records:
                return render_template("account_do_not_exist.html")

            return render_template('account.html', full_name=records[0][1], username=records[0][2],
                                   password=records[0][3])

        elif request.form.get("registration"):  # возвращает данные HTML-формы
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute('SELECT * FROM service.users WHERE login=\'{0}\''.format(
            str(login)))  # индикатор для метода format, чтобы он был заменен первым (нулевым индексом) параметром # format
        record = list(cursor.fetchall())
        if record:
            return render_template('user_existance.html')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return render_template('successful_reg.html')


        return redirect('/login/')

    return render_template('registration.html')

# render_template = отображает шаблон template_name_or_list из папки шаблонов

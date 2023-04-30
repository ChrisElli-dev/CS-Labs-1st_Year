import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
#QApplication управление потоком управления и основными настройками приложения с графическим интерфейсом
#QWidget базовым классом для всех объектов пользовательского интерфейса
#QLineEdit виджет, который разрешает вводить и редактировать одну строку текста
#QH выстраивает виджеты по горизонтали
#QV выстраивает виджеты по вертикали
#QPushButton кнопка, на которую можно нажимать

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_result = QHBoxLayout()
        # выравнивания с помощью функции addLayout()
        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_result)
        # QLineEdit - создание виджетов которые разрешает вводить и редактировать одну строку текста
        # addWidget() - привязка виджетов к осям
        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_third.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_0 = QPushButton("0", self)
        self.hbox_third.addWidget(self.b_0)

        self.b_dot = QPushButton(".", self)
        self.hbox_second.addWidget(self.b_dot)

        self.b_plus = QPushButton("+", self)
        self.hbox_result.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_result.addWidget(self.b_minus)

        self.b_multiply = QPushButton("*", self)
        self.hbox_result.addWidget(self.b_multiply)

        self.b_divide = QPushButton("/", self)
        self.hbox_result.addWidget(self.b_divide)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_dot.clicked.connect(lambda: self._button("."))
        self.b_plus.clicked.connect(lambda: self._button("+"))
        self.b_minus.clicked.connect(lambda: self._button("-"))
        self.b_multiply.clicked.connect(lambda: self._button("*"))
        self.b_divide.clicked.connect(lambda: self._button("/"))
        self.b_result.clicked.connect(self._calculate)
# Место появления окна
        self.setGeometry(650, 350, 600, 400)
        self.setWindowTitle('Basic math Calculator')
        self.show()

# отображает текст на экране калькулятора,
# когда пользователь нажимает на кнопки цифр и математических операций.
    def _button(self, param):
        line = self.input.text()
        self.input.setText(line + param)
        self.per = self.input.setText(line + param)
# вычисляет результат выражения, "=", введенного пользователем в калькулятор, используя функцию eval()
    def _calculate(self):
        try:
            result = eval(self.input.text())  # eval динамически-обновляемое выражение, как input()
            self.input.setText(str(result))
        except ZeroDivisionError:
            QMessageBox.warning(self, "Attention", "You can't divide by zero!")
        except:
            QMessageBox.warning(self, "Attention", "There was an error!")

# сохраняет первое число в переменной self.num_1 и
# выбранную математическую операцию в переменной self.op.
#"self.op" - это переменная-атрибут объекта класса калькулятора, которая используется
# для хранения выбранной пользователем математической операции (сложение, вычитание, умножение, деление).
    def _operation(self, op):
        self.num_1 = int(self.input.text())
        self.op = op
        self.input.setText("")

#Метод "_result" вызывается при нажатии кнопки "равно" на калькуляторе,
# после того как пользователь ввел второе число. Он сохраняет второе число в переменной "self.num_2"
# и вычисляет результат выражения с использованием переменных "self.num_1", "self.num_2" и "self.op"
    def _result(self):
        self.num_2 = int(self.input.text())
        if self.op == "+":
            self.input.setText(str(self.num_1 + self.num_2))
        if self.op == "-":
            self.input.setText(str(self.num_1 - self.num_2))
        if self.op == "*":
            self.input.setText(str(self.num_1 * self.num_2))
        if self.op == "/":
            self.input.setText(str(self.num_1 / self.num_2))


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())

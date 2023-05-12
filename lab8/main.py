import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Editor")
        # Создание компонентов интерфейса
        self.dbname_label = QLabel("Database name:")
        self.dbname_input = QLineEdit()
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        self.user_label = QLabel("User:")
        self.user_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.connect_button = QPushButton("Connect")

        self.connect_button.clicked.connect(self.connect_to_db)

        # Размещение компонентов интерфейса
        layout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.dbname_label)
        hbox1.addWidget(self.dbname_input)
        hbox1.addWidget(self.user_label)
        hbox1.addWidget(self.user_input)
        hbox1.addWidget(self.password_label)
        hbox1.addWidget(self.password_input)
        hbox1.addWidget(self.host_label)
        hbox1.addWidget(self.host_input)
        hbox1.addWidget(self.port_label)
        hbox1.addWidget(self.port_input)
        hbox1.addWidget(self.connect_button)
        layout.addLayout(hbox1)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Subject", "Time"])
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_table)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_record)
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_record)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_record)
        layout.addWidget(self.table)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.refresh_button)
        hbox2.addWidget(self.add_button)
        hbox2.addWidget(self.update_button)
        hbox2.addWidget(self.delete_button)
        layout.addLayout(hbox2)
        self.setLayout(layout)

    def connect_to_db(self):
        dbname = self.dbname_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        host = self.host_input.text()
        port = self.port_input.text()

        try:
            self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            self.show_message("Success", f"Connected to database: {dbname}")
        except psycopg2.Error as e:
            self.show_message("Error", str(e))

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def refresh_table(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM timetable")
                result = cur.fetchall()

            self.table.setRowCount(len(result))

            for row, data in enumerate(result):
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, col, item)
        except AttributeError:
            self.show_message("Error", "Not connected to a database")
        except psycopg2.Error as e:
            self.show_message("Error", str(e))

    def add_record(self):
        value, ok = QInputDialog.getText(self, "Add record", "Enter value:")
        if ok and value:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("INSERT INTO timetable (value) VALUES (%s)", (value,))
                    self.conn.commit()
                    self.refresh_table()
            except AttributeError:
                self.show_message("Error", "Not connected to a database")
            except psycopg2.Error as e:
                self.show_message("Error", str(e))

    def update_record(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            id_ = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()

        value, ok = QInputDialog.getText(self, "Update record", "Enter new value:", QLineEdit.Normal, value)
        if ok and value:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("UPDATE timetable SET name = %s WHERE value = %s", (value, id_))
                self.conn.commit()
                self.refresh_table()
            except AttributeError:
                self.show_message("Error", "Not connected to a database")
            except psycopg2.Error as e:
                self.show_message("Error", str(e))
        else:
            self.show_message("Error", "No row selected")

    def delete_record(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            id_ = self.table.item(row, 0).text()

        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM timetable WHERE value = %s", (id_,))
            self.conn.commit()
            self.refresh_table()
        except AttributeError:
            self.show_message("Error", "Not connected to a database")
        except psycopg2.Error as e:
            self.show_message("Error", str(e))
        else:
            self.show_message("Error", "No row selected")

app = QApplication(sys.argv)
win = MainWidget()
win.show()
sys.exit(app.exec_())

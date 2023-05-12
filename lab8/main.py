import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, \
    QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QTabWidget


class Teacher:
    def __init__(self, teacher_id, teacher_name):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name


class Subject:
    def __init__(self, subject_id, subject_name):
        self.subject_id = subject_id
        self.subject_name = subject_name


class Time:
    def __init__(self, time_id, start_time):
        self.time_id = time_id
        self.start_time = start_time


def show_message_box(message):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.exec_()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.time_delete_button = QPushButton("Delete")
        self.time_add_button = QPushButton("Add")
        self.time_update_button = QPushButton("Update")
        self.subject_update_button = QPushButton("Update")
        self.time_refresh_button = QPushButton("Refresh")
        self.time_table = QTableWidget()
        self.time_widget = QWidget()
        self.subject_delete_button = QPushButton("Delete")
        self.subject_table = QTableWidget()
        self.subject_add_button = QPushButton("Add")
        self.subject_refresh_button = QPushButton("Refresh")
        self.port_input = QLineEdit()
        self.subject_widget = QWidget()
        self.teacher_delete_button = QPushButton("Delete")
        self.teacher_update_button = QPushButton("Update")
        self.teacher_add_button = QPushButton("Add")
        self.teacher_refresh_button = QPushButton("Refresh")
        self.teacher_table = QTableWidget()
        self.teacher_widget = QWidget()
        self.tab_widget = QTabWidget(self)
        self.connect_button = QPushButton("Connect")
        self.password_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.user_input = QLineEdit()
        self.user_label = QLabel("User:")
        self.host_input = QLineEdit()
        self.host_label = QLabel("Host:")
        self.port_label = QLabel("Port:")
        self.dbname_input = QLineEdit()
        self.dbname_label = QLabel("Database name:")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Editor")
        # Создание компонентов интерфейса
        self.password_input.setEchoMode(QLineEdit.Password)

        self.connect_button.clicked.connect(self.connect_to_db)

        # Teachers Tab
        teacher_layout = QVBoxLayout(self.teacher_widget)
        teacher_table_layout = QHBoxLayout()
        teacher_table_label = QLabel("Teachers:")
        self.teacher_table.setColumnCount(2)
        self.teacher_table.setHorizontalHeaderLabels(["Teacher ID", "Teacher Name"])
        teacher_table_layout.addWidget(teacher_table_label)
        teacher_table_layout.addWidget(self.teacher_table)
        teacher_button_layout = QHBoxLayout()
        teacher_button_layout.addWidget(self.teacher_refresh_button)
        teacher_button_layout.addWidget(self.teacher_add_button)
        teacher_button_layout.addWidget(self.teacher_update_button)
        teacher_button_layout.addWidget(self.teacher_delete_button)
        teacher_layout.addLayout(teacher_table_layout)
        teacher_layout.addLayout(teacher_button_layout)
        self.tab_widget.addTab(self.teacher_widget, "Teachers")

        # Subjects Tab
        subject_layout = QVBoxLayout(self.subject_widget)
        subject_table_layout = QHBoxLayout()
        subject_table_label = QLabel("Subjects:")
        self.subject_table.setColumnCount(2)
        self.subject_table.setHorizontalHeaderLabels(["Subject ID", "Subject Name"])
        subject_table_layout.addWidget(subject_table_label)
        subject_table_layout.addWidget(self.subject_table)
        subject_button_layout = QHBoxLayout()
        subject_button_layout.addWidget(self.subject_refresh_button)
        subject_button_layout.addWidget(self.subject_add_button)
        subject_button_layout.addWidget(self.subject_update_button)
        subject_button_layout.addWidget(self.subject_delete_button)
        subject_layout.addLayout(subject_table_layout)
        subject_layout.addLayout(subject_button_layout)
        self.tab_widget.addTab(self.subject_widget, "Subjects")

        # Time Tab
        time_layout = QVBoxLayout(self.time_widget)
        time_table_layout = QHBoxLayout()
        time_table_label = QLabel("Time:")
        self.time_table.setColumnCount(2)
        self.time_table.setHorizontalHeaderLabels(["ID", "Start Time"])
        time_table_layout.addWidget(time_table_label)
        time_table_layout.addWidget(self.time_table)
        time_button_layout = QHBoxLayout()
        time_button_layout.addWidget(self.time_refresh_button)
        time_button_layout.addWidget(self.time_add_button)
        time_button_layout.addWidget(self.time_update_button)
        time_button_layout.addWidget(self.time_delete_button)
        time_layout.addLayout(time_table_layout)
        time_layout.addLayout(time_button_layout)
        self.tab_widget.addTab(self.time_widget, "Time")

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
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def connect_to_db(self):
        dbname = self.dbname_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        host = self.host_input.text()
        port = self.port_input.text()

        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.conn = conn
            show_message_box("Connection successful!")
            self.load_teacher_data()
            self.load_subject_data()
            self.load_times_data()

            self.teacher_refresh_button.clicked.connect(self.load_teacher_data)
            self.teacher_add_button.clicked.connect(self.add_teacher)
            self.teacher_update_button.clicked.connect(self.update_teacher)
            self.teacher_delete_button.clicked.connect(self.delete_teacher)

            self.subject_refresh_button.clicked.connect(self.load_subject_data)
            self.subject_add_button.clicked.connect(self.add_subject)
            self.subject_update_button.clicked.connect(self.update_subject)
            self.subject_delete_button.clicked.connect(self.delete_subject)

            self.time_refresh_button.clicked.connect(self.load_times_data)
            self.time_add_button.clicked.connect(self.add_time)
            self.time_update_button.clicked.connect(self.update_time)
            self.time_delete_button.clicked.connect(self.delete_time)

            self.tab_widget.setCurrentIndex(0)
        except Exception as e:
            show_message_box(str(e))

    def load_teacher_data(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM teacher;")
            teacher_data = cur.fetchall()
            self.teacher_table.setRowCount(len(teacher_data))
            for i, row in enumerate(teacher_data):
                for j, val in enumerate(row):
                    self.teacher_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            show_message_box(str(e))

    def add_teacher(self):
        name, ok = QInputDialog.getText(self, "Add Teacher", "Enter teacher name:")
        if ok and name:
            try:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO teacher (full_name) VALUES (%s)", (name,))
                self.conn.commit()
                cur.close()
                self.load_teacher_data()
            except psycopg2.Error as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

    def update_teacher(self):
        selected_rows = self.teacher_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Update Teacher", "Please select a teacher to update.", QMessageBox.Ok)
            return
        row = selected_rows[0].row()
        id = int(self.teacher_table.item(row, 0).text())
        name, ok = QInputDialog.getText(self, "Update Teacher", "Enter new teacher name:", QLineEdit.Normal,
                                        self.teacher_table.item(row, 1).text())
        if ok and name:
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE teacher SET full_name = %s WHERE id = %s", (name, id))
                self.conn.commit()
                cur.close()
                self.load_teacher_data()
            except psycopg2.Error as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

    def delete_teacher(self):
        selected_rows = self.teacher_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Delete Teacher", "Please select a teacher to delete.", QMessageBox.Ok)
            return
        row = selected_rows[0].row()
        id = int(self.teacher_table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Delete Teacher", f"Are you sure you want to delete teacher {id}?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM teacher WHERE id = %s", (id,))
                self.conn.commit()
                cur.close()
                self.load_teacher_data()
            except psycopg2.Error as e:
                QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

    def load_subject_data(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM subject;")
            subject_data = cur.fetchall()
            self.subject_table.setRowCount(len(subject_data))
            for i, row in enumerate(subject_data):
                for j, val in enumerate(row):
                    self.subject_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            show_message_box(str(e))

    def refresh_subject_table(self):
        self.subject_table.setRowCount(0)
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM subject")
            for row in cur.fetchall():
                self.subject_table.insertRow(self.subject_table.rowCount())
                for col, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.subject_table.setItem(self.subject_table.rowCount() - 1, col, item)

    def add_subject(self):
        name, ok = QInputDialog.getText(self, "Add Subject", "Enter subject name:")
        if ok and name:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO subject (name) VALUES (%s)", (name,))
            self.refresh_subject_table()

    def delete_subject(self):
        selected_rows = self.subject_table.selectedRows()
        if selected_rows:
            result = QMessageBox.question(self, "Delete Subject",
                                          "Are you sure you want to delete the selected subjects?",
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                with self.conn.cursor() as cur:
                    for row in selected_rows:
                        id = self.subjects_table.item(row.row(), 0).text()
                        cur.execute("DELETE FROM subject WHERE id = %s", (id,))
                self.refresh_subject_table()

    def update_subject(self):
        selected_rows = self.subject_table.selectedRows()
        if len(selected_rows) == 1:
            id = self.subject_table.item(selected_rows[0].row(), 0).text()
            name, ok = QInputDialog.getText(self, "Update Subject", "Enter new subject name:",
                                            QLineEdit.Normal,
                                            self.subject_table.item(selected_rows[0].row(), 1).text())
            if ok and name:
                with self.conn.cursor() as cur:
                    cur.execute("UPDATE subject SET name = %s WHERE id = %s", (name, id))
                self.refresh_subject_table()
        else:
            QMessageBox.warning(self, "Update Subject", "Please select a single row to update.")

    def load_times_data(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM time;")
            time_data = cur.fetchall()
            self.time_table.setRowCount(len(time_data))
            for i, row in enumerate(time_data):
                for j, val in enumerate(row):
                    self.time_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            show_message_box(str(e))

    def refresh_time_table(self):
        self.time_table.clearContents()
        self.time_table.setRowCount(0)
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM time ORDER BY id ASC")
            rows = cur.fetchall()
            for row in rows:
                rowPosition = self.time_table.rowCount()
                self.time_table.insertRow(rowPosition)
                self.time_table.setItem(rowPosition, 0, QTableWidgetItem(str(row[0])))
                self.time_table.setItem(rowPosition, 1, QTableWidgetItem(row[1]))

    def add_time(self):
        start_time, ok_pressed = QInputDialog.getText(self, "Add Time", "Start Time:")
        if ok_pressed and start_time:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("INSERT INTO time (start_time) VALUES (%s)", (start_time,))
            conn.commit()
            self.refresh_time_table()

    def update_time(self):
        selected_row = self.time_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No row selected")
            return

        time_id = self.time_table.item(selected_row, 0).text()
        start_time, ok_pressed = QInputDialog.getText(self, "Update Time", "Start Time:", QLineEdit.Normal,
                                                      self.time_table.item(selected_row, 1).text())
        if ok_pressed and start_time:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("UPDATE time SET start_time = %s WHERE id = %s", (start_time, time_id))
            conn.commit()
            self.refresh_time_table()

    def delete_time(self):
        selected_row = self.time_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No row selected")
            return

        time_id = self.time_table.item(selected_row, 0).text()
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM time WHERE id = %s", (time_id,))
        conn.commit()
        self.refresh_time_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())

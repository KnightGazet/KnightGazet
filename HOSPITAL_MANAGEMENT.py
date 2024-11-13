import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication,QGraphicsOpacityEffect, QMainWindow, QAction, QVBoxLayout, 
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox, 
                             QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
class HospitalManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BU HOSPITAL")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.initUI()
        self.initDatabase()
        self.current_window = None

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QTableWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
            }
            QHeaderView {
                background-color: #5A5A5A; /* Lighter background for better visibility */
                color: #000000; /* Dark text color */
            }
            QTableWidgetItem {
                background-color: #3E3E3E;
                color: #FFFFFF; /* Dark text for table items */
            }
            QFormLayout {
                color: #FFFFFF;
            }
        """)
        
        self.createHeader()
        self.createMenu()
        self.label = QLabel("Welcome to BU HOSPITAL")
        self.layout.addWidget(self.label)

    def createHeader(self):
        header_layout = QHBoxLayout()
        
        # Hospital Name as a clickable button
        hospital_name_button = QPushButton("BU HOSPITAL")
        hospital_name_button.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                text-decoration: underline; /* Optional: add underline on hover */
            }
        """)
        hospital_name_button.clicked.connect(self.showHomePage)  # Connect to the home page method
        header_layout.addWidget(hospital_name_button)

        # Spacer to push the login button to the right
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout.addLayout(header_layout)
    
    def clearLayout(self):
        # Clear all widgets from the layout
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def showHomePage(self):
        # Clear the layout
        self.clearLayout()

        # Remove the code that adds the hospital image as a background
        # background_label = QLabel(self)
        # pixmap = QPixmap("hospital_with_doctors.jpg")  # Replace with your image file name
        # background_label.setPixmap(pixmap)
        # background_label.setScaledContents(True)  # Scale the image to fit the label
        # background_label.setFixedSize(800, 600)  # Set a fixed size for the image label (match window size)

        # Create a new QLabel for the welcome message
        welcome_label = QLabel("Welcome to BU HOSPITAL!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFD700;")  # Gold color
        self.layout.addWidget(welcome_label)

        # Add hospital information with attractive styling
        hospital_info = [
            ("Our Mission: To provide compassionate and high-quality healthcare.", "font-size: 18px; color: #ADD8E6;"),
            ("Services Offered: Emergency care, outpatient services, surgery, and more.", "font-size: 18px; color: #90EE90;"),
            ("Established: 1990, serving the community for over 30 years.", "font-size: 18px; color: #FFB6C1;"),
            ("Contact Us: Phone: (123) 456-7890 | Email: info@buhospital.com", "font-size: 18px; color: #FFFFFF;"),
            ("Visit our website for more information: www.buhospital.com", "font-size: 18px; color: #FFA07A;"),
        ]

        for info, style in hospital_info:
            info_label = QLabel(info)
            info_label.setStyleSheet(style)  # Apply custom styles
            self.layout.addWidget(info_label)

        # Ensure the layout has the correct order
        # self.layout.setAlignment(background_label, Qt.AlignCenter)  # Remove this line as well
    def createMenu(self):
        menu_layout = QHBoxLayout()
        
        # Doctors Button
        doctors_button = QPushButton("Doctors")
        doctors_button.clicked.connect(self.showDoctors)
        menu_layout.addWidget(doctors_button)

        # Patients Button
        patients_button = QPushButton("Patients")
        patients_button.clicked.connect(self.showPatients)
        menu_layout.addWidget(patients_button)

        # Appointments Button
        appointments_button = QPushButton("Appointments")
        appointments_button.clicked.connect(self.showAppointments)
        menu_layout.addWidget(appointments_button)

        self.layout.addLayout(menu_layout)

    

    def initDatabase(self):
        self.conn = sqlite3.connect('hospital.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS doctors
                               (id INTEGER PRIMARY KEY, name TEXT, specialty TEXT, contact TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients
                               (id INTEGER PRIMARY KEY, name TEXT, concern TEXT, contact TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments
                               (id INTEGER PRIMARY KEY, doctor_id INTEGER, patient_id INTEGER, 
                               date TEXT, time TEXT)''')
        self.conn.commit()

    def showLogin(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()

    
    def showDoctors(self):
        self.clearLayout()  # Clear the layout before showing doctors
        self.current_window = DoctorWindow(self)
        self.layout.addWidget(self.current_window)  # Add the DoctorWindow to the layout
        self.current_window.loadDoctors()  # Load doctors data

    def showPatients(self):
        self.clearLayout()  # Clear the layout before showing patients
        self.current_window = PatientWindow(self)
        self.layout.addWidget(self.current_window)  # Add the PatientWindow to the layout
        self.current_window.loadPatients()  # Load patients data

    def showAppointments(self):
        self.clearLayout()  # Clear the layout before showing appointments
        self.current_window = AppointmentWindow(self)
        self.layout.addWidget(self.current_window)  # Add the AppointmentWindow to the layout
        self.current_window.loadAppointments()

class LoginWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Login")
        self.setGeometry(150, 150, 300, 200)
        
        self.layout = QVBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.checkLogin)

        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.setLayout(self.layout)

    def checkLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "ADMIN" and password == "admin123":
            QMessageBox.information(self, "Login", "Login Successful!")
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Invalid Credentials!")

class DoctorWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Doctors")
        self.setGeometry(150, 150, 600, 400)

        self.layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Specialty", "Contact"])
        self.layout.addWidget(self.table)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.specialty_input = QLineEdit(self)
        self.contact_input = QLineEdit(self)
        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Specialty:", self.specialty_input)
        self.form_layout.addRow("Contact:", self.contact_input)

        self.add_button = QPushButton("Add Doctor")
        self.add_button.clicked.connect(self.addDoctor)
        self.form_layout.addRow(self.add_button)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)
        self.loadDoctors()

    def loadDoctors(self):
        self.table.setRowCount(0)
        self.main_app.cursor.execute("SELECT * FROM doctors")
        for row_number, row_data in enumerate(self.main_app.cursor.fetchall()):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def addDoctor(self):
        name = self.name_input.text()
        specialty = self.specialty_input.text()
        contact = self.contact_input.text()
        if name and specialty and contact:
            self.main_app.cursor.execute("INSERT INTO doctors (name, specialty, contact) VALUES (?, ?, ?)", 
                                          (name, specialty, contact))
            self.main_app.conn.commit()
            self.loadDoctors()
            self.name_input.clear()
            self.specialty_input.clear()
            self.contact_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")

class PatientWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Patients")
        self.setGeometry(150, 150, 600, 400)

        self.layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Concern", "Contact"])
        self.layout.addWidget(self.table)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.concern_input = QLineEdit(self)
        self.contact_input = QLineEdit(self)
        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Concern:", self.concern_input)
        self.form_layout.addRow("Contact:", self.contact_input)

        self.add_button = QPushButton("Add Patient")
        self.add_button.clicked.connect(self.addPatient)
        self.form_layout.addRow(self.add_button)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)
        self.loadPatients()

    def loadPatients(self):
        self.table.setRowCount(0)
        self.main_app.cursor.execute("SELECT * FROM patients")
        for row_number, row_data in enumerate(self.main_app.cursor.fetchall()):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def addPatient(self):
        name = self.name_input.text()
        concern = self.concern_input.text()
        contact = self.contact_input.text()
        if name and concern and contact:
            self.main_app.cursor.execute("INSERT INTO patients (name, concern, contact) VALUES (?, ?, ?)", 
                                          (name, concern, contact))
            self.main_app.conn.commit()
            self.loadPatients()
            self.name_input.clear()
            self.concern_input.clear()
            self.contact_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")

class AppointmentWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Appointments")
        self.setGeometry(150, 150, 600, 400)

        self.layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Doctor ID", "Patient ID", "Date", "Time"])
        self.layout.addWidget(self.table)

        self.form_layout = QFormLayout()
        self.doctor_id_input = QLineEdit(self)
        self.patient_id_input = QLineEdit(self)
        self.date_input = QLineEdit(self)
        self.time_input = QLineEdit(self)
        self.form_layout.addRow("Doctor ID:", self .doctor_id_input)
        self.form_layout.addRow("Patient ID:", self.patient_id_input)
        self.form_layout.addRow("Date:", self.date_input)
        self.form_layout.addRow("Time:", self.time_input)

        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.addAppointment)
        self.form_layout.addRow(self.add_button)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)
        self.loadAppointments()

    def loadAppointments(self):
        self.table.setRowCount(0)
        self.main_app.cursor.execute("SELECT * FROM appointments")
        for row_number, row_data in enumerate(self.main_app.cursor.fetchall()):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def addAppointment(self):
        doctor_id = self.doctor_id_input.text()
        patient_id = self.patient_id_input.text()
        date = self.date_input.text()
        time = self.time_input.text()
        if doctor_id and patient_id and date and time:
            self.main_app.cursor.execute("INSERT INTO appointments (doctor_id, patient_id, date, time) VALUES (?, ?, ?, ?)", 
                                          (doctor_id, patient_id, date, time))
            self.main_app.conn.commit()
            self.loadAppointments()
            self.doctor_id_input.clear()
            self.patient_id_input.clear()
            self.date_input.clear()
            self.time_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HospitalManagementApp()
    window.show()
    sys.exit(app.exec_())
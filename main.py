import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout,QRadioButton,QTextEdit,
    QTableWidget, QTableWidgetItem,QComboBox,QFileDialog
)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator
from PyQt6.QtCore import Qt

# تسجيل الدخول
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" تسجيل الدخول - (طالب-ة/مدرس-ة)")
        #self.setWindowIcon(QIcon("image\ai.png"))  
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        # Layout
        main_layout = QVBoxLayout()

        # Top bar for the exit button
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        # Exit button
        self.exit_button = QPushButton()
        self.exit_button.setIcon(QIcon("image/sign-in-alt.png"))  # Replace with your exit icon
        self.exit_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #ff6b6b;
                border-radius: 5px;
            }
        """)

        self.exit_button.clicked.connect(self.close)  # Close the application
        top_bar.addWidget(self.exit_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Add the top bar to the main layout
        main_layout.addLayout(top_bar)

        # Add company logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/user.png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.logo_label)

        # Welcome label
        self.welcome_label = QLabel("مرحبًا بك في تطبيق الطلاب !")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 16))
        self.welcome_label.setStyleSheet("color: #34495e;")
        main_layout.addWidget(self.welcome_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)

        main_layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)
        main_layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("تسجيل الدخول")
        self.login_button.setIcon(QIcon("image/book-open-reader.png"))
        self.login_button.setFont(QFont("Arial", 12))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
                
            }
        """)

        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)

        # Create account button
        self.create_account_button = QPushButton("   إنشاء حساب جديد")
        self.create_account_button.setIcon(QIcon("image/add-friend (1).png"))
        self.create_account_button.setFont(QFont("Arial", 12))
        self.create_account_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
                
            }
        """)
        self.create_account_button.clicked.connect(self.open_registration_window)
        main_layout.addWidget(self.create_account_button)
        
        # Login button_forgot_password
        self.button_forgot_password = QPushButton("   نسيت كلمة المرور؟")
        self.button_forgot_password.setIcon(QIcon("image/forgot.png"))
        self.button_forgot_password.setFont(QFont("Arial", 12))
        self.button_forgot_password.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
                
            }
        """)
        self.button_forgot_password.clicked.connect(self.open_forget_window)
        main_layout.addWidget(self.button_forgot_password)

        self.setLayout(main_layout)


    def open_teacher_window(self):
        self.teacher_window = TeacherMainWindow()
        self.teacher_window.show()
        self.close()

    def open_student_window(self):
        self.student_window = StudentMainWindow()
        self.student_window.show()
        self.close()

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()
        self.hide()

    def open_forget_window(self):
        self.forget_window = ForgetPassWindow(self)
        self.forget_window.show()
        self.hide()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
             QMessageBox.warning(self, "خطأ", "الحقول فارغة.")

        try:
            users = self.load_users()
            if username in users:
                user = users[username]
                if user["password"] == password:
                    if user["type"] == "مدرس":
                        self.open_teacher_window()
                    elif user["type"] == "طالب":
                        self.open_student_window()
                else:
                    QMessageBox.warning(self, "خطأ", "كلمة المرور غير صحيحة.")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء قراءة البيانات: {e}")

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
        
# انشاء حساب
class RegistrationWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("إنشاء حساب جديد")
        self.setWindowIcon(QIcon("image/user.png"))  
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #34495e;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }
            QRadioButton {
                font-size: 18px;
            }
            QPushButton#register_button {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton#register_button:hover {
                background-color: #083A8A;
            }
            QPushButton#back_button {
                background-color: #EB9BBE;
            }
            QPushButton#back_button:hover {
                background-color: #C2809D;
            }
        """)

        # Main layout
        layout = QVBoxLayout()
        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/user.png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)


        # Add logo or banner image
        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/add-user (1).png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Welcome message
        self.title_label = QLabel("إنشاء حساب جديد")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.title_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        #Label chose student_teacher
        self.Label_chose=QLabel('نوع المستخدم:   ')
        self.Label_chose.setStyleSheet('font-size: 20px;')
        layout.addWidget(self.Label_chose)

        #Radio Buttons layout
        Radiobuttons_layout = QHBoxLayout()
        Radiobuttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align buttons to the left

        # Radio buttons for user type
        self.teacher_radio = QRadioButton("مدرس     ")
        self.student_radio = QRadioButton("طالب     ")
        Radiobuttons_layout.addWidget(self.teacher_radio)
        Radiobuttons_layout.addWidget(self.student_radio)
        layout.addLayout(Radiobuttons_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Register button
        self.register_button = QPushButton("   إنشاء حساب")
        self.register_button.setObjectName("register_button")
        self.register_button.setIcon(QIcon("image/add-friend (1).png"))  # Replace with your icon path
        self.register_button.clicked.connect(self.create_account)
        buttons_layout.addWidget(self.register_button)

        # Back button
        self.back_button = QPushButton("   عودة")
        self.back_button.setObjectName("back_button")
        self.back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        self.back_button.clicked.connect(self.back_to_login)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "خطأ", "يجب ملء جميع الحقول.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "خطأ", "كلمتا المرور غير متطابقتين.")
            return

        user_type = "مدرس" if self.teacher_radio.isChecked() else "طالب" if self.student_radio.isChecked() else None

        if not user_type:
            QMessageBox.warning(self, "خطأ", "يجب اختيار نوع المستخدم.")
            return

        try:
            users = self.load_users()
            if username in users:
                QMessageBox.warning(self, "خطأ", "اسم المستخدم موجود بالفعل.")
                return

            users[username] = {"password": password, "type": user_type}
            self.save_users(users)
            QMessageBox.information(self, "نجاح", "تم إنشاء الحساب بنجاح!")
            self.close()
            self.parent.show()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ البيانات: {e}")

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_users(self, users):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def back_to_login(self):
        self.close()
        self.parent.show()

# نسيت كلمة المرور
class ForgetPassWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("تحديث كلمة المرور")
        self.setWindowIcon(QIcon("image/user.png"))  # Replace with your icon path
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #34495e;
            }

            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }
            QPushButton#back_button {
                background-color: #EB9BBE;
            }
            QPushButton#back_button:hover {
                background-color: #C2809D;
            }
            QPushButton#updata_button {
                background-color: #0A4CB3;
            }
            QPushButton#updata_button:hover {
                background-color: #083A8A;
            }
            
        """)

        # Main layout   
        layout = QVBoxLayout()

        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/user.png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        self.logo_label = QLabel(self)
        pixmap = QPixmap("image\\add-user (1).png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Welcome message
        self.title_label = QLabel("تحديث كلمة المرور")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.title_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Register button
        self.updata_button = QPushButton(" تحديث")
        self.updata_button.setObjectName("updata_button")
        self.updata_button.setIcon(QIcon("image/refresh.png"))  # Replace with your icon path
        self.updata_button.clicked.connect(self.updata_account)
        buttons_layout.addWidget(self.updata_button)

        # Back button
        self.back_button = QPushButton("   عودة")
        self.back_button.setObjectName("back_button")
        self.back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        self.back_button.clicked.connect(self.back_to_login)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def back_to_login(self):
        self.close()
        self.parent.show() 
           
    def updata_account(self):
        username = self.username_input.text()
        new_password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not new_password or not confirm_password:
            QMessageBox.warning(self, "خطأ", "يجب ملء جميع الحقول.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "خطأ", "كلمتا المرور غير متطابقتان.")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "خطأ", "يجب أن تحتوي كلمة المرور على 6 أحرف على الأقل.")
            return

        try:
            # Load users from the JSON file
            users = self.load_users()

            if username not in users:
                QMessageBox.warning(self, "خطأ", "اسم المستخدم غير موجود.")
                return

            # Update the password
            users[username]["password"] = new_password
            self.save_users(users)

            QMessageBox.information(self, "نجاح", "تم تحديث كلمة المرور بنجاح!")
            self.back_to_login()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحديث كلمة المرور: {e}")

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_users(self, users):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

# واجهة المدرس
class TeacherMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" المدرسين ")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("image/chalkboard-user (1).png"))  # Replace with your icon path
        
        # CSS for styling
        self.setStyleSheet("""
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
            QPushButton:pressed {
                background-color: #083A8A;
            }
            QPushButton#Button_exit {
                background-color: #EB9BBE;           
            }
            QPushButton#Button_exit:hover {
                background-color: #C2809D;
            }
            QPushButton#back_button {
                background-color: #EB9BBE;
            }
            QPushButton#back_button:hover {
                background-color: #C2809D;
            }               
        """)

        #student layout
        layout_student = QVBoxLayout()

        # # Welcome Label
        # self.label = QLabel("مرحبًا بك في نظام إدارة المدرسين", self)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label.setFont(QFont("Arial", 24))
        # layout_student.addWidget(self.label)

        # Add company logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/user.png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_student.addWidget(self.logo_label)

        #buttons        
        self.Button_add_student=QPushButton('اضافة طالب ')
        self.Button_add_student.clicked.connect(self.add_student)
        layout_student.addWidget(self.Button_add_student)

        self.Button_check=QPushButton('تحضير الطلاب')
        self.Button_check.clicked.connect(self.check_student)
        layout_student.addWidget(self.Button_check)
        
        self.Button_display_student=QPushButton('عرض الطلاب')
        self.Button_display_student.clicked.connect(self.display_student)
        layout_student.addWidget(self.Button_display_student)

        self.button_add_homework=QPushButton('اضافة تكاليف ')
        self.button_add_homework.clicked.connect(self.add_homework)
        layout_student.addWidget(self.button_add_homework)

        self.button_add_socre=QPushButton('اضافة درجات ')
        self.button_add_socre.clicked.connect(self.add_socre)
        layout_student.addWidget(self.button_add_socre)

        #buttons layout
        
        self.Button_exit=QPushButton(' خروج')
        self.Button_exit.setObjectName("Button_exit")
        self.Button_exit.clicked.connect(self.close_application)
        layout_student.addWidget(self.Button_exit)
        
        self.setLayout(layout_student)
    

    def close_application(self):
        QApplication.quit()   

    def add_student(self):
        self.add_student_window = AddStudentWindow()
        self.add_student_window.show()

    def check_student(self):
        self.attendance_window = MarkAttendanceWindow()
        self.attendance_window.show()

    def display_student(self):
        self.display_students_window = DisplayStudentsWindow()
        self.display_students_window.show()
    
    def add_homework(self):
        self.add_homework_window = AddAssignmentsWindow()
        self.add_homework_window.show()

    def add_socre(self):
        self.add_socre_homework_window = AddSocreAssignmentsWindow()
        self.add_socre_homework_window.show()

    def close_application(self):
        QApplication.quit() 

# اضافة طالب
class AddStudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة طالب جديد")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        layout = QVBoxLayout()

        # إدخال بيانات الطالب
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("اسم الطالب")
        self.name_input.setStyleSheet("""
           QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)
        layout.addWidget(self.name_input)

        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("الرقم التعريفي")
        self.id_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)
        layout.addWidget(self.id_input)

        self.department_input = QLineEdit(self)
        self.department_input.setPlaceholderText("القسم")
        self.department_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)
        layout.addWidget(self.department_input)

        buttons_layout=QHBoxLayout()
        # زر الحفظ
        save_button = QPushButton("حفظ الطالب")
        save_button.clicked.connect(self.save_student)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
            
        """)
        buttons_layout.addWidget(save_button)
        
        # Back button
        self.back_button = QPushButton("   عودة")
        self.back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        self.back_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.back_button)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;
            }
        """)
       
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    # وظيفة لقراءة البيانات من ملف JSON
    def load_students_data(self):  # أضف self هنا لجعلها جزءاً من الكائن
        try:
            with open('student.json', "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    # وظيفة لحفظ البيانات في ملف JSON
    def save_students_data(self, data):  # أضف self هنا لجعلها جزءاً من الكائن
        with open('student.json', "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_student(self):
        #strip() لإزالة أي مسافات زائدة في بداية أو نهاية النص.
        name = self.name_input.text().strip()
        student_id = self.id_input.text().strip()
        department = self.department_input.text().strip()

        if not name or not student_id or not department:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return

        # تحميل البيانات
        students = self.load_students_data()

        # التأكد من أن الرقم التعريفي غير موجود
        if student_id in students:
            QMessageBox.warning(self, "خطأ", "الرقم التعريفي موجود بالفعل.")
            return

        # إضافة الطالب
        students[student_id] = {
            "name": name,
            "department": department,
            "attendance": [],
            "grades": {},
            "assignments": {}
        }
        # حفظ البيانات
        self.save_students_data(students)

        QMessageBox.information(self, "نجاح", "تم حفظ بيانات الطالب بنجاح.")
        self.close()

# حضور وغياب
class MarkAttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تحضير الطلاب")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar


        layout = QVBoxLayout()

        self.students = self.load_students_data()
        self.student_selector = QComboBox(self)
        self.student_selector.addItems(self.students.keys())
        layout.addWidget(self.student_selector)

        self.attendance_selector = QComboBox(self)
        self.attendance_selector.addItems(["حاضر", "غائب"])
        layout.addWidget(self.attendance_selector)

        buttons_layout=QHBoxLayout()

        save_button = QPushButton("حفظ الحضور")
        save_button.clicked.connect(self.save_attendance)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
        """)
        buttons_layout.addWidget(save_button)
        
        # Back button
        self.back_button = QPushButton("   عودة")
        self.back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        self.back_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.back_button)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;
            }
        """)
       
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def save_attendance(self):
        #هذه الدالة تسترجع النص الحالي الذي تم تحديده من القائمة المنسدلة. currentText()
        student_id = self.student_selector.currentText()
        attendance_status = self.attendance_selector.currentText()

        if student_id:
            self.students[student_id]["attendance"].append(attendance_status)
            self.save_students_data(self.students)
            QMessageBox.information(self, "نجاح", "تم حفظ حالة الحضور بنجاح.")
            self.close()
    
    # وظيفة لقراءة البيانات من ملف JSON
    def load_students_data(self):  # أضف self هنا لجعلها جزءاً من الكائن
        try:
            with open('student.json', "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    # وظيفة لحفظ البيانات في ملف JSON
    def save_students_data(self, data):  # أضف self هنا لجعلها جزءاً من الكائن
        with open('student.json', "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# عرض الطلاب
class DisplayStudentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("عرض الطلاب")
        self.setWindowIcon(QIcon("assets/ai.png"))  # Replace with your icon path
        self.setFixedSize(900, 500) 
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar


        # Layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("قائمة الطلاب")
        title_label.setFont(QFont("Arial", 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن طالب بالاسم أو الرقم التعريفي")
        self.search_input.textChanged.connect(self.filter_students)
        layout.addWidget(self.search_input)

        # Table Widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  # Columns: ID, Name, Department, Attendance, Grades
        self.table_widget.setHorizontalHeaderLabels(["الرقم التعريفي", "الاسم", "القسم", "الحضور", "الدرجات","التكاليف"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_widget)

        # Back Button
        back_button = QPushButton("    عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.setObjectName('back_button')
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        self.setLayout(layout)

        # CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #2c3e50;
                margin-bottom: 10px;
            }
                           
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
             }
           
            QTableWidget {
                border: 1px solid #083A8A;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
             
            QPushButton#back_button {
                background-color: #EB9BBE;
            }
            QPushButton#back_button:hover {
                background-color: #C2809D;
            }      
       
        """)

        # Load Student Data
        self.load_students()
        
    def load_students(self):
        """Load student data from JSON file."""
        if not os.path.exists("student.json"):
            self.students = {}
            return

        try:
            with open("student.json", "r", encoding="utf-8") as f:
                self.students = json.load(f)
            self.populate_table(self.students)  # استدعاء populate_table لعرض البيانات
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {e}")


    def populate_table(self, data):
        """Fill the table with student data."""
        self.table_widget.setRowCount(len(data))  # تعيين عدد الصفوف بناءً على عدد الطلاب

        for row, (student_id, info) in enumerate(data.items()):

            # الرقم التعريفي
            self.table_widget.setItem(row, 0, QTableWidgetItem(student_id))

            # الاسم
            self.table_widget.setItem(row, 1, QTableWidgetItem(info.get("name", "غير متوفر")))

            # القسم
            self.table_widget.setItem(row, 2, QTableWidgetItem(info.get("department", "غير متوفر")))

            # الحضور
            attendance = ", ".join(info.get("attendance", []))
            self.table_widget.setItem(row, 3, QTableWidgetItem(attendance if attendance else "لا توجد بيانات"))

            # الدرجات
            grades = ", ".join(f"{k}: {v}" for k, v in info.get("grades", {}).items())
            self.table_widget.setItem(row, 4, QTableWidgetItem(grades if grades else "لا توجد بيانات"))

            # التكاليف
            costs = info.get("costs", None)  # الحصول على حقل التكاليف
            if costs:  # إذا كانت التكاليف موجودة
                self.table_widget.setItem(row, 5, QTableWidgetItem("تم الحل" if costs.get("resolved", False) else "لم يتم الحل"))
            else:  # إذا لم تكن هناك بيانات عن التكاليف
                self.table_widget.setItem(row, 5, QTableWidgetItem("لا توجد بيانات"))

                

    def filter_students(self):
        """Filter students based on search input."""
        search_text = self.search_input.text().lower()

        filtered_students = {
            student_id: student_info
            for student_id, student_info in self.students.items()
            if search_text in student_id.lower() or search_text in student_info["name"].lower()
        }

        self.populate_table(filtered_students)

#اضافة تكليف 
class AddAssignmentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة تكاليف")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar


        layout = QVBoxLayout()

        self.assignment_input = QLineEdit(self)
        self.assignment_input.setPlaceholderText("وصف التكليف")
        layout.addWidget(self.assignment_input)

        button_layout=QHBoxLayout()

        save_button = QPushButton("إرسال التكليف")
        save_button.clicked.connect(self.save_assignment)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
                
            }
        """)
        button_layout.addWidget(save_button)

        # Back Button
        back_button = QPushButton("    عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.clicked.connect(self.close)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;;
   
            }
        """)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_assignment(self):
        assignment = self.assignment_input.text().strip()

        if not assignment:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال وصف التكليف.")
            return

        students = self.load_students_data()
        for student_id in students:
            students[student_id]["assignments"][assignment] = "لم يتم الحل"

        self.save_students_data(students)
        QMessageBox.information(self, "نجاح", "تم إرسال التكليف بنجاح.")
        self.close()

        # وظيفة لقراءة البيانات من ملف JSON
    def load_students_data(self):  # أضف self هنا لجعلها جزءاً من الكائن
        try:
            with open('student.json', "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    # وظيفة لحفظ البيانات في ملف JSON
    def save_students_data(self, data):  # أضف self هنا لجعلها جزءاً من الكائن
        with open('student.json', "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# اضافة درجات
class AddSocreAssignmentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة درجات")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        layout = QVBoxLayout()

        # Load students data
        self.students = self.load_students_data()

        # Student Selector
        self.student_selector = QComboBox(self)
        self.student_selector.addItems(self.students.keys())  # Add student IDs to the dropdown
        layout.addWidget(self.student_selector)

        # Subject Selector (Dropdown for predefined subjects)
        self.subject_selector = QComboBox(self)
        self.subject_selector.addItems(["معمارية حاسوب", "هياكل بيانات", "ذكاء اصطناعي", "برمجه", "إحصاء"])  # Add predefined subjects
        layout.addWidget(self.subject_selector)

        # Grade Input
        self.grade_input = QLineEdit(self)
        self.grade_input.setPlaceholderText("الدرجة")
        self.grade_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        """)
        layout.addWidget(self.grade_input)

        # Buttons Layout
        button_layout = QHBoxLayout()

        # Save Button
        save_button = QPushButton("حفظ الدرجة")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
        """)
        save_button.clicked.connect(self.save_grade)
        button_layout.addWidget(save_button)

        # Back Button
        back_button = QPushButton("    عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.clicked.connect(self.close)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;
            }
        """)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_grade(self):
        """Save the grade for the selected student and subject."""
        student_id = self.student_selector.currentText()
        subject = self.subject_selector.currentText()  # Get the selected subject from the dropdown
        grade = self.grade_input.text().strip()

        if not grade:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال الدرجة.")
            return

        if not grade.isdigit():
            QMessageBox.warning(self, "خطأ", "يرجى إدخال درجة صالحة.")
            return

        grade = int(grade)

        # Update the student's grades
        self.students[student_id]["grades"][subject] = grade
        self.save_students_data(self.students)

        QMessageBox.information(self, "نجاح", "تم حفظ الدرجة بنجاح.")
        self.close()

    def load_students_data(self):
        """Load students data from JSON."""
        try:
            with open('student.json', "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_students_data(self, data):
        """Save updated students data to JSON."""
        with open('student.json', "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# واجهة طالب
class StudentMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" الطلاب ")
        self.setWindowIcon(QIcon("image/book-open-reader.png"))  # Replace with your icon path
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        # CSS for styling
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
            QPushButton:pressed {
                background-color: #083A8A;
            }
            QPushButton#Button_exit {
                background-color: #EB9BBE;           
            }
            QPushButton#Button_exit:hover {
                background-color: #C2809D;
            }
        """)

        #student layout
        layout_student = QVBoxLayout()

        # Welcome Label
        self.welcome_label = QLabel("مرحبًا بك في نظام إدارة الطلاب", self)
        
        # Welcome Label
        #self.welcome_label = QLabel(f" مرحبًا بك، طالب رقم في نظام ادارة الطلاب: {self} ")
        self.welcome_label.setFont(QFont("Arial", 24))
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_student.addWidget(self.welcome_label)

        # Add company logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("image/user.png")  # Replace with your company's logo
        scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_student.addWidget(self.logo_label)

        #buttons        
        self.Button_display=QPushButton('عرض بيانات الطالب')
        self.Button_display.clicked.connect(self.data_display)
        layout_student.addWidget(self.Button_display)

        self.Button_img=QPushButton('رفع صورة شخصية')
        self.Button_img.clicked.connect(self.upload_image)
        layout_student.addWidget(self.Button_img)
        self.Button_display_homework = QPushButton('عرض التكاليف')
        self.Button_display_homework.clicked.connect(self.homework_display)
        layout_student.addWidget(self.Button_display_homework)

        self.Button_display_homework_check = QPushButton('حل التكاليف')
        self.Button_display_homework_check.clicked.connect(self.homework_check_display)
        layout_student.addWidget(self.Button_display_homework_check)
       
        self.Button_exit=QPushButton(' خروج')
        self.Button_exit.setObjectName("Button_exit")
        self.Button_exit.clicked.connect(self.close_application)
        layout_student.addWidget(self.Button_exit)


        self.setLayout(layout_student)

    def close_application(self):
        QApplication.quit()   

    def data_display(self):
        self.id_window = Student_id_Window()
        self.id_window.show()

    def homework_display(self):
        self.display_window_home = DisplayHomeworkWindow()
        self.display_window_home.show()

    def homework_check_display(self):
        self.solve_homework_window = CheckHomeworkWindow()
        self.solve_homework_window.show()

    def upload_image(self):
        # Open file dialog to select an image
        file_path, _ = QFileDialog.getOpenFileName(
        self, "اختر صورة", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        if file_path:
            # Load the selected image into QLabel
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.logo_label.setPixmap(scaled_pixmap)
                QMessageBox.information(self, "رفع صورة", f"تم رفع الصورة بنجاح: {file_path}")
            else:
                QMessageBox.warning(self, "خطأ", "تعذر تحميل الصورة. يرجى اختيار ملف صورة صالح.")
        else:
            QMessageBox.information(self, "إلغاء", "لم يتم اختيار أي صورة.")

# نافذة إدخال ID الطالب
class Student_id_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الرقك التعريفي")
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.setStyleSheet("""
        QLabel {
                color: #34495e;
            }

        QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
        QLineEdit:focus {
                border: 2px solid #083A8A;
            }
        QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
            QPushButton:pressed {
                background-color: #083A8A;
            }
            QPushButton#Button_back {
                background-color: #EB9BBE;           
            }
            QPushButton#Button_back:hover {
                background-color: #C2809D;
            }
        """)
        # Layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("أدخل الرقم التعريفي الخاص بك")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Student ID Input
        self.id_input = QLineEdit()
        self.id_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.id_input)

        button_H=QHBoxLayout()
        # Submit Button
        submit_button = QPushButton("عرض البيانات")
        submit_button.clicked.connect(self.open_student_data_window)
        button_H.addWidget(submit_button)
       
        back_button = QPushButton("   عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.setObjectName("Button_back")
        back_button.clicked.connect(self.close)
        button_H.addWidget(back_button)

        layout.addLayout(button_H)
        self.setLayout(layout)

    def open_student_data_window(self):
        student_id = self.id_input.text().strip()

        if not student_id:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال الرقم التعريفي الخاص بك.")
            return

        # Load student data
        if not os.path.exists("student.json"):
            QMessageBox.critical(self, "خطأ", "ملف بيانات الطلاب غير موجود.")
            return

        try:
            with open("student.json", "r", encoding="utf-8") as f:
                students = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء قراءة ملف البيانات: {e}")
            return

        # Check if the student ID exists
        if student_id not in students:
            QMessageBox.warning(self, "خطأ", "الرقم التعريفي غير موجود.")
            return

        # Open the student data window
        self.student_data_window = Display_Students_Window(student_id, students[student_id])
        self.student_data_window.show()
        self.close()

# عرض الطلاب
class Display_Students_Window(QWidget):
    def __init__(self, student_id, student_data):
        super().__init__()
        self.setWindowTitle("عرض البياات الشخصية لطالب")
        self.setWindowIcon(QIcon("assets/ai.png"))  # Replace with your icon path
        self.setFixedSize(600, 500) 
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar


        # Layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel(f"بيانات الطالب - {student_data.get('name', 'غير معروف')}")
        title_label.setFont(QFont("Arial", 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Table Widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Columns: Key, Value
        self.table_widget.setHorizontalHeaderLabels(["الحقل", "القيمة"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_widget)

        # Back Button
        back_button = QPushButton("    عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.setObjectName('back_button')
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)


        # CSS
        self.setStyleSheet("""
             QWidget {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #2c3e50;
                margin-bottom: 10px;
            }
                           
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #083A8A;
             }
           
            QTableWidget {
                border: 1px solid #0945A3;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
             
            QPushButton#back_button {
                background-color: #EB9BBE;
            }
            QPushButton#back_button:hover {
                background-color: #C2809D;
            }      
       
        """)

        self.populate_table(student_id,student_data)

        self.setLayout(layout)
    def populate_table(self,student_id, student_data):
        """Fill the table with student data."""
        fields = {
            "الرقم التعريفي": student_id,  # Use the key as the ID
            "الاسم": student_data.get("name", "غير متوفر"),
            "القسم": student_data.get("department", "غير متوفر"),
            "الحضور": ", ".join(student_data.get("attendance", [])) or "لا توجد بيانات",
            "الدرجات": ", ".join(f"{subject}: {grade}" for subject, grade in student_data.get("grades", {}).items()) or "لا توجد بيانات",
            "التكاليف": ", ".join(f"{assignment}: {'تم الحل' if status == 'تم الحل' else 'لم يتم الحل'}"
                                   for assignment, status in student_data.get("assignments", {}).items()) or "لا توجد بيانات"
        }

        self.table_widget.setRowCount(len(fields))

        for row, (key, value) in enumerate(fields.items()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(key))
            self.table_widget.setItem(row, 1, QTableWidgetItem(value))

# نافذة عرض التكاليف
class DisplayHomeworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("عرض التكاليف")
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar


        # Layout
        layout = QVBoxLayout()

        # Title Label
        self.label = QLabel(" التكاليف")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 18))
        layout.addWidget(self.label)


        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["التكليف", "الحالة"])
        layout.addWidget(self.table_widget)


        self.load_assignments()

       
        # Back Button
        back_button = QPushButton("    عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.clicked.connect(self.close)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;;
   
            }
        """)
        layout.addWidget(back_button)

        self.setLayout(layout)
    
    # وظيفة لقراءة البيانات من ملف JSON
    def load_students_data(self):
        try:
            with open("student.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "خطأ", "ملف بيانات الطلاب غير موجود.")
            return {}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء قراءة ملف البيانات.")
            return {}
    def load_assignments(self):
        try:
            students = self.load_students_data()

            # اختيار المعرف الخاص بالطالب (هنا افترضنا "1")
            student_id = "1"  # يمكنك تغيير هذا بناءً على الطالب المطلوب
            student_data = students.get(student_id, {})

            # الحصول على قائمة التكاليف من بيانات الطالب
            assignments = student_data.get("assignments", {})

            # إعداد الجدول
            self.table_widget.setRowCount(len(assignments))
            for row, (assignment, status) in enumerate(assignments.items()):
                self.table_widget.setItem(row, 0, QTableWidgetItem(assignment))
                if status == True:  # إذا كانت القيمة منطقية (Boolean)
                    status_text = "تم الحل"
                else:
                    status_text = str(status)  # عرض النص كما هو (مثل "لم يتم الحل")
                self.table_widget.setItem(row, 1, QTableWidgetItem(status_text))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {e}")

# نافذة حل التكاليف
class CheckHomeworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("حل التكاليف")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar

        # Layout
        layout = QVBoxLayout()

        # Title Label
        self.label = QLabel(" اكتب حلك لتكليف:  ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 18))
        layout.addWidget(self.label)

        # Student Selector (Dropdown for Student IDs)
        self.student_selector = QComboBox()
        self.student_selector.addItem("اختر الطالب")  # Default option
        self.students = self.load_students_data()
        self.student_selector.addItems(self.students.keys())  # Add student IDs to the dropdown
        self.student_selector.currentIndexChanged.connect(self.load_assignments)  # Trigger on student selection
        layout.addWidget(self.student_selector)

        # Assignment Selector (Dropdown for Assignments)
        self.assignment_selector = QComboBox()
        layout.addWidget(self.assignment_selector)

        # Text Edit for Solution
        self.solution_input = QTextEdit()
        self.solution_input.setPlaceholderText("اكتب الحل هنا...")
        layout.addWidget(self.solution_input)

        # Submit Button
        submit_button = QPushButton("إرسال الحل")
        submit_button.clicked.connect(self.submit_solution)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0A4CB3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #083A8A;
            }
        """)
        layout.addWidget(submit_button)

        # Back Button
        back_button = QPushButton("عودة")
        back_button.setIcon(QIcon("image/home (2).png"))  # Replace with your icon path
        back_button.clicked.connect(self.close)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #EB9BBE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C2809D;
            }
        """)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_students_data(self):
        """Load students data from JSON."""
        try:
            with open("student.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "خطأ", "ملف بيانات الطلاب غير موجود.")
            return {}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء قراءة ملف البيانات.")
            return {}

    def load_assignments(self):
        """Load assignments for the selected student into the dropdown."""
        student_id = self.student_selector.currentText()

        # إذا لم يتم تحديد طالب، قم بإفراغ قائمة التكاليف
        if student_id == "اختر الطالب":
            self.assignment_selector.clear()
            return

        # Load assignments for the selected student
        student_data = self.students.get(student_id, {})
        assignments = student_data.get("assignments", {})

        # Clear and populate the assignment selector
        self.assignment_selector.clear()
        for assignment_name, assignment_details in assignments.items():
            if isinstance(assignment_details, dict):
                # Check the "state" field if it's a dictionary
                if assignment_details.get("state") == "لم يتم الحل":
                    self.assignment_selector.addItem(assignment_name)
            elif isinstance(assignment_details, str):
                # If it's a string, assume it's "لم يتم الحل"
                if assignment_details == "لم يتم الحل":
                    self.assignment_selector.addItem(assignment_name)

    def save_students_data(self, students):
        """Save updated students data to JSON."""
        try:
            with open("student.json", "w", encoding="utf-8") as f:
                json.dump(students, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ البيانات: {e}")

    def submit_solution(self):
        """Handle solution submission."""
        student_id = self.student_selector.currentText()
        assignment_name = self.assignment_selector.currentText()
        solution = self.solution_input.toPlainText().strip()

        # Ensure a student and assignment are selected
        if student_id == "اختر الطالب":
            QMessageBox.warning(self, "خطأ", "يرجى اختيار الطالب.")
            return

        if not assignment_name:
            QMessageBox.warning(self, "خطأ", "يرجى اختيار التكليف.")
            return

        if not solution:
            QMessageBox.warning(self, "خطأ", "يرجى كتابة الحل.")
            return

        # Load students data
        student_data = self.students.get(student_id)

        if not student_data:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على الطالب بمعرف {student_id}.")
            return

        # Ensure the assignment exists
        assignments = student_data.get("assignments", {})
        if assignment_name not in assignments:
            QMessageBox.warning(self, "خطأ", f"التكليف '{assignment_name}' غير موجود.")
            return

        # Update the assignment state and save the solution
        if isinstance(assignments[assignment_name], dict):
            # If it's a dictionary, update the state and describe
            assignments[assignment_name]["state"] = "تم الحل"
            assignments[assignment_name]["describe"] = solution
        elif isinstance(assignments[assignment_name], str):
            # If it's a string, replace it with a dictionary
            assignments[assignment_name] = {"describe": solution, "state": "تم الحل"}

        # Save updated data
        self.save_students_data(self.students)

        QMessageBox.information(self, "نجاح", "تم إرسال الحل بنجاح.")
        self.close()

# Run the application
app = QApplication([])
login_window = LoginWindow()
login_window.show()
app.exec()
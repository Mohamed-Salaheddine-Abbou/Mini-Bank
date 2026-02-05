from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from PySide6.QtGui import QPixmap
import sys
import os
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import authenticate_admin

class AdminLoginView(QWidget):
    def __init__(self, parent=None, on_success=None):
        super().__init__(parent)
        self.on_success = on_success
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Left Side (Form) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.addStretch()
        
        container = QWidget()
        container.setFixedWidth(350)

        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Admin Login")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Username"))
        self.user_entry = QLineEdit()
        self.user_entry.setPlaceholderText("Username")
        layout.addWidget(self.user_entry)
        
        layout.addWidget(QLabel("Password"))
        self.pass_entry = QLineEdit()
        self.pass_entry.setEchoMode(QLineEdit.Password)
        self.pass_entry.setPlaceholderText("Password")
        layout.addWidget(self.pass_entry)
        
        btn = QPushButton("Login")
        btn.clicked.connect(self.login)
        btn.setMinimumHeight(40)
        layout.addWidget(btn)
        
        left_layout.addWidget(container, 0, Qt.AlignCenter)
        left_layout.addStretch()

        # --- Right Side (Logo) ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignCenter)

        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.svg')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(logo_label)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)
        self.setLayout(main_layout)

    def login(self):
        if authenticate_admin(self.user_entry.text(), self.pass_entry.text()):
            self.on_success()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")
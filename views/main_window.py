from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
import os
from views.login import LoginView
from views.create_account import CreateAccountView
from views.dashboard import DashboardView
from views.send_money import SendMoneyView
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboardView

GLOBAL_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}
QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #3e3e3e;
    color: #ffffff;
    padding: 8px;
    border-radius: 6px;
}
QPushButton {
    background-color: #333333;
    border: 1px solid #444444;
    color: #cccccc;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #444444;
    border-color: #555555;
}
QPushButton:pressed {
    background-color: #222222;
}
QHeaderView::section {
    background-color: #2d2d2d;
    color: #cccccc;
    padding: 6px;
    border: 1px solid #3e3e3e;
}
QTableWidget {
    gridline-color: #3e3e3e;
    background-color: #1e1e1e;
    color: #cccccc;
    selection-background-color: #3a3a3a;
}
QTabWidget::pane {
    border: 1px solid #3e3e3e;
}
QTabBar::tab {
    background-color: #2d2d2d;
    color: #cccccc;
    padding: 8px 16px;
    border: 1px solid #3e3e3e;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #444444;
}
QTextEdit {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e3e;
}
QDialog {
    background-color: #1e1e1e;
}
QMessageBox {
    background-color: #1e1e1e;
    color: #cccccc;
}
"""

class MainWindow(QMainWindow):
    def __init__(self, enable_admin=True):
        super().__init__()
        self.setWindowTitle("MiniBank - PySide6")
        self.resize(900, 600)
        self.enable_admin = enable_admin
        
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'bank_logo.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setStyleSheet(GLOBAL_STYLE)
        self.show_menu()

    def show_menu(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Left Side (Menu) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.addStretch()

        container = QWidget()
        container.setFixedWidth(350)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        title = QLabel("MiniBank System")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.show_login)
        btn_login.setMinimumHeight(40)
        
        btn_create = QPushButton("Create Account")
        btn_create.clicked.connect(self.show_create_account)
        btn_create.setMinimumHeight(40)
        
        layout.addWidget(btn_login)
        layout.addWidget(btn_create)

        if self.enable_admin:
            btn_admin = QPushButton("Admin Panel")
            btn_admin.clicked.connect(self.show_admin_login)
            btn_admin.setMinimumHeight(40)
            layout.addWidget(btn_admin)
        
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
        
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def show_login(self):
        self.setCentralWidget(LoginView(on_login_success=self.show_dashboard, on_back=self.show_menu))

    def show_create_account(self):
        self.setCentralWidget(CreateAccountView(on_back=self.show_menu))

    def show_dashboard(self, user_id):
        self.setCentralWidget(DashboardView(
            user_id=user_id, 
            on_logout=self.show_menu,
            on_send_money=self.show_send_money
        ))

    def show_send_money(self, user_id):
        self.setCentralWidget(SendMoneyView(
            user_id=user_id, 
            on_back=lambda: self.show_dashboard(user_id)
        ))

    def show_admin_login(self):
        self.setCentralWidget(AdminLoginView(on_success=self.show_admin_dashboard))

    def show_admin_dashboard(self):
        self.setCentralWidget(AdminDashboardView(on_logout=self.show_menu))

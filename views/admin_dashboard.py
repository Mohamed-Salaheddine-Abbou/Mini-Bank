from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget, 
                               QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QHeaderView)
import sys
import os
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import (
    fetch_all_users, remove_user, fetch_stats,
    fetch_all_admins, fetch_global_transactions
)

class AdminDashboardView(QWidget):
    def __init__(self, parent=None, on_logout=None):
        super().__init__(parent)
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Admin Panel")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(title)
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.on_logout)
        header.addWidget(logout_btn)
        layout.addLayout(header)

        # Stats
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.stats_label)
        self.refresh_stats()

        # Tabs
        self.tabs = QTabWidget()
        self.users_tab = QWidget()
        self.admins_tab = QWidget()
        self.trans_tab = QWidget()

        self.tabs.addTab(self.users_tab, "Users")
        self.tabs.addTab(self.admins_tab, "Admins")
        self.tabs.addTab(self.trans_tab, "Transactions")
        
        self.setup_users_tab()
        self.setup_admins_tab()
        self.setup_trans_tab()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def refresh_stats(self):
        count, money = fetch_stats()
        self.stats_label.setText(f"Total Users: {count} | Total Funds: {money:.2f} DA")

    def setup_users_tab(self):
        layout = QVBoxLayout()
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Account", "Balance"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_users)
        
        delete_btn = QPushButton("Delete User")
        delete_btn.clicked.connect(self.delete_user)

        layout.addWidget(self.users_table)
        layout.addWidget(refresh_btn)
        layout.addWidget(delete_btn)
        self.users_tab.setLayout(layout)
        self.load_users()

    def load_users(self):
        users = fetch_all_users()
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            for j, val in enumerate(user):
                self.users_table.setItem(i, j, QTableWidgetItem(str(val)))
        self.refresh_stats()

    def delete_user(self):
        row = self.users_table.currentRow()
        if row < 0: return
        user_id = self.users_table.item(row, 0).text()
        if remove_user(user_id):
            self.load_users()

    def setup_admins_tab(self):
        layout = QVBoxLayout()
        self.admins_table = QTableWidget()
        self.admins_table.setColumnCount(2)
        self.admins_table.setHorizontalHeaderLabels(["ID", "Username"])
        self.admins_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.admins_table)
        self.admins_tab.setLayout(layout)
        self.load_admins()

    def load_admins(self):
        admins = fetch_all_admins()
        self.admins_table.setRowCount(len(admins))
        for i, admin in enumerate(admins):
            for j, val in enumerate(admin):
                self.admins_table.setItem(i, j, QTableWidgetItem(str(val)))

    def setup_trans_tab(self):
        layout = QVBoxLayout()
        self.trans_table = QTableWidget()
        self.trans_table.setColumnCount(5)
        self.trans_table.setHorizontalHeaderLabels(["ID", "User", "Type", "Amount", "Date"])
        layout.addWidget(self.trans_table)
        self.trans_tab.setLayout(layout)
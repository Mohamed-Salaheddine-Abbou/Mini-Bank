from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, 
                               QMessageBox, QInputDialog, QDialog, QTextEdit)
from PySide6.QtCore import Qt, QTimer
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.transaction_controller import deposit, withdraw, get_account_history
from controllers.notification_controller import get_my_notifications, read_notifications
from models.user_model import get_user_by_id
from models.transaction_model import get_balance

class DashboardView(QWidget):
    def __init__(self, parent=None, user_id=None, on_logout=None, on_send_money=None):
        super().__init__(parent)
        self.user_id = user_id
        self.on_logout = on_logout
        self.on_send_money = on_send_money
        self.init_ui()
        self.update_balance()
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_notification)
        self.check_notifications()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Header
        self.welcome_label = QLabel("Welcome to your Dashboard")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.welcome_label)

        # Balance
        self.balance_label = QLabel("Loading...")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.balance_label)

        # Grid for Actions
        grid = QGridLayout()
        grid.setSpacing(10)
        
        btn_deposit = QPushButton("Deposit")
        btn_deposit.clicked.connect(self.handle_deposit)
        
        btn_withdraw = QPushButton("Withdraw")
        btn_withdraw.clicked.connect(self.handle_withdraw)
        
        btn_transfer = QPushButton("Transfer Money")
        btn_transfer.clicked.connect(lambda: self.on_send_money(self.user_id))
        
        btn_history = QPushButton("Transactions")
        btn_history.clicked.connect(self.show_transactions)
        
        self.btn_notif = QPushButton("Notifications")
        self.btn_notif.clicked.connect(self.show_notifications)
        
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.on_logout)

        grid.addWidget(btn_deposit, 0, 0)
        grid.addWidget(btn_withdraw, 0, 1)
        grid.addWidget(btn_transfer, 1, 0)
        grid.addWidget(btn_history, 1, 1)
        grid.addWidget(self.btn_notif, 2, 0)
        grid.addWidget(btn_logout, 2, 1)

        layout.addLayout(grid)
        self.setLayout(layout)

    def update_balance(self):
        balance = get_balance(self.user_id)
        self.balance_label.setText(f"Balance: {balance:.2f} DA" if balance is not None else "N/A")

    def handle_deposit(self):
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Amount:", 0, 0, 1000000, 2)
        if ok and amount > 0:
            success, msg = deposit(self.user_id, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.update_balance()
            else:
                QMessageBox.warning(self, "Error", msg)

    def handle_withdraw(self):
        amount, ok = QInputDialog.getDouble(self, "Withdraw", "Amount:", 0, 0, 1000000, 2)
        if ok and amount > 0:
            success, msg = withdraw(self.user_id, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.update_balance()
            else:
                QMessageBox.warning(self, "Error", msg)

    def show_transactions(self):
        txs = get_account_history(self.user_id)
        text = "\n".join([f"{t[2]}: {t[0]} {t[1]:.2f} DA" for t in txs]) if txs else "No transactions."
        self.show_info_dialog("Transaction History", text)

    def check_notifications(self):
        notifs = get_my_notifications(self.user_id)
        self.notif_count = len(notifs)
        
        if self.notif_count > 0:
            if not self.blink_timer.isActive():
                self.blink_timer.start(500)
        else:
            self.blink_timer.stop()
            self.btn_notif.setText("Notifications")

    def blink_notification(self):
        text = self.btn_notif.text()
        if "🔴" in text:
            self.btn_notif.setText(f"Notifications ({self.notif_count})")
        else:
            self.btn_notif.setText(f"Notifications ({self.notif_count}) 🔴")

    def show_notifications(self):
        notifs = get_my_notifications(self.user_id)
        text = "\n".join([n[0] for n in notifs]) if notifs else "No new notifications."
        self.show_info_dialog("Notifications", text)
        read_notifications(self.user_id)
        self.check_notifications()

    def show_info_dialog(self, title, content):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(content)
        text_area.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(text_area)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec()

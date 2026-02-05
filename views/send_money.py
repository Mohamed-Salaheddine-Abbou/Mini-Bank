from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys
import os
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.transaction_controller import send_money

class SendMoneyView(QWidget):
    def __init__(self, parent=None, user_id=None, on_back=None):
        super().__init__(parent)
        self.user_id = user_id
        self.on_back = on_back
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        container = QWidget()
        container.setFixedWidth(300)

        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Send Money")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addWidget(QLabel("Receiver Account Number"))
        self.receiver_entry = QLineEdit()
        layout.addWidget(self.receiver_entry)
        
        layout.addWidget(QLabel("Amount (DA)"))
        self.amount_entry = QLineEdit()
        layout.addWidget(self.amount_entry)

        send_btn = QPushButton("Send Money")
        send_btn.clicked.connect(self.handle_send)
        layout.addWidget(send_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.on_back)
        layout.addWidget(back_btn)

        main_layout.addWidget(container, 0, Qt.AlignCenter)
        self.setLayout(main_layout)

    def handle_send(self):
        receiver = self.receiver_entry.text().strip()
        amount_str = self.amount_entry.text().strip()

        try:
            amount = float(amount_str)
            success, msg = send_money(self.user_id, receiver, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.on_back()
            else:
                QMessageBox.critical(self, "Error", msg)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount")
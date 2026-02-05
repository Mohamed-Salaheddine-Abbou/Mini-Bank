import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboardView

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MiniBank Admin Panel")
        self.resize(900, 600)
        self.show_admin_login()

    def show_admin_login(self):
        self.setCentralWidget(AdminLoginView(on_success=self.show_admin_dashboard))

    def show_admin_dashboard(self):
        self.setCentralWidget(AdminDashboardView(on_logout=self.show_admin_login))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec())
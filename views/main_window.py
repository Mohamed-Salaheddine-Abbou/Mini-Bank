import tkinter as tk
from views.create_account import CreateAccountForm
from views.dashboard import Dashboard
from views.login import LoginView
from views.send_money import SendMoneyView
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboard

class MainWindow(tk.Tk):
    def __init__(self, enable_admin=True):
        super().__init__()
        self.title("MiniBank")
        self.geometry("900x600")

        self.menu_frame = tk.Frame(self)

        tk.Button(self.menu_frame, text="Create Account", command=self.show_create_account).grid(row=0, column=0, padx=10)
        tk.Button(self.menu_frame, text="Login", command=self.show_login).grid(row=0, column=1, padx=10)
        
        if enable_admin:
            tk.Button(self.menu_frame, text="Admin", command=self.show_admin_login).grid(row=0, column=2, padx=10)

        self.current_frame = None

        self.show_create_account()

    def show_create_account(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.menu_frame.pack(pady=20)
        self.current_frame = CreateAccountForm(self)
        self.current_frame.pack()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.menu_frame.pack(pady=20)
        self.current_frame = LoginView(self, on_login_success=self.show_dashboard)
        self.current_frame.pack()

    def show_admin_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.menu_frame.pack(pady=20)
        self.current_frame = AdminLoginView(self, on_success=self.show_admin_dashboard)
        self.current_frame.pack()

    def show_admin_dashboard(self):
        self.menu_frame.pack_forget()
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AdminDashboard(self)
        self.current_frame.pack()

    def show_dashboard(self, user_id):
        self.menu_frame.pack_forget()
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Dashboard(self, user_id)
        self.current_frame.pack()

    def show_send_money(self, user_id):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SendMoneyView(self, user_id, on_back=lambda: self.show_dashboard(user_id))
        self.current_frame.pack()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

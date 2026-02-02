import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import login

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack()

        tk.Label(self, text="Account Number:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.account_entry = tk.Entry(self)
        self.account_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Login", command=self.handle_login).grid(row=2, column=0, columnspan=2, pady=10)

    def handle_login(self):
        account_num = self.account_entry.get().strip()
        password = self.password_entry.get().strip()

        user, error = login(account_num, password)

        if error:
            messagebox.showerror("Login Failed", error)
        else:
            self.on_login_success(user['id'])
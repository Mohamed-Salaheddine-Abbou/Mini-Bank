import tkinter as tk
from tkinter import simpledialog, messagebox
from controllers.transaction_controller import deposit, withdraw, get_account_history
from controllers.notification_controller import get_my_notifications, read_notifications
from models.user_model import get_user_by_id

class Dashboard(tk.Frame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.pack()

        tk.Label(self, text="Welcome to your Dashboard").pack(pady=10)

        # User Info Section (Hidden by default)
        user_data = get_user_by_id(user_id)
        self.full_name = user_data[1] if user_data else "Unknown"
        self.account_number = user_data[2] if user_data else "Unknown"
        self.info_visible = False

        self.info_label = tk.Label(self, text="", font=("Arial", 10, "bold"), fg="blue")
        self.info_label.pack(pady=5)

        tk.Button(self, text="Show/Hide Details", command=self.toggle_info).pack(pady=2)

        self.balance_label = tk.Label(self, text="")
        self.balance_label.pack()

        # Container for buttons grid
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="Deposit", width=15, command=self.handle_deposit).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text="Withdraw", width=15, command=self.handle_withdraw).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(buttons_frame, text="Make a Transfer", width=15, command=self.handle_send_money).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text="Show Transactions", width=15, command=self.show_transactions).grid(row=1, column=1, padx=5, pady=5)
        
        self.notif_btn = tk.Button(buttons_frame, text="Notifications", width=15, command=self.show_notifications)
        self.notif_btn.grid(row=2, column=0, padx=5, pady=5)
        
        tk.Button(buttons_frame, text="Logout", width=15, command=self.logout).grid(row=2, column=1, padx=5, pady=5)

        self.update_balance()
        self.check_notifications()

    def toggle_info(self):
        self.info_visible = not self.info_visible
        if self.info_visible:
            self.info_label.config(text=f"Name: {self.full_name}\nAccount: {self.account_number}")
        else:
            self.info_label.config(text="")

    def check_notifications(self):
        notifs = get_my_notifications(self.user_id)
        if notifs:
            self.notif_btn.config(text=f"Notifications ({len(notifs)}) 🔴", fg="red")
        else:
            self.notif_btn.config(text="Notifications", fg="black")

    def update_balance(self):
        from models.transaction_model import get_balance
        balance = get_balance(self.user_id)
        self.balance_label.config(text=f"Current Balance: {balance:.2f} DA" if balance is not None else "Balance: N/A")

    def handle_deposit(self):
        amount_str = simpledialog.askstring("Deposit", "Enter amount to deposit:")
        if not amount_str or not amount_str.isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return
        amount = float(amount_str)
        success, msg = deposit(self.user_id, amount)
        if success:
            messagebox.showinfo("Success", msg)
            self.update_balance()
        else:
            messagebox.showerror("Error", msg)

    def handle_withdraw(self):
        amount_str = simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        if not amount_str or not amount_str.isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return
        amount = float(amount_str)
        success, msg = withdraw(self.user_id, amount)
        if success:
            messagebox.showinfo("Success", msg)
            self.update_balance()
        else:
            messagebox.showerror("Error", msg)

    def handle_send_money(self):
        self.master.show_send_money(self.user_id)

    def show_transactions(self):
        transactions = get_account_history(self.user_id)
        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found.")
            return

        # Build string of transactions
        text = ""
        for tx_type, amount, created_at in transactions:
            text += f"{created_at}: {tx_type} {amount:.2f} DA\n"

        messagebox.showinfo("Transactions History", text)

    def show_notifications(self):
        notifs = get_my_notifications(self.user_id)
        if not notifs:
            messagebox.showinfo("Notifications", "No new notifications.")
            return
        
        text = "\n".join([f"- {n[0]}" for n in notifs])
        messagebox.showinfo("New Notifications", text)
        
        read_notifications(self.user_id)
        self.check_notifications()

    def logout(self):
        self.master.show_login()

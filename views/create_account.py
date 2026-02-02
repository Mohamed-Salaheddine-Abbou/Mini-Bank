import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.account_controller import open_account
from utils.validators import is_valid_algerian_phone


class CreateAccountForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # Full Name
        tk.Label(self, text="Full Name:").grid(row=0, column=0, sticky="w")
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.grid(row=0, column=1)

        # Phone Number
        tk.Label(self, text="Phone (Algerian):").grid(row=1, column=0, sticky="w")
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=1, column=1)

        # Create Account Button
        self.create_button = tk.Button(self, text="Create Account", command=self.create_account)
        self.create_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_account(self):
        full_name = self.full_name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not full_name or not phone:
            messagebox.showerror("Error", "Please fill all fields")
            return

        if not is_valid_algerian_phone(phone):
            messagebox.showerror("Error", "Invalid Algerian phone number")
            return

        data, error = open_account(full_name, phone)
        if error:
            messagebox.showerror("Error", error)
            return

        # Account details "only once"
        msg = f"Your account has been created!\n\nAccount Number: {data['account_number']}\nPassword: {data['password']}\n\nPlease save these details now."
        messagebox.showinfo("Account Created", msg)

        # Clear after confirmation
        self.full_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MiniBank - Create Account")
    app = CreateAccountForm(master=root)
    app.mainloop()

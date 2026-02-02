import tkinter as tk
from tkinter import messagebox
from controllers.transaction_controller import send_money

class SendMoneyView(tk.Frame):
    def __init__(self, master, user_id, on_back):
        super().__init__(master)
        self.user_id = user_id
        self.on_back = on_back
        self.pack(fill=tk.BOTH, expand=True)

        # Main container for centering
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # tk.Label(container, text="Send Money", font=("Arial", 18, "bold")).pack(pady=30)

        form_frame = tk.Frame(container)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Receiver Account Number:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=15)
        self.receiver_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.receiver_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Amount (DA):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Send", command=self.handle_send, font=("Arial", 12), width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="Back", command=self.on_back, font=("Arial", 12), width=15).grid(row=0, column=1, padx=20)

    def handle_send(self):
        receiver = self.receiver_entry.get().strip()
        amount_str = self.amount_entry.get().strip()

        if not receiver:
            messagebox.showerror("Error", "Please enter receiver account number")
            return
        
        if not amount_str or not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return
            
        amount = float(amount_str)
        
        success, msg = send_money(self.user_id, receiver, amount)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.on_back()
        else:
            messagebox.showerror("Error", msg)
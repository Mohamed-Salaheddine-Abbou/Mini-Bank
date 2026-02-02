import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import authenticate_admin

class AdminLoginView(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success
        self.pack(fill=tk.BOTH, expand=True)
        
        # Container to center content
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="Admin Login", font=("Arial", 24, "bold")).pack(pady=30)
        
        tk.Label(container, text="Username:", font=("Arial", 12)).pack(anchor="w")
        self.user_entry = tk.Entry(container, font=("Arial", 12), width=30)
        self.user_entry.pack(pady=5, ipady=3)
        
        tk.Label(container, text="Password:", font=("Arial", 12)).pack(anchor="w")
        self.pass_entry = tk.Entry(container, show="*", font=("Arial", 12), width=30)
        self.pass_entry.pack(pady=5, ipady=3)
        
        tk.Button(container, text="Login", command=self.login, bg="black", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=30)

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        if authenticate_admin(u, p):
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Admin Login")
    # Dummy callback for testing
    app = AdminLoginView(master=root, on_success=lambda: print("Admin logged in!"))
    app.mainloop()
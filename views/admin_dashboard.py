import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import (
    fetch_all_users, remove_user, fetch_stats,
    fetch_all_admins, add_new_admin, remove_admin,
    fetch_global_transactions, remove_transaction
)

class AdminDashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        tk.Label(header_frame, text="Admin Panel", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        tk.Button(header_frame, text="Logout", command=self.logout, bg="#f44336", fg="white").pack(side=tk.RIGHT)
        
        # Stats Section
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(pady=5)
        self.refresh_stats()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.users_tab = tk.Frame(self.notebook)
        self.admins_tab = tk.Frame(self.notebook)
        self.trans_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.users_tab, text="Manage Users")
        self.notebook.add(self.admins_tab, text="Manage Admins")
        self.notebook.add(self.trans_tab, text="Transactions")
        
        self.setup_users_tab()
        self.setup_admins_tab()
        self.setup_trans_tab()

    def setup_users_tab(self):
        columns = ("ID", "Name", "Phone", "Account", "Balance")
        self.users_tree = ttk.Treeview(self.users_tab, columns=columns, show="headings")
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        self.users_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(self.users_tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_users).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete User", command=self.delete_selected_user, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.load_users()

    def setup_admins_tab(self):
        columns = ("ID", "Username")
        self.admins_tree = ttk.Treeview(self.admins_tab, columns=columns, show="headings")
        self.admins_tree.heading("ID", text="ID")
        self.admins_tree.heading("Username", text="Username")
        self.admins_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(self.admins_tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_admins).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Admin", command=self.create_admin_popup, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Admin", command=self.delete_selected_admin, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.load_admins()

    def setup_trans_tab(self):
        columns = ("ID", "User", "Type", "Amount", "Date")
        self.trans_tree = ttk.Treeview(self.trans_tab, columns=columns, show="headings")
        
        for col in columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=100)
            
        self.trans_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(self.trans_tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_transactions).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Transaction", command=self.delete_selected_transaction, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.load_transactions()

    def refresh_stats(self):
        count, total_money = fetch_stats()
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        tk.Label(self.stats_frame, text=f"Total Users: {count}", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(self.stats_frame, text=f"Total Funds in Bank: {total_money:.2f} DA", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        users = fetch_all_users()
        for user in users:
            self.users_tree.insert("", tk.END, values=user)
        self.refresh_stats()

    def load_admins(self):
        for item in self.admins_tree.get_children():
            self.admins_tree.delete(item)
        admins = fetch_all_admins()
        for admin in admins:
            self.admins_tree.insert("", tk.END, values=admin)

    def load_transactions(self):
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        trans = fetch_global_transactions()
        for t in trans:
            self.trans_tree.insert("", tk.END, values=t)

    def delete_selected_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        item = self.users_tree.item(selected[0])
        user_id = item['values'][0]
        user_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user_name}' (ID: {user_id})?\nThis will delete all their transactions and notifications."):
            if remove_user(user_id):
                messagebox.showinfo("Success", "User deleted successfully")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to delete user")

    def create_admin_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New Admin")
        popup.geometry("400x350")

        tk.Label(popup, text="Create New Admin", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(popup, text="Username:", font=("Arial", 12)).pack(anchor="w", padx=50)
        username_entry = tk.Entry(popup, font=("Arial", 12))
        username_entry.pack(fill="x", padx=50, pady=5)

        tk.Label(popup, text="Password:", font=("Arial", 12)).pack(anchor="w", padx=50)
        password_entry = tk.Entry(popup, show="*", font=("Arial", 12))
        password_entry.pack(fill="x", padx=50, pady=5)

        def submit():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if not u or not p:
                messagebox.showerror("Error", "All fields are required", parent=popup)
                return
            if add_new_admin(u, p):
                messagebox.showinfo("Success", "Admin created successfully", parent=popup)
                self.load_admins()
                popup.destroy()
            else:
                messagebox.showerror("Error", "Failed to create admin (Username might exist)", parent=popup)

        tk.Button(popup, text="Create", command=submit, bg="green", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=20)

    def delete_selected_admin(self):
        selected = self.admins_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an admin to delete")
            return
        
        item = self.admins_tree.item(selected[0])
        admin_id = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Delete admin '{username}'?"):
            if remove_admin(admin_id):
                messagebox.showinfo("Success", "Admin deleted")
                self.load_admins()
            else:
                messagebox.showerror("Error", "Failed to delete admin")

    def delete_selected_transaction(self):
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return
        
        item = self.trans_tree.item(selected[0])
        tx_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete transaction ID {tx_id}?"):
            if remove_transaction(tx_id):
                messagebox.showinfo("Success", "Transaction deleted")
                self.load_transactions()
            else:
                messagebox.showerror("Error", "Failed to delete transaction")

    def logout(self):
        if hasattr(self.master, 'show_admin_login'):
            self.master.show_admin_login()
        else:
            # Standalone mode: Return to login screen
            self.destroy()
            from views.admin_login import AdminLoginView
            
            def on_login_success():
                for widget in self.master.winfo_children():
                    widget.destroy()
                AdminDashboard(master=self.master)
            
            AdminLoginView(master=self.master, on_success=on_login_success)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Admin Panel")
    
    from views.admin_login import AdminLoginView
    
    def on_login_success():
        for widget in root.winfo_children():
            widget.destroy()
        app = AdminDashboard(master=root)
        
    app = AdminLoginView(master=root, on_success=on_login_success)
    root.mainloop()
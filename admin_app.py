import tkinter as tk
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboard

class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniBank Admin Panel")
        self.geometry("900x600")
        self.current_frame = None
        self.show_admin_login()

    def show_admin_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AdminLoginView(self, on_success=self.show_admin_dashboard)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_admin_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AdminDashboard(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
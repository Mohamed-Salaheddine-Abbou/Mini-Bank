from views.main_window import MainWindow

if __name__ == "__main__":
    # Launch MainWindow without the Admin button
    app = MainWindow(enable_admin=False)
    app.mainloop()
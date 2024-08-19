import customtkinter as ctk
from datetime import datetime


class MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CigiMoniPy")
        self.geometry("400x300")
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.tab1 = self.tabview.add("Main")
        self.loading_label = ctk.CTkLabel(self.tab1, text="Loading...")
        self.loading_label.pack(pady=20)
        self.tab2 = self.tabview.add("Log")
        self.log_box = ctk.CTkTextbox(self.tab2, state="disabled", height=10)
        self.log_box.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] : {message}"
        self.log_box.configure(state="normal")
        self.log_box.insert(ctk.END, message + "\n\n")
        self.log_box.configure(state="disabled")
        self.log_box.see(ctk.END)

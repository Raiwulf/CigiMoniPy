import customtkinter as ctk
import webbrowser
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
        self.add_signature_label()
        self.tab2 = self.tabview.add("Log")
        self.log_box = ctk.CTkTextbox(self.tab2, state="disabled", height=10)
        self.log_box.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    def add_signature_label(self):
        def goURL():
            webbrowser.open_new("https://github.com/Raiwulf/CigiMoniPy")

        def on_label_enter(event):
            signature.configure(text_color="cyan")

        def on_label_leave(event):
            signature.configure(text_color="white")

        signature = ctk.CTkLabel(
            master=self.tab1, text="© 2024 CigiLabs", font=("Roboto", 16)
        )
        signature.bind("<Button-1>", lambda e: goURL())
        signature.place(relx=0.02, rely=1.0, anchor="sw")
        signature.bind("<Enter>", on_label_enter)
        signature.bind("<Leave>", on_label_leave)

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] : {message}"
        self.log_box.configure(state="normal")
        self.log_box.insert(ctk.END, message + "\n\n")
        self.log_box.configure(state="disabled")
        self.log_box.see(ctk.END)

import customtkinter as ctk
from datetime import datetime


class MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CigiMoniPy")
        self.geometry("400x300")

        # Create TabView
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1 for Main Monitor Controls
        self.tab1 = self.tabview.add("Main")
        self.loading_label = ctk.CTkLabel(self.tab1, text="Loading...")
        self.loading_label.pack(pady=20)

        # Tab 2 for Logs
        self.tab2 = self.tabview.add("Log")
        self.log_box = ctk.CTkTextbox(self.tab2, state="disabled", height=10)
        self.log_box.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    def log_event(self, message):
        """Creates a formatted log message with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] : {message}"

    def append_log(self, message):
        """Appends a log message to the log_box."""
        self.log_box.configure(state="normal")  # Enable editing to add text
        self.log_box.insert(ctk.END, message + "\n\n")
        self.log_box.configure(state="disabled")  # Make it read-only again
        self.log_box.see(ctk.END)  # Scroll to the end of the log box

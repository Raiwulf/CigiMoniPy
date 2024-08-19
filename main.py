import customtkinter as ctk
from monitorcontrol import get_monitors, InputSource


class MonitorCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        monitor,
        monitor_label,
        current_input_mode,
        available_inputs,
        switch_input_callback,
    ):
        super().__init__(parent)
        self.monitor = monitor
        self.label = ctk.CTkLabel(self, text=monitor_label)
        self.label.pack(side=ctk.LEFT, padx=10)
        self.input_mode_var = ctk.StringVar(value=current_input_mode)
        self.dropdown = ctk.CTkOptionMenu(
            self, variable=self.input_mode_var, values=available_inputs
        )
        self.dropdown.pack(side=ctk.LEFT, padx=10)
        self.dropdown.bind(
            "<<OptionMenuSelected>>",
            lambda event: switch_input_callback(
                self.monitor, self.input_mode_var.get()
            ),
        )
        self.pack(fill=ctk.X, pady=5)


class MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CigiMoniPy")
        self.geometry("400x200")
        self.loading_label = ctk.CTkLabel(self, text="Loading...")
        self.loading_label.pack(pady=20)
        self.after(100, self.load_monitors)

    def load_monitors(self):
        monitors = self.get_active_monitors()
        self.create_monitor_cards(monitors)
        self.remove_loading_label()

    def create_monitor_cards(self, monitors):
        for monitor, input_mode, available_inputs in monitors:
            monitor_label = self.get_monitor_name(monitor)
            MonitorCard(
                self,
                monitor,
                monitor_label,
                input_mode,
                available_inputs,
                self.switch_input_mode,
            )

    def remove_loading_label(self):
        self.loading_label.pack_forget()

    def get_active_monitors(self):
        monitors = []
        predefined_inputs = [source.name for source in InputSource]
        for monitor in get_monitors():
            with monitor:
                try:
                    current_input_source = monitor.get_input_source()
                    input_mode = current_input_source.name
                except AttributeError:
                    input_mode = "Unknown"
                available_inputs = predefined_inputs
                monitors.append((monitor, input_mode, available_inputs))
        return monitors

    def get_monitor_name(self, monitor):
        with monitor:
            capabilities = monitor.get_vcp_capabilities()
            monitor_name = capabilities.get("model", "Unknown Monitor")
        return monitor_name

    def switch_input_mode(self, monitor, new_input_mode):
        try:
            input_source = InputSource[new_input_mode]
        except KeyError:
            print(f"Invalid input source: {new_input_mode}")
            return
        with monitor:
            monitor.set_input_source(input_source)
        print(f"Switched to {new_input_mode}")


if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()

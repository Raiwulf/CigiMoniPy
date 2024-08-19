import tkinter as tk
from tkinter import ttk
from monitorcontrol import get_monitors, InputSource


class MonitorCard(tk.Frame):
    def __init__(
        self, parent, monitor, monitor_label, current_input_mode, switch_input_callback
    ):
        super().__init__(parent)
        self.monitor = monitor
        self.label = tk.Label(self, text=monitor_label)
        self.label.pack(side=tk.LEFT, padx=10)
        self.input_mode_var = tk.StringVar(value=current_input_mode)
        self.dropdown = ttk.Combobox(
            self, textvariable=self.input_mode_var, state="readonly"
        )
        self.dropdown["values"] = [
            "VGA1",
            "HDMI1",
            "HDMI2",
            "DP1",
            "DP2",
        ]
        self.dropdown.pack(side=tk.LEFT, padx=10)
        self.dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event: switch_input_callback(
                self.monitor, self.input_mode_var.get()
            ),
        )
        self.pack(fill=tk.X, pady=5)


class MonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor Input Manager")
        self.load_monitors()

    def load_monitors(self):
        monitors = self.get_active_monitors()
        for idx, (monitor, input_mode) in enumerate(monitors):
            monitor_label = f"Monitor {idx + 1}"
            MonitorCard(
                self, monitor, monitor_label, input_mode, self.switch_input_mode
            )

    def get_active_monitors(self):
        monitors = []
        for monitor in get_monitors():
            with monitor:
                current_input_source = monitor.get_input_source()
                input_mode = current_input_source.name
            monitors.append((monitor, input_mode))
        return monitors

    def switch_input_mode(self, monitor, new_input_mode):
        input_source = InputSource[new_input_mode]
        with monitor:
            monitor.set_input_source(input_source)
        print(f"Switched to {new_input_mode}")


if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()

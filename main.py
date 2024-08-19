import tkinter as tk
from tkinter import ttk
from monitorcontrol import get_monitors, InputSource


class MonitorCard(tk.Frame):
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

        # Use monitor_label to display monitor name
        self.label = tk.Label(self, text=monitor_label)
        self.label.pack(side=tk.LEFT, padx=10)

        # Dropdown list for selecting input mode
        self.input_mode_var = tk.StringVar(value=current_input_mode)
        self.dropdown = ttk.Combobox(
            self, textvariable=self.input_mode_var, state="readonly"
        )

        # Populate dropdown with available inputs
        self.dropdown["values"] = available_inputs
        self.dropdown.pack(side=tk.LEFT, padx=10)

        # Monitor input switch callback
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

        # Load monitors and create MonitorCard for each
        self.load_monitors()

    def load_monitors(self):
        monitors = self.get_active_monitors()
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

    def get_active_monitors(self):
        monitors = []
        for monitor in get_monitors():
            with monitor:
                # Get current input source
                current_input_source = monitor.get_input_source()
                input_mode = current_input_source.name

                # Define a list of possible input sources (you might need to adjust this based on your monitors)
                available_inputs = [source.name for source in InputSource]

            monitors.append((monitor, input_mode, available_inputs))
        return monitors

    def get_monitor_name(self, monitor):
        with monitor:
            capabilities = monitor.get_vcp_capabilities()

            # Debug: Print the raw capabilities dictionary to the console
            print(f"Raw VCP Capabilities: {capabilities}")

            # Extract model name from the capabilities dictionary
            monitor_name = capabilities.get("model", "Unknown Monitor")

            # Debug: Print the derived monitor name to the console
            print(f"Derived Monitor Name: {monitor_name}")

        return monitor_name

    def switch_input_mode(self, monitor, new_input_mode):
        # Convert the new_input_mode to InputSource
        try:
            input_source = InputSource[new_input_mode]
        except KeyError:
            print(f"Invalid input source: {new_input_mode}")
            return

        with monitor:
            # Set the new input source
            monitor.set_input_source(input_source)

        print(f"Switched to {new_input_mode}")


if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()

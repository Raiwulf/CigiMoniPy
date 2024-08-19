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
        adjust_brightness_callback,
    ):
        super().__init__(parent)
        self.monitor = monitor
        self.adjust_brightness_callback = adjust_brightness_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Monitor label
        self.label = ctk.CTkLabel(self, text=monitor_label)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Input mode dropdown
        self.input_mode_var = ctk.StringVar(value=current_input_mode)
        self.dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.input_mode_var,
            values=available_inputs,
            command=lambda new_mode: switch_input_callback(self.monitor, new_mode),
        )
        self.dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w", columnspan=2)

        # Brightness label
        self.brightness_label = ctk.CTkLabel(self, text="Brightness:")
        self.brightness_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Brightness entry
        self.brightness_entry = ctk.CTkEntry(self, width=50)
        self.brightness_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.brightness_entry.bind(
            "<KeyRelease>", lambda event: self.update_brightness_from_entry()
        )

        # Brightness slider
        self.brightness_slider = ctk.CTkSlider(self, from_=1, to=100)
        self.brightness_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.brightness_slider.bind(
            "<ButtonRelease-1>", lambda event: self.update_brightness_from_slider()
        )

        # Initialize the brightness slider value
        self.initialize_slider_value()

    def initialize_slider_value(self):
        try:
            with self.monitor:
                self.brightness_value = self.monitor.get_luminance()
        except AttributeError:
            self.brightness_value = 50
        self.brightness_slider.set(self.brightness_value)
        self.brightness_entry.delete(0, ctk.END)
        self.brightness_entry.insert(0, str(int(self.brightness_value)))

    def update_brightness_from_slider(self):
        self.brightness_value = self.brightness_slider.get()
        self.brightness_entry.delete(0, ctk.END)
        self.brightness_entry.insert(0, str(int(self.brightness_value)))
        self.update_brightness_value()

    def update_brightness_from_entry(self):
        try:
            new_value = int(self.brightness_entry.get())
            if 1 <= new_value <= 100:
                self.brightness_value = new_value
                self.brightness_slider.set(self.brightness_value)
                self.update_brightness_value()
            else:
                self.brightness_entry.delete(0, ctk.END)
                self.brightness_entry.insert(0, str(int(self.brightness_value)))
        except ValueError:
            self.brightness_entry.delete(0, ctk.END)
            self.brightness_entry.insert(0, str(int(self.brightness_value)))

    def update_brightness_value(self):
        try:
            if self.adjust_brightness_callback:
                self.adjust_brightness_callback(self.monitor, self.brightness_value)
        except Exception as e:
            print(f"Failed to adjust brightness: {e}")


class MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CigiMoniPy")
        self.geometry("400x300")

        # Create a Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Add tabs
        self.tab1 = self.tabview.add("Tab 1")
        self.tab2 = self.tabview.add("Tab 2")

        # Loading label in Tab 1
        self.loading_label = ctk.CTkLabel(self.tab1, text="Loading...")
        self.loading_label.pack(pady=20)

        # Simulate loading of monitors after a short delay
        self.after(100, self.load_monitors)

    def load_monitors(self):
        try:
            monitors = self.get_active_monitors()
            if monitors:
                self.create_monitor_cards(monitors)
            self.remove_loading_label()
        except Exception as e:
            print(f"Error loading monitors: {e}")

    def create_monitor_cards(self, monitors):
        for monitor, input_mode, available_inputs in monitors:
            monitor_label = self.get_monitor_name(monitor)
            MonitorCard(
                self.tab1,  # Pack MonitorCard in Tab 1
                monitor,
                monitor_label,
                input_mode,
                available_inputs,
                self.switch_input_mode,
                self.adjust_brightness,
            ).pack(fill=ctk.X, pady=5)

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
                monitors.append((monitor, input_mode, predefined_inputs))
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

    def adjust_brightness(self, monitor, brightness_value):
        try:
            with monitor:
                brightness_value = int(brightness_value)
                if 1 <= brightness_value <= 100:
                    monitor.set_luminance(brightness_value)
                    print(f"Brightness set to {brightness_value}")
                else:
                    print(f"Brightness value {brightness_value} is out of range.")
        except Exception as e:
            print(f"Failed to adjust brightness: {e}")


if __name__ == "__main__":
    app = MonitorApp()
    app.mainloop()

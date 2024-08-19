import customtkinter as ctk


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
        self.label = ctk.CTkLabel(self, text=monitor_label)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.input_mode_var = ctk.StringVar(value=current_input_mode)
        self.dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.input_mode_var,
            values=available_inputs,
            command=lambda new_mode: switch_input_callback(self.monitor, new_mode),
        )
        self.dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w", columnspan=2)
        self.brightness_label = ctk.CTkLabel(self, text="Brightness:")
        self.brightness_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.brightness_entry = ctk.CTkEntry(self, width=50)
        self.brightness_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.brightness_entry.bind(
            "<KeyRelease>", lambda event: self.update_brightness_from_entry()
        )
        self.brightness_slider = ctk.CTkSlider(self, from_=1, to=100)
        self.brightness_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.brightness_slider.bind(
            "<ButtonRelease-1>", lambda event: self.update_brightness_from_slider()
        )
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
        if self.adjust_brightness_callback:
            self.adjust_brightness_callback(self.monitor, self.brightness_value)

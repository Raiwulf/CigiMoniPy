from monitorcontrol import get_monitors, InputSource
from gui import MonitorApp
from monitor_card import MonitorCard
import customtkinter as ctk


def load_monitors(app):
    try:
        monitors = get_active_monitors()
        if monitors:
            create_monitor_cards(app, monitors)
        remove_loading_label(app)
    except Exception as e:
        app.append_log(app.log_event(f"Error loading monitors: {e}"))


def create_monitor_cards(app, monitors):
    for monitor, input_mode, available_inputs in monitors:
        monitor_label = get_monitor_name(monitor)
        MonitorCard(
            app.tab1,
            monitor,
            monitor_label,
            input_mode,
            available_inputs,
            switch_input_mode,
            adjust_brightness,
        ).pack(fill=ctk.X, pady=5)
    app.append_log(app.log_event("Monitor cards created successfully."))


def remove_loading_label(app):
    app.loading_label.pack_forget()


def get_active_monitors():
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


def get_monitor_name(monitor):
    with monitor:
        capabilities = monitor.get_vcp_capabilities()
        monitor_name = capabilities.get("model", "Unknown Monitor")
    return monitor_name


def switch_input_mode(monitor, new_input_mode):
    try:
        input_source = InputSource[new_input_mode]
    except KeyError:
        app.append_log(app.log_event(f"Invalid input source: {new_input_mode}"))
        return
    with monitor:
        monitor.set_input_source(input_source)
    app.append_log(app.log_event(f"Switched to {new_input_mode}"))


def adjust_brightness(monitor, brightness_value):
    try:
        with monitor:
            brightness_value = int(brightness_value)
            if 1 <= brightness_value <= 100:
                monitor.set_luminance(brightness_value)
                app.append_log(app.log_event(f"Brightness set to {brightness_value}"))
            else:
                app.append_log(
                    app.log_event(
                        f"Brightness value {brightness_value} is out of range."
                    )
                )
    except Exception as e:
        app.append_log(app.log_event(f"Failed to adjust brightness: {e}"))


if __name__ == "__main__":
    app = MonitorApp()
    app.after(100, lambda: load_monitors(app))
    app.mainloop()

# CigiMoniPy

CigiMoniPy is a GUI application for managing monitor settings, including input source selection and brightness adjustment. It utilizes `customtkinter` for the user interface and `monitorcontrol` for interacting with the monitors.

![image](https://github.com/user-attachments/assets/b4f19ce8-f497-4779-885b-fa5d41af0f55)


## Installation

### Prerequisites

1. **Python**: Ensure Python 3.6 or higher is installed on your system.

2. **Install Dependencies**: Install the required Python packages using `pip`. Open a terminal and run the following commands:

   ```bash
   pip install customtkinter monitorcontrol
   ```

   This will install `customtkinter` for the graphical interface and `monitorcontrol` for monitor management.

## Usage

### Running the Application

1. **Save the Code**: Save the provided Python script to a file named `monitor_app.py`.

2. **Run the Application**: Open a terminal, navigate to the directory where you saved `monitor_app.py`, and run the script using Python:

   ```bash
   python monitor_app.py
   ```

3. **Using the Application**:
   - The application window will display a list of connected monitors.
   - Each monitor card shows the monitor label, current input mode, and brightness settings.
   - **Change Input Mode**: Use the dropdown menu to select a new input mode for the monitor.
   - **Adjust Brightness**:
     - **Slider**: Move the slider to adjust the brightness.
     - **Entry Field**: Type a value in the entry field to set the brightness. The value must be between 1 and 100.

### Key Functions

- **`get_active_monitors`**: Retrieves a list of active monitors and their current input sources.
- **`get_monitor_name`**: Fetches the model name of the monitor using its VCP capabilities.
- **`switch_input_mode`**: Changes the input source of the monitor.
- **`adjust_brightness`**: Sets the brightness level of the monitor.

## Troubleshooting

- **Monitor Detection Issues**: Ensure that all monitors are properly connected and detected by your operating system. The application relies on the `monitorcontrol` library to interface with the monitors.

- **Missing Dependencies**: Verify that all required Python packages are installed. Use `pip list` to check if `customtkinter` and `monitorcontrol` are listed.

- **Errors**: If you encounter any errors while running the application, check the terminal output for detailed error messages. Ensure your Python environment is properly set up and the necessary permissions are granted for monitor control.

## Contributing

If you would like to contribute to the development of CigiMoniPy, feel free to fork the repository, make improvements, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

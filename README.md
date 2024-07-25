# Strain Gauge Data Acquisition Application

Welcome to the Strain Gauge Data Acquisition Application repository. This application is designed to facilitate the acquisition and visualization of data from four strain gauges. It offers real-time data visualization, calibration, and data export functionalities.

## Features

- **Real-Time Data Visualization**: View data from four strain gauges in real-time.
- **Measurement Control**: Start, stop, and reset measurements.
- **Calibration**: Calibrate the strain gauges to ensure accurate measurements.
- **Data Export**: Export the acquired data to a CSV file for further analysis.

## Requirements

Before running the application, ensure you have the following libraries installed:

- `matplotlib`
- `xlsxwriter`
- `pyserial`
- `pillow`

You can install these libraries using pip:

```bash
pip install matplotlib xlsxwriter pyserial pillow
```
## Installation

1. **Clone the Repository**: Clone this repository to your local machine using the following command:

    ```bash
    git clone https://github.com/saviodp7/StrainGaugeApp.git
    ```

2. **Run the Application**: Start the application with the following command:

    ```bash
    python main.py
    ```

## Usage

### Real-Time Data Visualization

The application allows you to view data from the strain gauges in real-time. Simply start the application and initiate data acquisition to see live updates.

### Measurement Control

- **Start Measurement**: Click the 'Start' button to begin data acquisition.
- **Stop Measurement**: Click the 'Stop' button to halt data acquisition.
- **Reset Measurement**: Click the 'Reset' button to clear the current data and reset the gauges.

### Calibration

To ensure accurate readings, calibrate the strain gauges using the calibration button provided in the application.

### Data Export

Export the acquired data to a CSV file for further analysis. Click the 'Export' button and the file will be created in the current directory.

For any questions or feedback, please open an issue in the repository or contact me at [saviodp7@gmail.com](mailto:saviodp7@gmail.com).

# Energy Consumption Reporting Tool

## Overview

This project is a Python-based tool designed to generate a report on energy consumption using data from a Home Assistant instance. The tool connects to the Home Assistant API via WebSocket, retrieves energy consumption data for a specified period, and calculates potential discounts based on predefined energy plans. The output includes a detailed report of energy usage, discounts applicable, and the total cost after applying the best discount.

## Features

- **Connects to Home Assistant:** Uses WebSocket API to authenticate and retrieve energy consumption data.
- **Customizable Energy Plans:** Allows defining multiple energy plans with specific discount rates based on hours and days.
- **Time Period Selection:** Generates reports for a specific month and year or for the current month by default.
- **ASCII Bar Chart:** Visualizes hourly energy consumption with an ASCII-based bar chart.
- **Cost Calculation:** Calculates the total energy cost before and after applying the best discount from the available energy plans.

## Requirements

- Python 3.10+
- `websockets` library
- `dotenv` library

You can install the required libraries using pip:

```bash
pip install websockets python-dotenv
```

## Environment Variables

The tool requires several environment variables to function correctly. These variables should be stored in a `.env` file in the project root:

- **HA_URL:** URL of your Home Assistant instance (e.g., `ws://homeassistant.local:8123`).
- **HA_ACCESS_TOKEN:** Access token for authenticating with Home Assistant.
- **HA_SENSOR_IDS:** Comma-separated list of sensor IDs to retrieve energy data from.
- **UNIVERSAL_TARIFF:** The base tariff rate for energy consumption (in NIS per kWh). Default is `0.61`.
- **ENERGY_PLAN_X:** Energy plans in the format `PlanName|Hours|Days|Discount`. Replace `X` with an integer starting from 1 for each plan.

### Example `.env` file:

```env
HA_URL=ws://homeassistant.local:8123
HA_ACCESS_TOKEN=your_long_lived_access_token
HA_SENSOR_IDS=sensor.shellyem3_x_channel_a_energy,sensor.shellyem3_x_channel_b_energy,sensor.shellyem3_x_channel_c_energy
HA_DAYS=7
UNIVERSAL_TARIFF=0.61
ENERGY_PLAN_1=Cellcom Flat|0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.05
ENERGY_PLAN_2=Cellcom Day|7,8,9,10,11,12,13,14,15,16|Sunday,Monday,Tuesday,Wednesday,Thursday|0.15
ENERGY_PLAN_3=Cellcom Family|14,15,16,17,18,19|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.18
ENERGY_PLAN_4=Cellcom Night|23,0,1,2,3,4,5,6|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.18
```

## Usage

The tool can be run from the command line. It accepts two optional arguments for specifying the month and year for the report:

- **--month:** Month for which to generate the report (1-12). If not specified, the current month is used.
- **--year:** Year for which to generate the report. If not specified, the current year is used.

### Example usage:

```bash
python energy_report.py --month 7 --year 2023
```

This command will generate a report for July 2023.

## Output

The output is logged to the console and includes:

1. Hourly energy consumption as an ASCII bar chart.
2. Total energy consumption (in kWh).
3. Discount calculations for each defined energy plan.
4. Best discount applied and the total cost after the discount.

## Error Handling

The tool includes basic error handling for scenarios such as missing environment variables, failed API requests, and data parsing errors. Errors are logged to the console.

## Logging

The tool uses Python's `logging` module to log information and errors. The logging level is set to `INFO` by default, meaning all informational messages and errors will be displayed.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! If you have ideas for improving this tool or find a bug, feel free to open an issue or submit a pull request.

---

This README provides a detailed guide on setting up and using the energy consumption reporting tool. Ensure that your environment is configured correctly, and feel free to customize the energy plans according to your needs.

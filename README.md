# Home Energy Reporter

## Overview

**Home Energy Reporter** is a tool designed to help you better understand and optimize your energy consumption patterns using data from your Home Assistant setup. By analyzing your energy usage across different times of the day and days of the week, the tool identifies opportunities for savings based on predefined energy plans. It provides insights into your consumption behavior, helping you make informed decisions to reduce costs and improve energy efficiency.

## Features

- **Connects to Home Assistant:** Uses WebSocket API to authenticate and retrieve energy consumption data.
- **Customizable Energy Plans:** Allows defining multiple energy plans with specific discount rates based on hours and days.
- **Time Period Selection:** Generates reports for a specific month and year or for the current month by default.
- **Cost Calculation:** Calculates the total energy cost before and after applying the best discount from the available energy plans.


## Output Example

```
Energy consumption from 2024-07-01 to 2024-07-31
Number of days: 31

Hourly consumption (kWh):
Hour |   kWh | Chart
-------------------------------------------------------------
00:00 | 53.71 | ███████████████████████████
01:00 | 49.94 | █████████████████████████
02:00 | 48.34 | ████████████████████████
03:00 | 45.20 | ███████████████████████
04:00 | 44.05 | ██████████████████████
05:00 | 42.97 | ██████████████████████
06:00 | 38.31 | ███████████████████
07:00 | 43.15 | ██████████████████████
08:00 | 46.57 | ███████████████████████
09:00 | 60.06 | ██████████████████████████████
10:00 | 79.73 | ████████████████████████████████████████
11:00 | 78.90 | ████████████████████████████████████████
12:00 | 79.20 | ████████████████████████████████████████
13:00 | 86.95 | ████████████████████████████████████████████
14:00 | 97.41 | ██████████████████████████████████████████████████
15:00 | 92.21 | ███████████████████████████████████████████████
16:00 | 91.63 | ███████████████████████████████████████████████
17:00 | 73.41 | █████████████████████████████████████
18:00 | 65.35 | █████████████████████████████████
19:00 | 60.91 | ███████████████████████████████
20:00 | 67.34 | ██████████████████████████████████
21:00 | 70.01 | ███████████████████████████████████
22:00 | 69.08 | ███████████████████████████████████
23:00 | 64.42 | █████████████████████████████████

Total energy consumption: 1548.856 kWh

Discount per plan (NIS):
Cellcom Flat: 47.24
Cellcom Day: 55.46 (Best)
Cellcom Family: 52.81
Cellcom Night: 42.49

Total cost before discount: 944.80 NIS
Best discount applied: 55.46 NIS
Total cost after best discount: 889.34 NIS
```

## Usage

### Step 1: Clone the Repository

First, clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/YogevKr/home-energy-reporter.git
```

### Step 2: Navigate to the Project Directory

Move into the project directory:

```bash
cd home-energy-reporter
```

### Step 3: Set Up the Environment Variables

Create a `.env` file in the project root and add the required environment variables (as shown above).

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
UNIVERSAL_TARIFF=0.61
ENERGY_PLAN_1=Cellcom Flat|0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.05
ENERGY_PLAN_2=Cellcom Day|7,8,9,10,11,12,13,14,15,16|Sunday,Monday,Tuesday,Wednesday,Thursday|0.15
ENERGY_PLAN_3=Cellcom Family|14,15,16,17,18,19|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.18
ENERGY_PLAN_4=Cellcom Night|23,0,1,2,3,4,5,6|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|0.18
```

### Step 4: Install Required Dependencies

Make sure you have Python 3.10+ installed. Then, install the required Python libraries:

```bash
pip install websockets python-dotenv
```

### Step 5: Run the Report

You can now run the tool to generate a report. The report can be run for the current month or for a specific month and year:

- **To generate a report for the current month:**

  ```bash
  python energy_report.py
  ```

- **To generate a report for a specific month and year:**

  ```bash
  python energy_report.py --month 7 --year 2023
  ```

### Step 6: Review the Output

The tool will output a detailed report in your terminal, including:

1. Hourly energy consumption as an ASCII bar chart.
2. Total energy consumption (in kWh).
3. Discount calculations for each defined energy plan.
4. Best discount applied and the total cost after the discount.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! If you have ideas for improving this tool or find a bug, feel free to open an issue or submit a pull request.

---

This README provides a comprehensive guide on setting up and using **Home Energy Reporter** to analyze and optimize your home energy consumption. Make sure your environment is configured correctly, and feel free to customize the energy plans according to your needs.

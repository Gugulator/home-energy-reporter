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
Energy consumption from 2024-09-01 to 2024-09-30
Number of days: 30

Hourly consumption (kWh):
Hour |   kWh | Chart
-------------------------------------------------------------
00:00 | 40.33 | ██████████████████████████████████████████████████
01:00 | 38.40 | ███████████████████████████████████████████████
02:00 | 35.19 | ███████████████████████████████████████████
03:00 | 33.79 | █████████████████████████████████████████
04:00 | 29.50 | ████████████████████████████████████
05:00 | 27.38 | █████████████████████████████████
06:00 | 28.45 | ███████████████████████████████████
07:00 | 26.52 | ████████████████████████████████
08:00 | 25.87 | ████████████████████████████████
09:00 | 24.56 | ██████████████████████████████
10:00 | 25.03 | ███████████████████████████████
11:00 | 23.66 | █████████████████████████████
12:00 | 22.44 | ███████████████████████████
13:00 | 24.26 | ██████████████████████████████
14:00 | 26.21 | ████████████████████████████████
15:00 | 22.97 | ████████████████████████████
16:00 | 24.36 | ██████████████████████████████
17:00 | 28.33 | ███████████████████████████████████
18:00 | 32.27 | ████████████████████████████████████████
19:00 | 32.60 | ████████████████████████████████████████
20:00 | 30.07 | █████████████████████████████████████
21:00 | 30.46 | █████████████████████████████████████
22:00 | 31.81 | ███████████████████████████████████████
23:00 | 38.53 | ███████████████████████████████████████████████

Total energy consumption: 702.990 kWh

Top 3 Best Discounts (NIS):
HOT e-Triple: 43.20
PazGas Yellow Wallet: 43.20
Electra Night: 36.64

Other Discounts (NIS):
Electra Hi-Tech Year 3+: 33.54
Cellcom Night: 33.38
Electra Power Year 3+: 30.24
HOT Save 24/7 Year 3+: 30.24
HOT Save Constant HOT: 30.24
AmIsraGas Constant Savings (AmIsraGas Customers): 30.24
Bezeq Smart Savings 24/7: 30.24
PazGas Discount 24/7: 30.24
Partner Constant Discount Year 3+: 30.24
Electra Hi-Tech Year 2: 30.18
AmIsraGas Constant Savings: 28.08
Electra Hi-Tech Year 1: 26.83
HOT Save at Night: 26.03
Bezeq Smart Savings Night: 26.03
Partner Night Owls: 26.03
Electra Power Year 2: 25.92
HOT Save Constant NEXT: 25.92
HOT Save 24/7 Year 2: 25.92
Partner Constant Discount Year 2: 25.92
Cellcom Flat: 21.60
Electra Power Year 1: 21.60
HOT Save 24/7 Year 1: 21.60
Partner Constant Discount Year 1: 21.60
Cellcom Family: 18.44
HOT Save at Day: 16.82
Bezeq Smart Savings Day: 16.82
Partner Work from Home: 16.82
Cellcom Day: 15.20
Total cost before discount: 431.99 NIS
Best discount applied: 43.20 NIS
Total cost after best discount: 388.79 NIS
```
# Usage

### Step 1: Clone the Repository

First, clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/Gugulator/home-energy-reporter.git
```

### Step 2: Navigate to the Project Directory

Move into the project directory:

```bash
cd home-energy-reporter
```

### Step 3: Set Up the Environment Variables

Create a `.env` file in the project root and add the required environment variables.

```bash
mv .env.example .env
```

## Environment Variables

The tool requires several environment variables to function correctly. These variables should be stored in a `.env` file in the project root:

- **SSL_VERIFY:** False - if not need to check SSL certificate, True - to enable check
- **HA_URL:** URL of your Home Assistant instance (e.g., `ws://homeassistant.local:8123`). Type `wss` if using self signed certificate.
- **HA_ACCESS_TOKEN:** Access token for authenticating with Home Assistant.
- **HA_SENSOR_IDS:** Comma-separated list of sensor IDs to retrieve energy data from.
- **UNIVERSAL_TARIFF:** The base tariff rate for energy consumption (in NIS per kWh). Default is `0.61`.
- **ENERGY_PLAN_X:** Energy plans in the format `PlanName|Hours|Days|Discount`. Replace `X` with an integer starting from 1 for each plan.

### Example `.env` file:

```env
SSL_VERIFY=False
HA_URL=ws://homeassistant.local:8123
HA_ACCESS_TOKEN=your_long_lived_access_token
HA_SENSOR_IDS=sensor.shellyem3_x_channel_a_energy,sensor.shellyem3_x_channel_b_energy,sensor.shellyem3_x_channel_c_energy

UNIVERSAL_TARIFF=0.6145

ENERGY_PLAN_1=Cellcom Flat|0-23|Sunday-Saturday|0.05
ENERGY_PLAN_2=Cellcom Day|7-16|Sunday-Thursday|0.15
ENERGY_PLAN_3=Cellcom Family|14-19|Sunday-Saturday|0.18
ENERGY_PLAN_4=Cellcom Night|23,0-6|Sunday-Saturday|0.20

# Electra Power - Hi-Tech plan
# 23:00 - 17:00, discount depends on the subscription year
ENERGY_PLAN_5=Electra Hi-Tech Year 1|23,0-17|Sunday-Saturday|0.08
ENERGY_PLAN_6=Electra Hi-Tech Year 2|23,0-17|Sunday-Saturday|0.09
ENERGY_PLAN_7=Electra Hi-Tech Year 3+|23,0-17|Sunday-Saturday|0.10

# Electra Power - POWER plan
# 24/7, discount depends on the subscription year
ENERGY_PLAN_8=Electra Power Year 1|0-23|Sunday-Saturday|0.05
ENERGY_PLAN_9=Electra Power Year 2|0-23|Sunday-Saturday|0.06
ENERGY_PLAN_10=Electra Power Year 3+|0-23|Sunday-Saturday|0.07

# Electra Power - Night plan
# 23:00 - 07:00, fixed 20% discount
ENERGY_PLAN_11=Electra Night|23,0-7|Sunday-Saturday|0.20

# HOT Energy - Save Constant NEXT plan
# For NEXT Double customers only, 24/7 coverage
# Fixed 6% discount
ENERGY_PLAN_12=HOT Save Constant NEXT|0-23|Sunday-Saturday|0.06

# HOT Energy - e-Triple plan
# Discount for HOT Triple and HOT Mobile customers only
# Applies 24/7, fixed 10% discount
ENERGY_PLAN_13=HOT e-Triple|0-23|Sunday-Saturday|0.10

# HOT Energy - Save at Night plan
# Applies from 23:00 to 07:00, Sunday-Thursday
# Fixed 20% discount during nighttime
ENERGY_PLAN_14=HOT Save at Night|23,0-7|Sunday-Thursday|0.20

# HOT Energy - Save 24/7 plan
# 24/7, discount depends on the subscription year
ENERGY_PLAN_15=HOT Save 24/7 Year 1|0-23|Sunday-Saturday|0.05
ENERGY_PLAN_16=HOT Save 24/7 Year 2|0-23|Sunday-Saturday|0.06
ENERGY_PLAN_17=HOT Save 24/7 Year 3+|0-23|Sunday-Saturday|0.07

# HOT Energy - Save at Day plan
# Applies from 07:00 to 17:00, Sunday-Thursday
# Fixed 15% discount during daytime
ENERGY_PLAN_18=HOT Save at Day|7-17|Sunday-Thursday|0.15

# HOT Energy - Save Constant HOT plan
# For HOT Triple customers only, applies 24/7
# Fixed 7% discount
ENERGY_PLAN_19=HOT Save Constant HOT|0-23|Sunday-Saturday|0.07

# AmIsraGas - Constant Savings plan
# Fixed 6.5% discount, applies 24/7
ENERGY_PLAN_20=AmIsraGas Constant Savings|0-23|Sunday-Saturday|0.065

# AmIsraGas - Constant Savings for AmIsraGas Customers plan
# Fixed 7% discount for AmIsraGas customers, applies 24/7
ENERGY_PLAN_21=AmIsraGas Constant Savings (AmIsraGas Customers)|0-23|Sunday-Saturday|0.07

# Bezeq Energy - Smart Savings 24/7 plan
# Fixed 7% discount, applies 24/7
ENERGY_PLAN_22=Bezeq Smart Savings 24/7|0-23|Sunday-Saturday|0.07

# Bezeq Energy - Smart Savings at Night plan
# Fixed 20% discount during nighttime from 23:00 to 07:00, Sunday-Thursday
ENERGY_PLAN_23=Bezeq Smart Savings Night|23,0-7|Sunday-Thursday|0.20

# Bezeq Energy - Smart Savings at Day plan
# Fixed 15% discount during daytime from 07:00 to 17:00, Sunday-Thursday
ENERGY_PLAN_24=Bezeq Smart Savings Day|7-17|Sunday-Thursday|0.15

# PazGas - Discount 24/7 plan
# Fixed 7% discount, applies 24/7
ENERGY_PLAN_25=PazGas Discount 24/7|0-23|Sunday-Saturday|0.07

# PazGas - Accumulation to Yellow Wallet plan
# 10% of the payment accumulates to the Yellow Wallet app, applies 24/7
# Maximum accumulation: 50 NIS per month and 600 NIS per year
ENERGY_PLAN_26=PazGas Yellow Wallet|0-23|Sunday-Saturday|0.10

# Partner Power - Constant Discount All Day plan
# Discount depends on the subscription year, applies 24/7
ENERGY_PLAN_27=Partner Constant Discount Year 1|0-23|Sunday-Saturday|0.05
ENERGY_PLAN_28=Partner Constant Discount Year 2|0-23|Sunday-Saturday|0.06
ENERGY_PLAN_29=Partner Constant Discount Year 3+|0-23|Sunday-Saturday|0.07

# Partner Power - Night Owls plan
# Fixed 20% discount during nighttime from 23:00 to 07:00, Sunday-Thursday
ENERGY_PLAN_30=Partner Night Owls|23,0-7|Sunday-Thursday|0.20

# Partner Power - Work from Home plan
# Fixed 15% discount during daytime from 07:00 to 17:00, Sunday-Thursday
ENERGY_PLAN_31=Partner Work from Home|7-17|Sunday-Thursday|0.15

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
4. Best discount applied and the total cost after the discount in descending order.
5. At the beginning it displays 3 best discounts.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! If you have ideas for improving this tool or find a bug, feel free to open an issue or submit a pull request.

---

This README provides a comprehensive guide on setting up and using **Home Energy Reporter** to analyze and optimize your home energy consumption. Make sure your environment is configured correctly, and feel free to customize the energy plans according to your needs.

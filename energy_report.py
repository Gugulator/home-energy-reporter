import asyncio
import json
import websockets
import datetime
import logging
import os
import argparse
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class EnergyPlan:
    def __init__(self, name, hours, days, discount):
        self.name = name
        self.hours = hours
        self.days = days
        self.discount = discount

class HomeAssistantClient:
    def __init__(self, url, access_token, sensor_ids):
        self.url = url
        self.access_token = access_token
        self.sensor_ids = sensor_ids
        self.message_id = 1

    async def connect(self):
        try:
            self.websocket = await websockets.connect(f"{self.url}/api/websocket")
            await self.authenticate()
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            raise

    async def authenticate(self):
        auth_required = await self.websocket.recv()
        auth_required_data = json.loads(auth_required)
        
        if auth_required_data["type"] != "auth_required":
            raise Exception("Unexpected first message")

        auth_message = {
            "type": "auth",
            "access_token": self.access_token
        }
        await self.websocket.send(json.dumps(auth_message))
        
        auth_ok = await self.websocket.recv()
        auth_ok_data = json.loads(auth_ok)
        
        if auth_ok_data["type"] != "auth_ok":
            error_msg = auth_ok_data.get("message", "Unknown error")
            raise Exception(f"Authentication failed: {error_msg}")

    async def get_energy_data(self, start_time, end_time):
        message = {
            "id": self.message_id,
            "type": "recorder/statistics_during_period",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "statistic_ids": self.sensor_ids,
            "period": "hour",
            "types": ["change"],
            "units": {"energy": "kWh"}
        }
        
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        data = json.loads(response)
        
        if not data.get("success", False):
            error_msg = data.get("error", {}).get("message", "Unknown error")
            raise Exception(f"API request failed: {error_msg}")
        
        return data["result"]

    async def close(self):
        if hasattr(self, 'websocket'):
            await self.websocket.close()

def parse_timestamp(timestamp):
    if isinstance(timestamp, int):
        return datetime.datetime.fromtimestamp(timestamp / 1000)
    elif isinstance(timestamp, str):
        return datetime.datetime.fromisoformat(timestamp.rstrip('Z'))
    else:
        raise ValueError(f"Unexpected timestamp format: {timestamp}")

def calculate_discount(consumption, plans, universal_tariff):
    discounts = {}
    for plan in plans:
        plan_discount = 0
        for day, hourly_consumption in consumption.items():
            if day in plan.days:
                for hour, amount in hourly_consumption.items():
                    if hour in plan.hours:
                        plan_discount += amount * universal_tariff * plan.discount
        discounts[plan.name] = plan_discount
    return discounts

def parse_plan(plan_str):
    name, hours, days, discount = plan_str.split('|')
    hours = parse_hour_range(hours)
    days = parse_day_range(days)
    discount = float(discount)
    return EnergyPlan(name, hours, days, discount)

def parse_day_range(day_str):
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    days = []
    for part in day_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            start_index = days_of_week.index(start)
            end_index = days_of_week.index(end)
            if start_index <= end_index:
                days.extend(days_of_week[start_index:end_index+1])
            else:
                days.extend(days_of_week[start_index:] + days_of_week[:end_index+1])
        else:
            days.append(part)
    return days

def parse_hour_range(hour_str):
    hours = []
    for part in hour_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            hours.extend(range(start, end + 1))
        else:
            hours.append(int(part))
    return hours

def plot_ascii_bar_chart(data, max_width=50):
    max_value = max(data.values())
    scale = max_width / max_value if max_value > 0 else 1

    logger.info("")
    logger.info("Hourly consumption (kWh):")
    logger.info("Hour |   kWh | Chart")
    logger.info("-" * (11 + max_width))

    for hour in range(24):
        value = data[hour]
        bar_width = int(value * scale)
        bar = '█' * bar_width
        logger.info(f"{hour:02d}:00 | {value:5.2f} | {bar}")

async def main(month=None, year=None):
    ha_url = os.getenv('HA_URL')
    access_token = os.getenv('HA_ACCESS_TOKEN')
    sensor_ids = os.getenv('HA_SENSOR_IDS').split(',')
    universal_tariff = float(os.getenv('UNIVERSAL_TARIFF', '0.15'))  # Default to 0.15 NIS per kWh if not specified

    if not all([ha_url, access_token, sensor_ids]):
        logger.error("Missing required environment variables. Please check your .env file.")
        return

    # Parse energy plans from environment variables
    plans = []
    plan_index = 1
    while True:
        plan_str = os.getenv(f'ENERGY_PLAN_{plan_index}')
        if not plan_str:
            break
        plans.append(parse_plan(plan_str))
        plan_index += 1

    if not plans:
        logger.error("No energy plans defined. Please check your .env file.")
        return

    client = HomeAssistantClient(
        url=ha_url,
        access_token=access_token,
        sensor_ids=sensor_ids
    )
    
    try:
        await client.connect()
        
        # Determine start and end dates based on input
        now = datetime.datetime.now()
        if month is None:
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        else:
            year = year or now.year
            start_date = datetime.datetime(year, month, 1)
            if month == 12:
                end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(seconds=1)
            else:
                end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(seconds=1)
        
        energy_data = await client.get_energy_data(start_date, end_date)
        
        weekly_hourly_totals = defaultdict(float)
        consumption_by_day_hour = defaultdict(lambda: defaultdict(float))
        
        for sensor_id, sensor_data in energy_data.items():
            for entry in sensor_data:
                try:
                    timestamp = parse_timestamp(entry['start'])
                    day_of_week = timestamp.strftime('%A')
                    hour = timestamp.hour
                    consumption = entry['change']
                    
                    weekly_hourly_totals[hour] += consumption
                    consumption_by_day_hour[day_of_week][hour] += consumption
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing entry: {entry}. Error: {str(e)}")

        # Generate report
        logger.info(f"Energy consumption from {start_date.date()} to {end_date.date()}")
        logger.info(f"Number of days: {(end_date.date() - start_date.date()).days + 1}")
        
        plot_ascii_bar_chart(weekly_hourly_totals)

        total_consumption = sum(weekly_hourly_totals.values())
        logger.info(f"\nTotal energy consumption: {total_consumption:.3f} kWh")

        discounts = calculate_discount(consumption_by_day_hour, plans, universal_tariff)
        logger.info("\nDiscount per plan (NIS):")
        best_discount = max(discounts.items(), key=lambda x: x[1])
        for plan_name, discount in discounts.items():
            if plan_name == best_discount[0]:
                logger.info(f"{plan_name}: {discount:.2f} (Best)")
            else:
                logger.info(f"{plan_name}: {discount:.2f}")

        best_discount_amount = best_discount[1]
        total_cost = total_consumption * universal_tariff - best_discount_amount
        
        logger.info(f"Total cost before discount: {total_consumption * universal_tariff:.2f} NIS")
        logger.info(f"Best discount applied: {best_discount_amount:.2f} NIS")
        logger.info(f"Total cost after best discount: {total_cost:.2f} NIS")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        await client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate energy consumption report.")
    parser.add_argument("--month", type=int, choices=range(1, 13), help="Month (1-12)")
    parser.add_argument("--year", type=int, help="Year (e.g., 2023)")
    args = parser.parse_args()

    asyncio.run(main(args.month, args.year))

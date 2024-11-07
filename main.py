#!venv/bin/python3 -u
from winix.auth import login
from winix.driver import WinixAccount, WinixDevice
from prometheus_client import start_http_server, Gauge
import os
import sys
from datetime import datetime
import time

ERROR_PARSING_VALUE = 999

# metrics that we know exist
# on / off
power_metric = Gauge(
    "winix_c545_power",
    "power state on the winix c545. 0 is off, 1 is on. 999 is error parsing",
    ["id", "mac", "alias", "location_code"],
)

power_table = {
    "off": 0,
    "on": 1,
}

# auto / manual
mode_metric = Gauge(
    "winix_c545_fan_mode",
    "fan mode on the winix c545. 0 is manual, 1 is auto. 999 is error parsing",
    ["id", "mac", "alias", "location_code"],
)

mode_table = {
    "manual": 0,
    "auto": 1,
}

# low / medium/ high / turbo
airflow_metric = Gauge(
    "winix_c545_airflow",
    "fan airflow mode on the winix c545. 0=sleep,1=low,2=medium,3=high,4=turbo,999=error parsing",
    ["id", "mac", "alias", "location_code"],
)

airflow_table = {
    "sleep": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "turbo": 4,
}

aqi_metric = Gauge(
    "winix_c545_aqi",
    "aqi reading on the winix c545.",
    ["id", "mac", "alias", "location_code"],
)

# on / off
plasmawave_metric = Gauge(
    "winix_c545_plasma",
    "plasmawave state on the winix c545. 0 is off, 1 is on, 999 is error parsing",
    ["id", "mac", "alias", "location_code"],
)

plasmawave_table = {
    "off": 0,
    "on": 1,
}

filter_hour_metric = Gauge(
    "winix_c545_filter_hour",
    "filter hour on the winix c545.",
    ["id", "mac", "alias", "location_code"],
)

# good / fair / poor
air_quality_metric = Gauge(
    "winix_c545_air_quality",
    "air quality on the winix c545. 1=good,0=fair,-1=poor,999=error parsing",
    ["id", "mac", "alias", "location_code"],
)

air_quality_table = {"good": 1, "fair": 0, "poor": -1}

air_qvalue_metric = Gauge(
    "winix_c545_air_qvalue",
    "air qvalue on the winix c545.",
    ["id", "mac", "alias", "location_code"],
)
ambient_light_metric = Gauge(
    "winix_c545_ambient_light",
    "ambient light on the winix c545.",
    ["id", "mac", "alias", "location_code"],
)

if __name__ == "__main__":
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    metrics_port = int(os.getenv("METRICS_PORT", 8000))
    interval = int(os.getenv("INTERVAL", 60))

    # Check that required environment variables are set
    if not username:
        sys.exit("Error: USERNAME environment variable is required.")
    if not password:
        sys.exit("Error: PASSWORD environment variable is required.")

    start_http_server(metrics_port)
    cognito = login(username, password)
    account = WinixAccount(cognito.access_token)
    account.register_user(username)
    account.check_access_token()
    devices = account.get_device_info_list()

    while True:
        print(f"Starting winix api scrape...")
        for device in devices:
            print(device)
            fulldevice = WinixDevice(device.id)
            state = fulldevice.get_state()
            # set the values from state onto the metrics
            power_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(
                power_table.get(
                    state.get("power", ERROR_PARSING_VALUE), ERROR_PARSING_VALUE
                )
            )
            mode_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(
                mode_table.get(
                    state.get("mode", ERROR_PARSING_VALUE), ERROR_PARSING_VALUE
                )
            )
            airflow_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(
                airflow_table.get(
                    state.get("airflow", ERROR_PARSING_VALUE), ERROR_PARSING_VALUE
                )
            )
            aqi_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(state.get("aqi"), ERROR_PARSING_VALUE)
            plasmawave_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(
                plasmawave_table.get(
                    state.get("plasma", ERROR_PARSING_VALUE), ERROR_PARSING_VALUE
                )
            )
            filter_hour_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(state.get("filter_hour", ERROR_PARSING_VALUE))
            air_quality_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(
                air_quality_table.get(
                    state.get("air_quality", ERROR_PARSING_VALUE), ERROR_PARSING_VALUE
                )
            )
            air_qvalue_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(state.get("air_qvalue", ERROR_PARSING_VALUE))
            ambient_light_metric.labels(
                id=device.id,
                mac=device.mac,
                alias=device.alias,
                location_code=device.location_code,
            ).set(state.get("ambient_light", ERROR_PARSING_VALUE))
            # print out for every scrape
            print(datetime.now())
            for f, v in state.items():
                print(f"{f:>15} : {v}")
        print(f"Sleeping {interval} seconds until the next winix api scrape...")
        time.sleep(interval)

#!/usr/bin/env python3

import pandas as pd
from selenium import webdriver
from datetime import timedelta, date, datetime
from pathlib import Path
from tqdm import trange

output_path = Path("data/wetter-de.csv")

def csv_append_create(csv_path: Path, df: pd.DataFrame):
    if csv_path.exists():
        pd.concat((pd.read_csv(csv_path), df), ignore_index=True).to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, index=False)

def process_day(driver, day_offset: int, today: datetime):
    assert 1 <= day_offset <= 14
    base_url = "https://www.wetter.de/deutschland/wetter-regensburg-18226809"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # yeah, I know, weird choice of URL names
    if day_offset == 1:
        driver.get(base_url + "/wetterbericht-morgen.html")
    elif day_offset == 2:
        driver.get(base_url + "/wetterbericht-uebermorgen.html")
    elif day_offset == 3:
        driver.get(base_url + "/wetter-bericht.html")
    elif day_offset == 4:
        driver.get(base_url + "/wettervorhersage.html")
    elif day_offset == 5:
        driver.get(base_url + "/wetter-vorhersage.html")
    elif day_offset == 6:
        driver.get(base_url + "/wettervorschau.html")
    elif day_offset == 7:
        driver.get(base_url + "/wetter-vorschau.html")
    elif day_offset <= 14:
        driver.get(base_url + "/tag-{}.html".format(day_offset + 1))

    return pd.DataFrame({
        "forecast_time": [today + timedelta(day_offset, h * 60 * 60) for h in range(25)],
        "temp": [int(el.get_attribute("innerText")[:-1]) for el in driver.find_elements_by_css_selector(".temperature")],
        "precip_prob": [float(el.get_attribute("innerText")[:-1]) / 100 for el in driver.find_elements_by_css_selector(".forecast-rain span:nth-of-type(2)")],
        "current_time": [current_time] * 25
    })

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    today = date.today()
    today_dt = datetime(today.year, today.month, today.day)

    frames = []
    for day_offset in trange(1, 15):
        frames.append(process_day(driver, day_offset, today_dt))

    driver.close()

    df = pd.concat(frames, ignore_index=True)
    csv_append_create(output_path, df)

if __name__ == "__main__":
    main()

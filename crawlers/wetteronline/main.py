#!/usr/bin/env python3

# crawler for wetteronline.de
# the site provides three different resolutons of forecast:
#   - the next (for every hour)
#   - the next 3 days (three times a day)

from datetime import datetime, timedelta, date
import pandas as pd
from selenium import webdriver
from pathlib import Path

out_stem = Path("data/wetteronline")
out_stem.parent.mkdir(exist_ok=True, parents=True)

def forecast_1(driver, today):
    items = {"forecast_time": [], "temp": [], "rain_prob": [], "weather_type": []}
    for hour_el in driver.find_elements_by_css_selector(".hourly-element.morgen"):
        t = int(hour_el.find_element_by_css_selector(".time").get_attribute("innerText").split(" ")[0])

        temp = int(hour_el.find_element_by_css_selector(".temperature").get_attribute("innerText")[:-1])
        weather_type = hour_el.find_element_by_css_selector(".symbol img").get_attribute("alt")

        rain_prob = int(hour_el.find_element_by_css_selector(".precipitation-probability .value").get_attribute("innerText").split(" ")[0]) / 100.0

        items["forecast_time"].append(today + timedelta(1, t * 60 * 60))
        items["temp"].append(temp)
        items["rain_prob"].append(rain_prob)
        items["weather_type"].append(weather_type)
    return items

def forecast_3(driver, today):
    # NOTE the next day will be skipped (already handled in forecast_1)
    max_temp_2 = driver.find_element_by_css_selector("#weather .Maximum.Temperature td:nth-child(3) span.temp").get_attribute("innerText")[:-1]
    max_temp_3 = driver.find_element_by_css_selector("#weather .Maximum.Temperature td:nth-child(4) span.temp").get_attribute("innerText")[:-1]

    min_temp_2 = driver.find_element_by_css_selector("#weather .Minimum.Temperature td:nth-child(3) span.temp").get_attribute("innerText")[:-1]
    min_temp_3 = driver.find_element_by_css_selector("#weather .Minimum.Temperature td:nth-child(4) span.temp").get_attribute("innerText")[:-1]

    rain_probs = [int(e.get_attribute("innerText").split(" ")[0]) / 100 for e in driver.find_elements_by_css_selector("#weather .prec")[2:]]

    items = {
        "forecast_date": [today + timedelta(2), today + timedelta(3)],
        "max_temp": [max_temp_2, max_temp_3],
        "min_temp": [min_temp_2, min_temp_3],
        "rain_prob": rain_probs
    }
    return items

def main():
    location = "regensburg"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    print("Launch browser")
    driver = webdriver.Chrome(options=options)

    today = date.today()
    now_date = datetime(today.year, today.month, today.day)
    now_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Open the web page...", end="", flush=True)
    driver.get(f"https://www.wetteronline.de/wetter/{location}")
    print("done")

    pred_1 = forecast_1(driver, now_date)
    pred_3 = forecast_3(driver, now_date)

    driver.close()

    df = pd.DataFrame(pred_1)
    df["get_time"] = now_stamp
    path_1 = out_stem.with_name(out_stem.name + "_1.csv")
    if path_1.exists():
        pd.concat(pd.read_csv(path_1), df, ignore_index=False).to_csv(path_1, index=False)
    else:
        df.to_csv(path_1, index=False)

    df = pd.DataFrame(pred_3)
    df["get_time"] = now_stamp
    path_3 = out_stem.with_name(out_stem.name + "_3.csv")
    if path_3.exists():
        pd.concat(pd.read_csv(path_3), df, ignore_index=False).to_csv(path_3, index=False)
    else:
        df.to_csv(path_3, index=False)


if __name__ == "__main__":
    main()

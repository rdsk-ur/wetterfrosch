# Wetterfrosch

Compare different weather websites for your location and find out which one's the best.

## How it works

A script schedules a set of crawlers for various weather websites at certain times of the day and fetches data continously. Each crawler produces it's own data file which has to be merged if a full analysis is planned.

## Crawlers

For each weather station, a separate crawler has to be implemented. Each crawler is located in a separate folder in the the `crawlers` directory (e.g. `crawlers/wetteronline`). You can use any framework or programming language for the crawlers as long as the following criteria are implemented:

- There is an executabe file called `run.*` or simply `run` in the top level directory of the crawler, this is the entry point of the crawler
- The crawler should be able to run without any command line arguments
- The crawler should store it's results in csv files `data/{crawler_name}*.csv`. You can replace `*` with everything you want.
- The crawler should create csv files if they don't exist and append if they do exist
- The CSV file should contain the following columns:
    - `forecast_time`: The start of the timeframe of the forecast
    - `forecast_time_end`: The end of the timeframe of the forecast
    - `temp` (or `max_temp` and `min_temp` if available): The temperature. If the forcast is for a longer timeframe, there sometimes is a maximum and a minimum temperature available.
    - `precip_prob`: The precipitation probability
    - `curent_time`: The time when the request to the website was initiated
- Until further notice, the crawler should fetch the forecasts for [Regensburg](https://en.wikipedia.org/wiki/Regensburg)

Note that although some websites have simple APIs that can be used, we still call the program that fetches the data from APIs a crawler.

Currently, crawlers for the following websites are implemented:

- darksky.net
- wetter.de
- wetteronline.de

## TODOs

- Write more crawlers
- Analyse the data
- Gather reference data (what was the actual weather?)

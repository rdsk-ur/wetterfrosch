# Wetterfrosch

Compare different weather websites for your location and find out which one's the best.

## Crawlers

For each weather station, a separate crawler has to be implemented. Each crawler is located in a separate folder in the the `crawlers` directory (e.g. `crawlers/wetteronline`). You can use any framework or programming language for the crawlers. For now, it should simply load the forecasts for Regensburg and store them in the `data` directory with a prefix that can be used to identify the crawler.

## TODOs

- Write more crawlers
- Add a tool to run all crawlers automatically
- Analyse the data
- Gather reference data (what was the actual weather?)

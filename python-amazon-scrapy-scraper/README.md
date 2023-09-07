GOOGLE AMAZON SCRAPER
=============

This project comprises scraping of amazon and google search spiders.

It comprises of two spiders:

- asins 
- search_terms

The `asins` scraper starts from a csv file containing amazon asins and scrapes the asin pages. The input file should be named `asins.csv` and have below format (i.e. must contain at least the shown column names). The `ASINs` column must have comma separated values.

|Page ID|Keyword ID|....|ASINs|
|------ |--------|------|-----|
|21981|58422|.....|B08VNG2547,B08X67GSJ6,...|


The `search_terms` spider starts from a csv file containing search terms, goes to google.com, finds all [amazon.com](amazon.com) links and scrapes those pages returning asins. The input file must be named `keywords.csv` and have at least the below columns.

|ID|Keyword|....|
|-----|-----|---|
|1|file cabinets|....|
|2|computer mouse|....|


## Installation
1. Create a virtualenv by running `pipenv shell`
2. Install dependencies from the pipfile

## Running the spiders
Execute `scrapy crawl <spider_name>` at the root of the project.

In case you want to run the spiders from an independent script then follow the pattern in the file `run.py`

## Output
The project supports three modes of output; json, mongodb or postgres. Just enable the relevant one in the `settings.py` file. All can be used at the same time as well.

## Settings
Change the relevant section in `settings.py` file to alter the behaviour of the spiders. Below are some of the settings that can be changed.

- Proxies
- Download timeout
- Concurrent Requests
- Whether to scrape reviews or questions
- What `star` level to scrape
- Whether to enable logging and the output log file
- Database credentials
- Whether to obey the Robots.txt file for amazon and google
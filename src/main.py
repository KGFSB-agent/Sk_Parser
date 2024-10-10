import os
import time
import asyncio
from csv_writer import write_csv
from selenium_parser_sk import selenium_parser, parse_news


def main():
    """
    The main asynchronous function that handles scraping, parsing, translating,
    and writing news data to a CSV file.

    It scrapes news articles from multiple pages, translates their content, 
    and writes the original and translated content to a CSV file. The execution 
    time is measured to evaluate the performance.
    """

    # Start the timer to measure total execution time
    start_time = time.time()

    html = selenium_parser("technology")
    technologies_html, catalogue_title = html
    response = parse_news(technologies_html, catalogue_title)
    write_csv(response, "data/results.csv")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    main()
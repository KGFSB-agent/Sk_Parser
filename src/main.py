import time
from csv_writer import write_csv
# from selenium_parser_sk import selenium_parser
from test import selenium_parser


def main():
    """
    The main function that handles scraping, parsing, and writing technology data to a CSV file.

    It scrapes technology data from a given category, processes the content, 
    and writes it to a CSV file. The execution time is measured to evaluate performance.
    """

    # Start the timer to measure total execution time
    start_time = time.time()

    html = selenium_parser("technology")
    write_csv(html, "data/results.csv")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    main()
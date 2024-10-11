class Scrolls:
    """
    The Scrolls class provides methods for controlling the scrolling of a webpage using Selenium WebDriver.

    Methods:
        __init__(driver): Initializes the Scrolls object with the Selenium WebDriver.
        scroll_by(x, y): Scrolls the page by a specified number of pixels along the X and Y axes.
        scroll_to_bottom(): Scrolls the page to the bottom (end of the document).
        scroll_to_top(): Scrolls the page to the top (start of the document).

    Arguments:
        driver (webdriver): An instance of Selenium WebDriver used to interact with the browser.
    """

    def __init__(self, driver):
        self.driver = driver

    def scroll_by(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y})")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

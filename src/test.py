import time
from os import path
from scrolls import Scrolls
from selenium import webdriver
from dataclasses import dataclass, asdict
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

@dataclass
class TechnologyInfo:
    main_sector: str
    title: str
    sectors: str
    readiness_lvl: str
    description: str
    advantages_of_the_technology: str
    references: str
    technology_url: str


def selenium_parser():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size-=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    scroll = Scrolls(driver)
    wait = WebDriverWait(driver, 5, poll_frequency=1)

    driver.get("https://rnd.sk.ru/lk/catalog")

    CATALOGUE_ITEM = ("xpath", "//div[@class='catalog-item']")
    # ALL_TECHNOLOGIES_URLS = ("xpath", "//div[@class='list__item']//a[@class='tech-card']")
    # ALL_TECHNOLOGIES_TITLES = ("xpath", "//div[@class='list__item']//div[@class='tech-card__title']")

    wait.until(EC.element_to_be_clickable(CATALOGUE_ITEM)).click()

    html_content = driver.page_source

    # time.sleep(1)
    # scroll.scroll_to_bottom()

    # tecnologies_urls = wait.until(EC.visibility_of_all_elements_located(ALL_TECHNOLOGIES_URLS))
    # tecnologies_titles = wait.until(EC.visibility_of_all_elements_located(ALL_TECHNOLOGIES_TITLES))

    # data = [
    #     {}
    # ]

    # urls = []
    # for technology in tecnologies_urls:
    #     url = technology.get_attribute("href")
    #     urls.append(url)

    # titles = []
    # for title in tecnologies_titles:
    #     tec_name = title.text
    #     titles.append(tec_name)

    # sector = []

    # for technology_url in urls:
    #     driver.get(technology_url)



    time.sleep(10)

    print("Конец!:)")
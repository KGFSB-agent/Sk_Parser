import time
from scrolls import Scrolls
from selenium import webdriver
from dataclasses import dataclass, asdict
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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


def existence_checker(driver, locator):
    """
    Checks the existence of an element on the web page by using a locator.
    If the element is found, returns its text; otherwise, returns None.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (tuple): A tuple that contains the strategy to locate the element (e.g., "xpath") and the specific locator.

    Returns:
        str or None: The text of the located element, or None if the element does not exist.
    """
    try:
        element = driver.find_element(*locator)
        return element.text if element else None
    except:
        return None


def selenium_parser(category):
    """
    Initializes a Selenium parser, navigates to a specific category page, and collects HTML data 
    of the technologies listed on that page. The function extracts various details about each 
    technology, such as its sector, readiness level, description, advantages, and references.

    Args:
        category (str): The specific category of technologies to parse.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains details about a specific technology.
    """
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size-=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    scroll = Scrolls(driver)
    wait = WebDriverWait(driver, 20, poll_frequency=2)

    driver.get(f"https://rnd.sk.ru/lk/catalog#{category}")

    CATALOGUE_ITEM = ("xpath", "//div[@class='catalog-item']")  # To click
    CATALOGUE_ITEM_TITLE = ("xpath", "//div[@class='catalog-item']/span[@class='catalog-text']")  # The name of the main industry
    ALL_TECHNOLOGIES_URLS = ("xpath", "//div[@class='list__item']//a[@class='tech-card']")  # All links to technology
    ALL_TECHNOLOGIES_TITLES = ("xpath", "//div[@class='list__item']//div[@class='tech-card__title']")  # All technology names

    wait.until(EC.visibility_of_element_located(CATALOGUE_ITEM_TITLE))
    catalogue_title = driver.find_element(*CATALOGUE_ITEM_TITLE).text
    wait.until(EC.element_to_be_clickable(CATALOGUE_ITEM)).click()

    time.sleep(2)
    
    technologies_urls = driver.find_elements(*ALL_TECHNOLOGIES_URLS)  # List of link objects
    technologies_titles = driver.find_elements(*ALL_TECHNOLOGIES_TITLES)  # List of technology name objects

    results = []
    # print(f"Длинна списка ссылок на технологии: {len(technologies_urls)}")
    # print(f"Ссылка на технологию: {technologies_urls[0].get_attribute('href')}")
    
    for i in range(len(technologies_urls)):
        technology_href = technologies_urls[i].get_attribute("href")
        print(f"Ссылка на технологию: {technology_href}")
        tecnology_title = technologies_titles[i].text
        print(f"Название технологию: {tecnology_title}")
        
        driver.get(technology_href)
        
        time.sleep(2)
        # scroll.scroll_to_bottom()
        
        MAIN_BLOCK_TITLE_SECTOR = ("xpath", "//div[@class='main__block']//span[text()='Отрасль']")  # The path to the text "Отрасль"
        MAIN_BLOCK_TITLE_LVL = ("xpath", "//div[@class='main__block']//span[text()='Уровень готовности']")  # The path to the text "Уровень готовности"
        MAIN_BLOCK_TITLE_DESCRIPTION = ("xpath", "//div[@class='main__block']//span[text()='Описание технологии']")  # The path to the text "Описание технологии"
        MAIN_BLOCK_TITLE_ADVANTAGES = ("xpath", "//div[@class='main__block']//span[text()='Преимущества технологии']")  # The path to the text "Преимущества технологии"
        MAIN_BLOCK_TITLE_REFERENCES = ("xpath", "//div[@class='main__block']//span[text()='Референсы']")  # The path to the text "Референсы"

        main_block_title_sector = existence_checker(driver, MAIN_BLOCK_TITLE_SECTOR)
        main_block_title_lvl = existence_checker(driver, MAIN_BLOCK_TITLE_LVL)
        main_block_title_description = existence_checker(driver, MAIN_BLOCK_TITLE_DESCRIPTION)
        main_block_title_advantages = existence_checker(driver, MAIN_BLOCK_TITLE_ADVANTAGES)
        main_block_title_references = existence_checker(driver, MAIN_BLOCK_TITLE_REFERENCES)

        titles_list = [main_block_title_sector, main_block_title_lvl, main_block_title_description, main_block_title_advantages, main_block_title_references]

        TEXT_SECTOR_LVL = ("xpath", "//div[@class='main__block']//div[@class='text']")  # The path to all texts <div class="text"> in technology (but we only need texts in the industry and readiness lvl.)
        TEXT_DESCRIPTION_ADVANTAGES_REFERENCES = ("xpath", "//div[@class='main__block']//div[@class='text']//p")  # The path to all texts <p> in the description, advantages and references

        texts_sector_lvl = driver.find_elements(*TEXT_SECTOR_LVL)
        texts_description_advantages_references = driver.find_elements(*TEXT_DESCRIPTION_ADVANTAGES_REFERENCES)

        emptiness_counter = 0
        for title in titles_list:
            if not title:
                emptiness_counter += 1

        sector_texts = []
        readiness_lvl_text = "-"
        description_text = "-"
        advantages_text = "-"
        references_text = "-"
        for title_information in titles_list:
            if title_information == titles_list[0]:  # Sector
                if emptiness_counter == 0 and title_information:
                    for text in texts_sector_lvl[:-4]:
                        sector_texts.append(text.text)
                        
                elif emptiness_counter == 1 and title_information:
                    for text in texts_sector_lvl[:-3]:
                        sector_texts.append(text.text)

                elif emptiness_counter == 2 and title_information:
                    for text in texts_sector_lvl[:-2]:
                        sector_texts.append(text.text)
                
                else:  # title_information None
                    sector_texts.append("-")

            elif title_information == titles_list[1]:  # Readiness level
                if emptiness_counter == 0 and title_information:
                    readiness_lvl_text = texts_sector_lvl[-4].text
                        
                elif emptiness_counter == 1 and title_information:
                    readiness_lvl_text = texts_sector_lvl[-3].text

                elif emptiness_counter == 2 and title_information:
                    readiness_lvl_text = texts_sector_lvl[-2].text
                
                else:  # title_information None
                    readiness_lvl_text = "-"
            
            elif title_information == titles_list[2]:  # Description of the technology
                if title_information:
                    description_text = texts_description_advantages_references[0].text

                else:  # title_information None
                    description_text = "-"
            
            elif title_information == titles_list[3]:  # Advantages of the technology
                if emptiness_counter == 0 and title_information:
                    advantages_text = texts_description_advantages_references[1].text
                        
                elif emptiness_counter == 1 and title_information:
                    advantages_text = texts_description_advantages_references[1].text
                
                else:  # title_information None
                    advantages_text = "-"
            
            elif title_information == titles_list[4]:  # References
                if emptiness_counter == 0 and title_information:
                    references_text = texts_description_advantages_references[2].text
                        
                elif emptiness_counter == 1 and title_information:
                    references_text = texts_description_advantages_references[1].text
                
                else:  # title_information None
                    references_text = "-"

        full_sector_text = " ".join(sector_texts)

        new_technology = TechnologyInfo(
            main_sector=catalogue_title,
            title=tecnology_title,
            sectors=full_sector_text,
            readiness_lvl=readiness_lvl_text,
            description=description_text,
            advantages_of_the_technology=advantages_text,
            references=references_text,
            technology_url=technology_href
        )

        # Convert the TechnologyInfo dataclass to a dictionary and add it to the results list
        results.append(asdict(new_technology))
    return results

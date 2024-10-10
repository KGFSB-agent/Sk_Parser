import time
import httpx
from scrolls import Scrolls
from selenium import webdriver
from selectolax.parser import HTMLParser
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


def selenium_parser(category): # инициализирует парсинг, нажимая на категорию и собирая прогрузившийся HTML-код со всеми необходимыми нам данными
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size-=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    scroll = Scrolls(driver)
    wait = WebDriverWait(driver, 5, poll_frequency=1)

    driver.get(f"https://rnd.sk.ru/lk/catalog#{category}")

    CATALOGUE_ITEM = ("xpath", "//div[@class='catalog-item']")
    # CATALOGUE_ITEM_TITLE = ("xpath", "//div[@class='catalog-item']/span[@class='catalog-text']")

    wait.until(EC.element_to_be_clickable(CATALOGUE_ITEM)).click()

    time.sleep(2)
    scroll.scroll_to_bottom()
    
    catalogue_title = "БЕЗОПАСНОСТЬ И КОНТРОЛЬНО-НАДЗОРНАЯ ДЕЯТЕЛЬНОСТЬ"
    # catalogue_title = driver.find_element(*CATALOGUE_ITEM_TITLE).text
    # catalogue_title = wait.until(EC.visibility_of_element_located(CATALOGUE_ITEM_TITLE)).text

    html_content = driver.page_source
    
    return html_content, catalogue_title


def parse_news(html_code, catalogue_name):
    """
    Parses the HTML content to extract news articles from the China Briefing website.

    Args:
        html (HTMLParser): The parsed HTML content of a news page.

    Returns:
        list: A list of dictionaries containing information about each news article, 
              including title, date, link, short text, and main text.
    """
    
    html = HTMLParser(html_code)
    technologies = html.css("div.list__item")
    print(len(technologies))

    titles = ["Отрасль", "Уровень готовности", "Описание технологии", "Преимущества технологии", "Референсы"]

    results = []
    for technology in technologies:
        technology_href = technology.css_first("a").attributes.get('href')
        technology_title = technology.css_first("div.tech-card__title").text()
        response = httpx.get(f"https://rnd.sk.ru{technology_href}")
        time.sleep(4)
        technology_html = HTMLParser(response.text)

        print(technology_html)
        technology_inner_info = technology_html.css_first("div.main__body")
        print(technology_inner_info)
        
        sectors_text = []
        technology_blocks = technology_inner_info.css("div.main__block")
        
        for block in technology_blocks:
            main_block_title = block.css_first("div.block-title.block-title--sm span").text()
            
            if main_block_title == titles[0]:
                sectors_text = block.css("div.text")
                for text in sectors_text:
                    sectors_text.append(text.text())
            
            elif main_block_title == titles[1]:
                readiness_lvl_text = block.css_first("div.text").text()
            
            elif main_block_title == titles[2]:
                description_text = block.css_first("div.text").text()
            
            elif main_block_title == titles[3]:
                # Проверяем наличие элемента перед доступом к тексту
                advantages_element = block.css_first("div.text")
                if advantages_element:
                    advantages_of_the_technology_text = advantages_element.text()
                else:
                    advantages_of_the_technology_text = "-"
            
            elif main_block_title == titles[4]:
                # Проверяем наличие элемента перед доступом к тексту
                references_element = block.css_first("div.text")
                if references_element:
                    references_text = references_element.text()
                else:
                    references_text = "-"   
        
        # Join all the text elements into one string to represent the full article text
        full_sector_text = " ".join(sectors_text)

        # Create a new NewsTitle object with the extracted data
        new_technology = TechnologyInfo(
            main_sector=catalogue_name,
            title=technology_title,
            sectors=full_sector_text,
            readiness_lvl=readiness_lvl_text,
            description=description_text,
            advantages_of_the_technology=advantages_of_the_technology_text,
            references=references_text,
            technology_url=technology_href
        )

        # Convert the NewsTitle dataclass to a dictionary and add it to the results list
        results.append(asdict(new_technology))
    return results

import os
import selenium.webdriver as webdriver

from utils import source_urls_file, html_folder
from utils import create_logger, safe_write

logger = create_logger("get_vacancy_html_by_url_list")

# with позволяет аккуратно работать с файлом, сразу же его закрывать после
with open(source_urls_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f]
    
urls = list(set(urls)) # удаляем дубли ссылок

already_parsed_urls = set(list(os.listdir(html_folder)))

urls = list(set(urls) - already_parsed_urls) # удаляем уже спаршенные ссылки

browser = webdriver.Chrome()

for url in urls:
    logger.info("Открываю " + url)
    
    browser.get(url)
    content = browser.page_source

    logger.info("Контент получен размера " + str(len(content)))

    # оставляем только slug вакансии (slug = sistemnyy-administrator-junior-85981706)
    page_slug = url.split("/")[-1].split('.')[0] 
    
    file_name = os.path.join(html_folder, page_slug) + ".html"
    safe_write(file_name, content)
    logger.info("Записано в " + file_name)
    break #TODO


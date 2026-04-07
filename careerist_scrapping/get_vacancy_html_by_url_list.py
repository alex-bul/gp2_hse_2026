import logging
import os
import time
import selenium.webdriver as webdriver

from datetime import datetime

logger = logging.getLogger("parse_vacancy_list") 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # чтобы вне зависимости от запуска создавать все внутри папки

logs_folder = os.path.join(BASE_DIR, "logs") # папка для логов
html_folder = os.path.join(BASE_DIR, "page_html") # сохраняется html страниц по мере парсинга для того чтобы если что по другому распарсить
source_urls_file = os.path.join(BASE_DIR, "vacancy_links.txt")  # файл с ссылками на вакансии
result_csv_file = os.path.join(BASE_DIR, "result.csv") # файл с результатами = таблицей с данными


os.makedirs(logs_folder, exist_ok=True) # создаем папку, если ее еще нет
os.makedirs(html_folder, exist_ok=True) # создаем папку, если ее еще нет


logging.basicConfig(
    filename=datetime.now().strftime(f"{logs_folder}/%Y-%m-%d_%H-%M-%S.log"), # создаем файл логов с текущем временем в имени
    level=logging.INFO, 
    # уровень логирования (debug, info, warning, error, critical), начиная с какого сохранять
    # мы хотим INFO, так как иначе много логов от селениум набегает
    format="%(asctime)s %(levelname)s %(message)s" # формат логов: время, уровень, сам текст
)
logger = logging.getLogger("parse_vacancy_list")


def safe_write(file_name, content):
    """
    Безопасная запись в файл. Пишем в tmp файл, а потом заменяем.
    Избегаем кейса, когда в момент записи программа упадет и файл затрется
    """
    tmp_file_name = file_name + ".tmp" # чтобы в случае внезапной остановки при записи данные сохранились
    with open(tmp_file_name, mode="w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_file_name, file_name) # tmp на реальный файл заменяем

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
    break


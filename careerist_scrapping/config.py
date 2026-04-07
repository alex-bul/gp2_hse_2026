import logging
import os
import datetime

logger = logging.getLogger("parse_vacancy_list") 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # чтобы вне зависимости от запуска создавать все внутри папки

logs_folder = os.path.join(BASE_DIR, "logs") # папка для логов
html_folder = os.path.join(BASE_DIR, "page_html") # сохраняется html страниц по мере парсинга для того чтобы если что по другому распарсить
source_urls_file = os.path.join(BASE_DIR, "vacancy_links.txt")  # файл с ссылками на вакансии
result_csv_file = os.path.join(BASE_DIR, "result.csv") # файл с результатами = таблицей с данными

os.makedirs(logs_folder, exist_ok=True) # создаем папку, если ее еще нет
os.makedirs(html_folder, exist_ok=True) # создаем папку, если ее еще нет

def create_logger(script_name):
    """
    Создает логгер для каждого скрипта с его именем, чтобы не дублировать код
    """

    # создаем файл логов с текущем временем в имени
    log_filename = datetime.datetime.now().strftime(f"{logs_folder}/{script_name}_%Y-%m-%d_%H-%M-%S.log")
    
    # логгер для конкретного скрипта, задаем имя
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO) 
    # мы хотим INFO, так как иначе много логов от селениум набегает
    # уровень логирования (debug, info, warning, error, critical)
    
    # Создаем handler для записи в файл
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    
    # формат логов: время, уровень, текст
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    
    # Добавляем handler к логгеру
    logger.addHandler(file_handler)
    
    return logger
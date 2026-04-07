import pandas as pd
import os

from bs4 import BeautifulSoup

from utils import html_folder, result_csv_file, columns
from utils import create_logger, safe_write

logger = create_logger("parse_vacancy_html")

df = pd.read_csv(result_csv_file)

# получаем слаги, которые уже в датасете
already_parsed_slugs = set(df["slug"])

# получаем html файлы в папке
page_html_files = [f for f in os.listdir(html_folder) if f.endswith(".html")]
# удаляем ранее распаршенные слаги
page_html_files = list(set(page_html_files) - already_parsed_slugs)

logger.info(f"Найдено {len(page_html_files)} html файлов для распаршивания")

# def vacancy_html_to_row(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")

#     soup.find("div", {"class": "b-b-1 vacancyPageHeaderNew for-hdr-1"})


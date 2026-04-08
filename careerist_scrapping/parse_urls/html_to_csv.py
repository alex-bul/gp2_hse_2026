import pandas as pd
import os

from bs4 import BeautifulSoup

from careerist_scrapping.parse_urls.utils import html_folder, result_csv_file, csv_sep
from careerist_scrapping.parse_urls.utils import create_logger, safe_write

logger = create_logger("parse_vacancy_html")

def vacancy_html_to_row(slug, html_content):
    logger.info(f"Парсим вакансию {slug}, размер html {len(html_content)}")
    soup = BeautifulSoup(html_content, "html.parser")

    # берется из синих ссылок на странице вверху разделов
    category = soup.find("ol", {"class": "breadcrumb hidden-sm-down"}).find_all("span")[1].text.strip(" ⚫  ✔ ")

    
    # основной блок информацией о вакансии: заголовок, параметры, описание
    vacancy_content_block = soup.find("div", {"class": "targetDesBG"}) 

    profession = vacancy_content_block.find("div", {"class": "b-b-1 vacancyPageHeaderNew for-hdr-1"}).find("h1").text.strip()

    # блок с параметрами вакансии: опыт, город, занятость
    vacancy_param_block = vacancy_content_block.find_all("div", {"class": "b-b-1"})[1]
    publication_date = vacancy_param_block.find("p", {"class": "pull-xs-right m-l-1 text-small"}).text.strip()

    # зарплаты может и не быть
    try:
        salary = vacancy_param_block.find("p", {"class": "h5"}).text.strip()
    except:
        logger.error(f"Не удалось найти зарплату")
        salary = None

    firm_name = vacancy_param_block.find("div", {"class": "m-b-10"}).text.strip()

    param_rows = vacancy_param_block.find("div", {"class": "row"}).find_all("p")
    param_dict = dict()
    for i in range(0, len(param_rows), 2): # идем с шагом два, чтобы пары собирать
        # два раза strip, потому что первый убирает все пробелы/переносы, а второй убирает ":"
        param_dict[param_rows[i].text.strip().strip(":")] = param_rows[i + 1].text.strip().strip(":")

    experience = param_dict.get("Опыт")
    city = param_dict.get("Город")
    employment = param_dict.get("Занятость")

    raw_description = vacancy_content_block.find_all("div", {"class": "b-b-1"})[2]
    description = raw_description.text.strip()

    result = [slug, profession, salary, firm_name, city, employment, experience, raw_description, description, publication_date, category]
    return result

df = pd.read_csv(result_csv_file, sep=csv_sep)

with open(result_csv_file, "r", encoding="utf-8") as f:
    csv_raw_content = f.read().strip()

# получаем слаги, которые уже в датасете
already_parsed_slugs = set(df["slug"])
logger.info(f"Найдено {len(already_parsed_slugs)} уже распаршенных вакансий")

# получаем html файлы в папке
page_html_slug= [f.split('.')[0] for f in os.listdir(html_folder) if f.endswith(".html")]
html_in_folder = len(page_html_slug)
logger.info(f"Найдено {html_in_folder} html файлов в папке")

# удаляем ранее распаршенные слаги
page_html_slug = list(set(page_html_slug) - already_parsed_slugs)
logger.info(f"После удаления распаршенных вакансий осталось {len(page_html_slug)}")



for index, html_file_name in enumerate(page_html_slug):
    logger.info(f"Парсим {index + 1}/{len(page_html_slug)} (в папке всего {html_in_folder})")

    # получаем путь до html файла
    html_file_path = os.path.join(html_folder, html_file_name + ".html")
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    slug = html_file_name.split(".")[0]
    try:
        result = vacancy_html_to_row(slug, html_content)
    except Exception as e:
        logger.exception("Не удалось распарсить вакансию " + slug)
        continue
    
    # сколько значений заполнено
    logger.info("Количество не None " + str(len([i for i in result if i is not None])))

    # делаем все строками (возможны None), чтобы потом сделать csv строку
    # очищаем от переносов и от csv_sep, чтобы не ломать csv
    result = [str(i).replace(csv_sep, ",").replace("\n", " ") for i in result] 

    new_row = csv_sep.join(result)

    csv_raw_content += "\n" + new_row

    if index % 1000 == 0:
        logger.info("Записываю в файл, строк в файле " + str(csv_raw_content.count("\n")))
        safe_write(result_csv_file, csv_raw_content)

    # break

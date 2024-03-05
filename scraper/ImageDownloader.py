import requests
import os
import time
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #убрать предупреждение  InsecureRequestWarning


readyLinks = [] #Все исходные ссылки на изображения
SAVE_DIRECTORY = "ScrappedData/Images"  # Папка для сохранения изображения
# Открытие файла для чтения
with open('img_links.txt', 'r', encoding='utf-8') as file:
    # Чтение каждой строки из файла
    for line in file:
        #print(line)
        # Разделение строки на название и ссылку
        сategory, name, link_page, link_upload = line.strip().split('| ')
        # Добавление названия и ссылки в массив preparedLinks
        readyLinks.append([сategory, name, link_page, link_upload])

# #получаем готовый Url необходимой страницы для BS4, параметр verify можно отключить, в зависимости от сайта
def getNewUrl(newUrl):
    r=requests.get(newUrl,verify=False)
    return r.text


# def download_image(image_url, new_filename):

#     # Отправляем GET-запрос для загрузки страницы
#     response = requests.get(image_url,verify=False)

#     # Проверяем успешность запроса
#     if response.status_code == 200:
#         # Используем BeautifulSoup для парсинга HTML страницы
#         soup = BeautifulSoup(getNewUrl(image_url), 'html.parser', from_encoding='ascii')
#         print("\n********************************************************")
#         print(soup)
#         print("********************************************************\n")
#         # Находим тег <img> с заданным URL изображения
#         img_tag = soup.find('img')
#         print("\n********************************************************")
#         print(img_tag)
#         print("********************************************************\n")
#         if img_tag:
#             # Получаем URL изображения
#             img_src = img_tag.get('src')

#             # Отправляем GET-запрос для загрузки изображения
#             img_response = requests.get(img_src,verify=False)

#             # Проверяем успешность запроса
#             if img_response.status_code == 200:
#                 # Создаем папку, если она не существует
#                 if not os.path.exists(SAVE_DIRECTORY):
#                     os.makedirs(SAVE_DIRECTORY)
            
#                 img_filename = new_filename
#                 # Путь для сохранения изображения
#                 save_path = os.path.join(SAVE_DIRECTORY, img_filename)

#                 # Сохраняем изображение на диск
#                 with open(save_path, 'wb') as f:
#                     f.write(img_response.content)
#                 print("Изображение успешно сохранено:", save_path)
#             else:
#                 print("Ошибка при загрузке изображения:", img_response.status_code)
#         else:
#             print("Изображение не найдено на странице.")
#     else:
#         print("Ошибка при загрузке страницы:", response.status_code)



def download_image(image_url, new_filename):

    # Отправляем GET-запрос для загрузки страницы
    response = requests.get(image_url,verify=False)

    # Проверяем успешность запроса
    if response.status_code == 200:
        
        # Создаем папку, если она не существует
        if not os.path.exists(SAVE_DIRECTORY):
            os.makedirs(SAVE_DIRECTORY)
    
        img_filename = new_filename
        # Путь для сохранения изображения
        save_path = os.path.join(SAVE_DIRECTORY, img_filename)

        # Сохраняем изображение на диск
        with open(save_path, 'wb') as f:
            f.write(response.content)
        # print("Изображение успешно сохранено:", save_path)

    else:
        print("Ошибка при загрузке страницы:", response.status_code)



# # Пример использования
# image_url = "https://example.com/image.jpg"  # Замените на нужный URL изображения

# new_filename = "my_custom_image.jpg"  # Новое имя файла (необязательно)
# download_image(image_url,  new_filename)



# #####################################################################################

# #функции для чтения и записи файла, в котором хранится позиция последнего спарсенного файла.
def check_write(value):
    try:
        with open('check.txt', 'w') as file:
            file.write(str(value))
    except Exception as e:
        print("\nCheck WRITE -", e)

def check_read(value):
    try:
        with open('check.txt', 'r') as file:
            value = int(file.read())
        return value
    except Exception as e:
        print("\n*Check READ - :", e)


# Функция для создание имени изображения.
def create_image_name(data_input):
    category=RepairArticleName(data_input[0])
    name=RepairArticleName(data_input[1])
    return str(category + "_" + name+".png")

# Убрать запрещенные символы
def RepairArticleName(string):
    forbidden_symbols = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for symbol in forbidden_symbols:
        string = string.replace(symbol, '')
    return string
# #####################################################################################

def Data_splitter(data_input, start_position):
    check_counter = 1
    print("\n*START POSITION = ", start_position)
    for data in tqdm(data_input[start_position:]):
        name=create_image_name(data)
        download_image(data[3],name)
        check_counter += 1
        check_write(start_position+check_counter)
    
    print("\n\n***EXECUTED SUCCESSFULLY!***\n SCRAPPED = ", check_counter,"PAGES")
    return check_counter
#####################################################################################
#момент истины:

def startScrapper(pages):

    scrapper_data=readyLinks[:pages]
    scrapper_pos=0

    scrapper_pos=check_read(scrapper_pos)
    start_time = time.time()
    scrapper_pos=scrapper_pos+Data_splitter(scrapper_data, scrapper_pos)
    end_time = time.time() - start_time
    print("\n\nEXECUTION TIME: ",end_time)
    scrapper_pos=check_write(scrapper_pos)

# #####################################################################################
# #ставь число стольких страниц, сколько ты хочешь соскрапитьдо какой ты хочешь скрапить
# #ВНИМАНИЕ, для самого начала скраппинга нужно поставить значение внутри check в 0
    
####################################################################################
#MAIN

startScrapper(1055)


########################################################################



# import requests
# import json
# from bs4 import BeautifulSoup
# import os
# import numpy as np
# import time
# from tqdm import tqdm

# from urllib.parse import unquote

# LINK_DOMEN="https://xn--80aag1ciek.xn--h1aagk2bza.xn--p1ai/catalog/rybalka/udilishcha/"





# #############################################################################

# # #получаем готовый Url следующей страницы для BS4
# def getNewUrl(newUrl):
#     r=requests.get(newUrl)
#     return r.text



# # Открытие файла для чтения
# with open('links.txt', 'r', encoding='utf-8') as file:
#     # Чтение каждой строки из файла
#     for line in file:
#         #print(line)
#         # Разделение строки на название и ссылку
#         name, link = line.strip().split('| ')
#         # Добавление названия и ссылки в массив preparedLinks
#         readyLinks.append([name, link])

# #############################################################################

# # #Достаем индивидуальную часть ссылки
# def getSpecialLink(raw_link):
#     ready_link= raw_link.split("/")[-1]
#     return ready_link

# #############################################################################

# #странички будут парситься и информация будет лежать в данном классе

# class Data():
#     title:str
#     id:int
#     category=[]
#     text:str
#     link:str

# #############################################################################

# def categoryPrepare(arr):
#     tmp = ""
#     for inner_list in arr:
#         if inner_list[0] is not None:
#             tmp += inner_list[0] + ", "
#     tmp = tmp.rstrip(", ")  # Удаляем последнюю запятую и пробел
#     tmp2 = tmp.replace("Категория:", "")
#     result = tmp2.split(", ")
#     return result

# #############################################################################

# # #спарсим айди страницы из специальной версии страницы (API)
# # def ParseID(special_link):
# #     special_url=f"{LINK_DOMEN}/api.php?action=parse&page={special_link}&format=json&formatversion=2"
# #     soup=BeautifulSoup(getNewUrl(special_url),'lxml')
# #     parse_data=soup.find('p')
# #     data=parse_data.text

# #     # Find the index of "pageid"
# #     pageid_start_index = data.find('"pageid":') + len('"pageid":')

# #     # Find the index of the comma or closing brace after the pageid value
# #     pageid_end_index = data.find(',', pageid_start_index)
# #     if pageid_end_index == -1:
# #         pageid_end_index = data.find('}', pageid_start_index)

# #     # Extract the pageid value
# #     pageid = data[pageid_start_index:pageid_end_index]
# #     return pageid

# #############################################################################

# #парсим основную страницу, вытаскиваем категории и чистый текст статьи


# def ParseMainPage(link):
#     result=[[],""]
#     raw_categories=[]
#     soup=BeautifulSoup(getNewUrl(link),'lxml')
#     raw_data=soup.find('div',class_='page-header__categories')
#     if raw_data:
#         raw_datas=raw_data.findAll('a')

#         for a in raw_datas:
#             if a:
#                 raw_category=a.get('title')
            
#                 raw_categories.append([raw_category])
#         prepared_category=  categoryPrepare(raw_categories)

#         main_text_raw = soup.find('div',class_='mw-parser-output')
#         if main_text_raw:
#             unwanted_elements = main_text_raw.find_all(['script', 'aside', 'p'], class_='caption')

#             for element in unwanted_elements:
#                 element.extract()
#             main_text_prepared = main_text_raw.get_text()

#             result=[prepared_category,main_text_prepared]

#             return result
#         else:
#             return result
#     else :
#         return result



# #############################################################################

# #вспомогательная функция конвертации данных основного текста в нормальный вид
# def RepairMainText(raw_data):
#     ready_data:str=raw_data
#     return ready_data

# def RepairArticleName(string):
#     forbidden_symbols = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
#     for symbol in forbidden_symbols:
#         string = string.replace(symbol, '')
#     return string


# #############################################################################


# #Без шуток основная функция - тут мы скрапим, обрабатываем и закидываем в JSON

# def JustDoIt(article):
#     special_link=getSpecialLink(article[1])
#     main_link=article[1]

#     raw_data=ParseMainPage(main_link)
#     tmp_data=Data()
#     #tmp_data.id=ParseID(special_link)
#     tmp_data.title=article[0]
#     tmp_data.link=article[1]
#     tmp_data.category= raw_data[0]
#     tmp_data.text=RepairMainText(raw_data[1])

#     # Create a directory to store the files if it doesn't exist
#     directory = "scrappedArticles"
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     #отгружаем в файл JSON
#     tmp_raw_filename= unquote(special_link)
#     tmp_ready_filename=RepairArticleName(tmp_raw_filename)
#     filename = os.path.join(directory,tmp_ready_filename + ".json")
#     data_out = {"title":tmp_data.title,
#                 "link":tmp_data.link,
#                 #"id":  tmp_data.id,
#                 "category":  tmp_data.category,
#                 "text": tmp_data.text}
#     with open(filename, 'w',encoding='utf-8') as file_out:
#         json.dump(data_out, file_out,ensure_ascii=False, indent=4)
    


# #####################################################################################

# #функции для чтения и записи файла, в котором хранится позиция последнего спарсенного файла.
# def check_write(value):
#     try:
#         with open('check.txt', 'w') as file:
#             file.write(str(value))
#     except Exception as e:
#         print("\nCheck WRITE -", e)

# def check_read(value):
#     try:
#         with open('check.txt', 'r') as file:
#             value = int(file.read())
#         return value
#     except Exception as e:
#         print("\n*Check READ - :", e)



# #####################################################################################

# def Data_splitter(data_input, start_position):
#     check_counter = 1
#     print("\n*START POSITION = ", start_position)
#     for data in tqdm(data_input[start_position:]):
#         JustDoIt(data)
#         check_counter += 1
#         check_write(start_position+check_counter)
    
#     print("\n\n***EXECUTED SUCCESSFULLY!***\n SCRAPPED = ", check_counter,"PAGES")
#     return check_counter
# #####################################################################################
# #момент истины:

# def startScrapper(pages):

#     scrapper_data=readyLinks[:pages]
#     scrapper_pos=0
#     scrapper_pos=check_read(scrapper_pos)
#     start_time = time.time()
#     scrapper_pos=scrapper_pos+Data_splitter(scrapper_data, scrapper_pos)
#     end_time = time.time() - start_time
#     print("\n\nEXECUTION TIME: ",end_time)
#     scrapper_pos=check_write(scrapper_pos)

# #####################################################################################
# #ставь число стольких страниц, сколько ты хочешь соскрапитьдо какой ты хочешь скрапить
# #ВНИМАНИЕ, для самого начала скраппинга нужно поставить значение внутри check в 0
# startScrapper(4600)

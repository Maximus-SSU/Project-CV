import requests
import json
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #убрать предупреждение  InsecureRequestWarning

# Список всех ссылок на  нужные категории
LINK_CATEGORY_JUICE="https://online.metro-cc.ru/category/bezalkogolnye-napitki/soki-morsy-nektary?page="
LINK_CATEGORY_WATER="https://online.metro-cc.ru/category/bezalkogolnye-napitki/pityevaya-voda-kulery?page="
LINK_CATEGORY_CHEESE="https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?page="
LINK_CATEGORY_DAIRY="https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/jogurty?page="
LINK_CATEGORY_OFFICE_MEBEL="https://online.metro-cc.ru/category/ofis-obuchenie-hobbi/tovary-dlya-ofisa/mebel-119001001"
LINK_CATEGORY_FISH="https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?page="
LINK_CATEGORY_BAKERY="https://online.metro-cc.ru/category/hleb-vypechka-torty/hleb-lavash-lepeshki?page="
LINK_CATEGORY_CANNED_GOODS="https://online.metro-cc.ru/category/bakaleya/konservy?page="
LINK_CATEGORY_TABLEWARE="https://online.metro-cc.ru/category/tovary-dlya-doma-dachi-sada/posuda/stolovye-pribory?page="
LINK_CATEGORY_KNIFE="https://online.metro-cc.ru/category/tovary-dlya-doma-dachi-sada/posuda/nozhi-i-razdelochnye-doski/f/tip/nozh?page="
LINK_CATEGORY_TOWEL="https://online.metro-cc.ru/category/tovary-dlya-doma-dachi-sada/domashniy-tekstil/polotentsa-khalaty-tapochki?page="
LINK_CATEGORY_CUPS="https://online.metro-cc.ru/category/tovary-dlya-doma-dachi-sada/posuda/posuda-dlya-chaya-i-kofe?page="
# Основная ссылка на сайт
# LINK_PRODUCT_DOMEN="https://leroymerlin.ru/product/"
# LINK_UPLOAD_DOMEN="https://cdn.leroymerlin.ru/lmru/image/upload/"
MAIN_LINK_DOMEN="https://online.metro-cc.ru"


# #получаем готовый Url необходимой страницы для BS4, параметр verify можно отключить, в зависимости от сайта
def getNewUrl(newUrl):
    r=requests.get(newUrl)
    if r.status_code==200:
        # print(f"\nSUCCESS - Status CODE: = {r.status_code}")
        return r.text
    else:
        print(f"\nERROR - Status CODE: = {r.status_code}")
        return r.text


# парсим каждую страницу
def ParsePage(soup, item_group):
    soup=soup.find('div', class_="subcategory-or-type__products")
    rawData=soup.findAll('a') #Список всех картинок
    for element in rawData:
        element_link= element.get('href') 
        element_title= element.get('title')
        picture_link= element.find('img')
        if picture_link is not None:

            # debug MODE:
            #####################################################################
            # count+=1
            # print("\n________________________________________________________")
 
            # print("\n********************************************************")
            # print(element_link)
            # print("\n********************************************************")
            # print(picture_link)
            # print("\n********************************************************")
             ####################################################################
            picture_link_upload=picture_link.get('src')
            prepared_element_link=MAIN_LINK_DOMEN+element_link
            preparedLinks.append([item_group,element_title,prepared_element_link,picture_link_upload])
    # rawLinks_length=len(rawLinks)# количество всех ссылок
        # if rawLinks_length==21 :
        #     return True
        # else :
        #     return False




#Парсим все
def Parse(startUrl,item_group,max_pages_in_group):
    if max_pages_in_group>0:
        for page_count in range (1,max_pages_in_group+1):
            url=startUrl+str(page_count)
            # print("\nTRY SCRAPPING : "+ url+"\n")
            Soup=BeautifulSoup(getNewUrl(url),'lxml')
            ParsePage(Soup,item_group)
            page_count+=1
    else:
        url=startUrl
        # print("\nTRY SCRAPPING : "+ url+"\n")
        Soup=BeautifulSoup(getNewUrl(url),'lxml')
        ParsePage(Soup,item_group)



#заливаем ссылки в формате: название | ссылка
def CreateLinkDocument(ListOut):
     with open('img_links.txt','w',encoding='utf-8') as file:
          for link in ListOut:
               file.write(f"{link[0]} | {link[1]} | {link[2]} | {link[3]}\n")
            


################################################################################################################
#MAIN:

preparedLinks=[]
start_DATA=[
    (LINK_CATEGORY_JUICE,"Соки",3),
    (LINK_CATEGORY_WATER,"Вода",3),
    (LINK_CATEGORY_CHEESE,"Сыры",3),
    (LINK_CATEGORY_CHEESE,"Йогурты",3),
    (LINK_CATEGORY_OFFICE_MEBEL,"Офисная мебель",0),
    (LINK_CATEGORY_FISH,"Рыба",3),
    (LINK_CATEGORY_BAKERY,"Хлеб",3),
    (LINK_CATEGORY_CANNED_GOODS,"Консервы",5),
    (LINK_CATEGORY_TABLEWARE,"Столовые приборы",3),
    (LINK_CATEGORY_KNIFE,"Ножи",3),
    (LINK_CATEGORY_TOWEL,"Полотенца",3),
    (LINK_CATEGORY_CUPS,"Чашки",3)
    ]

k=len(start_DATA)
for i in tqdm(range(0,k)):

    Parse(start_DATA[i][0],start_DATA[i][1],start_DATA[i][2])



#################################################################
# debug mode
# Parse(start_DATA[0][0],start_DATA[0][1],start_DATA[0][2])
###############################################################

CreateLinkDocument(preparedLinks)
parsed_count= len(preparedLinks)
print(f"\n * SUCCESSFULLY SCRAPPED {parsed_count}] LINKS\n")


########################################################################################################

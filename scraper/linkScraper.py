import requests
import json
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #убрать предупреждение  InsecureRequestWarning

# Список всех ссылок на  нужные категории
LINK_DOMEN_UDOCHKI="https://саратов.хищник.рф/catalog/rybalka/udilishcha/?PAGEN_1="
LINK_DOMEN_KATUSHKI="https://саратов.хищник.рф/catalog/rybalka/katushki/?PAGEN_1="
LINK_DOMEN_LESKA="https://саратов.хищник.рф/catalog/rybalka/leska-shnury/?PAGEN_1="
LINK_DOMEN_KOROBKI="https://саратов.хищник.рф/catalog/rybalka/korobki-i-tubusy/korobki/?PAGEN_1="
LINK_DOMEN_YASCHIKI="https://саратов.хищник.рф/catalog/rybalka/korobki-i-tubusy/yashchiki/?PAGEN_1="
LINK_DOMEN_NODZI="https://саратов.хищник.рф/catalog/turizm/orudiya-i-instrumenty/nozhi/?PAGEN_1="
LINK_DOMEN_MULTITOOLS="https://саратов.хищник.рф/catalog/turizm/orudiya-i-instrumenty/instrument/?PAGEN_1="
LINK_DOMEN_MOTORY="https://саратов.хищник.рф/catalog/lodki-i-motory/lodochnye-motory/lodochnye-motory-dvs/?PAGEN_1="
LINK_DOMEN_LODKI="https://саратов.хищник.рф/catalog/lodki-i-motory/naduvnye-lodki-pvkh/?PAGEN_1="
LINK_DOMEN_PALATKI1="https://саратов.хищник.рф/catalog/turizm/palatki-i-pologi/palatki-kempingovye/"
LINK_DOMEN_PALATKI2="https://саратов.хищник.рф/catalog/turizm/palatki-i-pologi/palatki-turisticheskie/"
LINK_DOMEN_STULYA="https://саратов.хищник.рф/catalog/turizm/turisticheskaya-mebel/stulya/?PAGEN_1="
LINK_DOMEN_STOLI="https://саратов.хищник.рф/catalog/turizm/turisticheskaya-mebel/stoly/"
LINK_DOMEN_KURTKI="https://саратов.хищник.рф/catalog/odezhda-i-obuv/demisezonnaya-odezhda/kurtki/"
LINK_MODEL_BOTINKI="https://саратов.хищник.рф/catalog/odezhda-i-obuv/obuv/botinki/?PAGEN_1="
LINK_MODEL_SAPOGI1="https://саратов.хищник.рф/catalog/odezhda-i-obuv/obuv/sapogi-zimnie/"
LINK_MODEL_SAPOGI2="https://саратов.хищник.рф/catalog/odezhda-i-obuv/obuv/sapogi-rezinovye/"
LINK_MODEL_SAPOGI3="https://саратов.хищник.рф/catalog/odezhda-i-obuv/obuv/sapogi-zabrodnye/"
LINK_MODEL_FOOTBOLKI="https://саратов.хищник.рф/catalog/odezhda-i-obuv/letnyaya-odezhda/futbolki/?PAGEN_1="

# Основная ссылка на сайт
MAIN_LINK_DOMEN="https://саратов.хищник.рф"

# #получаем готовый Url необходимой страницы для BS4, параметр verify можно отключить, в зависимости от сайта
def getNewUrl(newUrl):
    r=requests.get(newUrl,verify=False)
    return r.text




# парсим каждую страницу
def ParsePage(soup, item_group):
    soup=soup.find('div', class_="catalog_block")
    rawLinks=soup.findAll('a') #Список всех картинок
    for rawLink in rawLinks:
        rawLink_link= rawLink.get('href') 
        picture_link= rawLink.find('img')
        if picture_link is not None:

            # debug MODE:
            #####################################################################
            # count+=1
            # print("\n________________________________________________________")
            # print("\n********************************************************")
            # print(count)
            # print("\n********************************************************")
            # print(rawLink)
            # print("\n********************************************************")
            # print(picture_link)
            # print("\n********************************************************")
             #####################################################################
            pictureLink_title= picture_link.get('title')
            pictureLink_upload_raw=picture_link.get('src')
            pictureLink_upload=MAIN_LINK_DOMEN+pictureLink_upload_raw
            preparedlink=MAIN_LINK_DOMEN+rawLink_link
            preparedLinks.append([item_group,pictureLink_title,preparedlink,pictureLink_upload])
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
    (LINK_DOMEN_UDOCHKI,"Удилища",10),
    (LINK_DOMEN_KATUSHKI,"Катушки",10),
    (LINK_DOMEN_LESKA,"Леска",5),
    (LINK_DOMEN_KOROBKI,"Коробки",5),
    (LINK_DOMEN_YASCHIKI,"Ящики", 2),
    (LINK_DOMEN_NODZI,"Ножи", 5),
    (LINK_DOMEN_MULTITOOLS,"Мультитулы", 3),
    (LINK_DOMEN_MOTORY,"Моторы",2),
    (LINK_DOMEN_LODKI,"Лодки",2),
    (LINK_DOMEN_PALATKI1,"Палатки",0),
    (LINK_DOMEN_PALATKI2,"Палатки",0),
    (LINK_DOMEN_STULYA,"Стулья",2),
    (LINK_DOMEN_STOLI,"Столы",0),
    (LINK_DOMEN_KURTKI,"Куртки",0),
    (LINK_MODEL_BOTINKI,"Ботинки",2),
    (LINK_MODEL_SAPOGI1,"Сапоги",0),
    (LINK_MODEL_SAPOGI2,"Сапоги",0),
    (LINK_MODEL_SAPOGI3,"Сапоги",0),
    (LINK_MODEL_FOOTBOLKI,"Футболки",2)
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

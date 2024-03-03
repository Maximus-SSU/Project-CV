import requests
import json
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #убрать предупреждение  InsecureRequestWarning

# Список всех ссылок на  нужные категории
LINK_CATEGORY_INSTRUMENT_SOKI="https://online.metro-cc.ru/category/bezalkogolnye-napitki/soki-morsy-nektary"
# Основная ссылка на сайт
# LINK_PRODUCT_DOMEN="https://leroymerlin.ru/product/"
# LINK_UPLOAD_DOMEN="https://cdn.leroymerlin.ru/lmru/image/upload/"
MAIN_LINK_DOMEN="https://саратов.хищник.рф"


# #получаем готовый Url необходимой страницы для BS4, параметр verify можно отключить, в зависимости от сайта
def getNewUrl(newUrl):
    r=requests.get(newUrl)
    if r.status_code==200:
        print(f"\nSUCCESS - Status CODE: = {r.status_code}")
        return r.text
    else:
        print(f"\nERROR - Status CODE: = {r.status_code}")
        return r.text



# парсим каждую страницу
def ParsePage(soup, item_group):
    soup=soup.find('div', class_="p135dg85_plp")
    if soup is not None:
        rawLinks=soup.findAll('div',class_="p155f0re_plp largeCard") #Список всех картинок
        for rawLink in rawLinks:
            rawLink=rawLink.find('a')
            rawLink_link= rawLink.get('href') 
            pictureLink_title=rawLink.get('aria-label')
            picture_link= rawLink.find('source', media_= "(min-width: 1200px)")
            # picture_link= picture_link_soup.get('srcset')
            if picture_link is not None:

                # debug MODE:
                #####################################################################
                # count+=1
                print("\n________________________________________________________")
                # print("\n********************************************************")
                # print(count)
                print("\n********************************************************")
                print(rawLink)
                print("\n********************************************************")
                print(picture_link)
                print("\n********************************************************")
                #####################################################################
                pictureLink_upload=picture_link.get('srcset')
                preparedlink=MAIN_LINK_DOMEN+rawLink_link
                preparedLinks.append([item_group,pictureLink_title,preparedlink,pictureLink_upload])
        # rawLinks_length=len(rawLinks)# количество всех ссылок
            # if rawLinks_length==21 :
            #     return True
            # else :
            #     return False
    else:
        print("\nERR: Soup is NONE\n")



#Парсим все
def Parse(startUrl,item_group,max_pages_in_group):
    if max_pages_in_group>0:
        for page_count in range (1,max_pages_in_group+1):
            url=startUrl+str(page_count)
            print("\nTRY SCRAPPING : "+ url+"\n")
            Soup=BeautifulSoup(getNewUrl(url),'lxml')
            ParsePage(Soup,item_group)
            page_count+=1
    else:
        url=startUrl
        print("\nTRY SCRAPPING : "+ url+"\n")
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
    (LINK_CATEGORY_INSTRUMENT_SHURUPOVERTS,"Шуруповерт",0)]

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

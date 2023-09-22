import re
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import argparse
import urllib
import shutil
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json

#获取数据
def get_data(url, file_path, file_name):
    file = file_path + "/" + file_name
    urllib.request.urlretrieve(url, file)

#初始化seleinium web drvier
def init_driver(load_time_num):
    driver = webdriver.Chrome()
    
    #网页不显示自动化工具
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    
    #网站timeout 参数设置
    driver.implicitly_wait(load_time_num)
    return driver

def css_select(driver, url, tag_name):
    driver.get(url)
    driver.find_elements(By.CSS_SELECTOR , tag_name)
        
    return driver.page_source

def delete_subfolders(root_dir):
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"删除子文件夹：{folder_path}")
    
def delete_subfile(folder_path):
    file_list = os.listdir(folder_path)

    # 遍历文件列表，删除所有文件
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"删除下载文件：{file_path}")

def remove_all():
    root_dir_list = [
        "downloads/Intel/", "downloads/Asus/",
        "downloads/ASRock/", "downloads/Dell/",
        "downloads/GigaByte/", "downloads/Lenovo/",
        "downloads/BMC/",
    ]

    print("\nStart to delete files ")
    for root_dir in root_dir_list:
        delete_subfolders(root_dir)
        delete_subfile(root_dir)
    print("finish deleting all files \n")

class Intel:
    resLienList = dict()
    file_path = "downloads/Intel"
    home_url = "https://www.intel.cn/content/www/cn/zh/search.html?ws=text#q=BIOS&first=10&sort=relevancy&layout=table"

    def download_bios():
        """
        下载文件
        """
        Intel.resLienList = Intel.get_liens_list(Intel.home_url)

        for bios_type in Intel.resLienList.keys():
            fileName = Intel.get_file_name(bios_type)
            download_lien = Intel.get_real_lien(bios_type)
            
            print(f"start downloading, file name : {fileName}")
            print(download_lien)
            Intel.get_data_from_lien(download_lien, fileName)
            print(f"finish downloading\n")
        print("the end of downloading for Intel \n")

    def get_real_lien(bios_type):
        """
        通过访问子网站，获取真正的下载链接(mirror)
        """

        # 网站加载与定位方式与主网站相似
        driver = init_driver(20)
        
        if bios_type in Intel.resLienList.keys():
            text = css_select(driver, Intel.resLienList[bios_type], 'dc-page-available-downloads-hero-button')
            soup = BeautifulSoup(text, "html.parser")
            buttons = soup.find_all('button', attrs={"data-modal-id":"2"})
            
            return buttons[0].get("data-href")
        else:
            print("Err : wrong bios model")
        
    def get_data_from_lien(url, file_name):
        get_data(url, Intel.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in Intel.resLienList.keys():
            return bios_type_num + ".cap"
    
    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """
        # init 
        print("start collecting lien for Inter \n\n\n")

        pattern_url = "https://www.intel.cn/content/www/cn/zh/download/" 
        
        # selenium driver init
        driver = init_driver(20)
        text = css_select(driver, url, '.title.component.tabProducts')
        
        # pass to bs4
        soup = BeautifulSoup(text, "html.parser")
        links = soup.find_all('a', attrs={"class":"CoveoResultLink"})
        for link in links:
        #保存数据 key:value    
            if link.get("href") != None and re.match(pattern_url, link.get("href")) != None:
                pattern_type = r"\[[A-Z0-9]+\]"    # 匹配单词 [字母加数字]
                matches = re.findall(pattern_type, link.get("aria-label"))
                if len(matches) == 1:
                    pattern_type = r"[A-Z0-9]+"    # 去掉中括号
                    matches = re.findall(pattern_type, matches[0])
                    lien = link.get("href")
                    print(f"reach file correspond : {lien}")
                    Intel.resLienList.update({matches[0] : lien})
        return Intel.resLienList

    def print_res_list():
        for key in Intel.resLienList.keys():
            print(key)
            print(Intel.resLienList[key])
        print(len(Intel.resLienList))

class ASRock:
    resLienList = dict()
    file_path = "downloads/ASRock"
    home_url = "https://www.asrockind.com/zh-cn/download-center&category_id=35"

    def download_bios():
        """
        下载文件
        """
        ASRock.resLienList = ASRock.get_liens_list(ASRock.home_url)

        for bios_type in ASRock.resLienList.keys():
            fileName = ASRock.get_file_name(bios_type)
            
            print(f"start downloading, file name : {fileName}")
            print(ASRock.resLienList[bios_type])
            ASRock.get_data_from_lien(ASRock.resLienList[bios_type], fileName)
            print(f"finish downloading\n")
        print("the end of downloading for ASRock \n")
        
    def get_data_from_lien(url, file_name):
        get_data(url, ASRock.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in ASRock.resLienList.keys():
            return bios_type_num + ".zip"

    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """
        # init 
        pattern_url = "ftp://asrockchina.com.cn/BIOS/IPC" 
        
        count = 1

        print("start collecting lien for ASRock \n\n\n")
        while count < 3:
            # selenium driver init
            url_new = url + f"&page={count}"
            driver = init_driver(20)
            text = css_select(driver, url_new, 'btns')
            
            # pass to bs4
            soup = BeautifulSoup(text, "html.parser")
            links = soup.find_all('a', attrs={"class":"btn"})
            for link in links:
            #保存数据 key:value    
                if link.get("href") != None and re.match(pattern_url, link.get("href")) != None:
                    pattern_type = r"[A-Z0-9]+-[0-9]+\(.*\)"
                    file_name = re.findall(pattern_type, link.get("href"))
                    if len(file_name) == 1:
                        lien =  link.get("href")
                        print(f"reach file correspond : {lien}")
                        file_name[0] = re.sub("\(|\)", "", file_name[0])
                        ASRock.resLienList.update({file_name[0] : lien})
            count += 1
        return ASRock.resLienList
    
    def print_res_list():
        for key in ASRock.resLienList.keys():
            print(key)
            print(ASRock.resLienList[key])
        print(len(ASRock.resLienList))

class GigaByte:
    resLienList = dict()
    file_path = "downloads/GigaByte"
    home_url = "https://www.gigabyte.cn/Support/Utility?p=1&kw=BIOS"

    def download_bios():
        """
        下载文件
        """
        GigaByte.resLienList = GigaByte.get_liens_list(GigaByte.home_url)

        for bios_type in GigaByte.resLienList.keys():
            fileName = GigaByte.get_file_name(bios_type)
            download_lien = GigaByte.resLienList[bios_type]
            
            print(f"start downloading, file name : {fileName}")
            GigaByte.get_data_from_lien(download_lien, fileName)
            print(f"finish downloading\n")
        print("the end of downloading for GigaByte \n")
        
    def get_data_from_lien(url, file_name):
        get_data(url, GigaByte.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in GigaByte.resLienList.keys():
            return bios_type_num + ".zip"
    
    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """
        # init 
        print("start collecting lien for GigaByte \n\n\n")

        pattern_url = "https://download.gigabyte.cn/FileList/Utility/mb_utility_atbios" 
        
        # selenium driver init
        driver = init_driver(20)
        text = css_select(driver, url, 'hq-site')
        
        # pass to bs4
        soup = BeautifulSoup(text, "html.parser")
        links = soup.find_all('a', attrs={"title":"下载"})
        count = 1
        for link in links:
        #保存数据 key:value    
            if link.get("href") != None and re.match(pattern_url, link.get("href")) != None:
                lien = link.get("href")
                file_name = "gigabyte_bios_" + str(count).zfill(5)
                GigaByte.resLienList.update({file_name : lien})
                print(f"reach file correspond : {lien}")
            count += 1
        return GigaByte.resLienList

    def print_res_list():
        for key in GigaByte.resLienList.keys():
            print(key)
            print(GigaByte.resLienList[key])
        print(len(GigaByte.resLienList))

class Asus:
    resLienList = dict()
    file_path = "downloads/Asus"
    home_url = "https://www.asus.com.cn/support/api/product.asmx/GetPDLevel"
    # 列表 : 存储需要下载的目标型号
    typeId_list = ["1618", "1464", "4390", "4005", "2696", "155"]
    header = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    maxNum = 20

    def download_bios():
        """
        下载文件
        """
        Asus.resLienList = Asus.get_liens_list(Asus.home_url)

        for bios_type in Asus.resLienList.keys():
            fileName = Asus.get_file_name(bios_type)
            download_lien = Asus.get_real_lien(bios_type)
            
            print(f"start downloading, file name : {fileName}")
            if download_lien != None:
                Asus.get_data_from_lien(download_lien, fileName)
            print(f"finish downloading\n")
        print("the end of downloading for Asus \n")
        
    def get_data_from_lien(url, file_name):
        get_data(url, Asus.file_path, file_name)

    def get_real_lien(bios_type):
        """
        通过访问子网站，获取真正的下载链接(mirror)
        """

        # 网站加载与定位方式与主网站相似
        driver = init_driver(20)
        
        if bios_type in Asus.resLienList.keys():
            text = css_select(driver, Asus.resLienList[bios_type], 'ProductSupportDriverBIOS__contentRight__31-1X')
            soup = BeautifulSoup(text, "html.parser")
            buttons = soup.find_all('a', attrs={"class":"SolidButton__normal__3XdQd SolidButton__btn__1NmTw"})
            if len(buttons) >= 1:
                return buttons[0].get("href")
            else: 
                return None
        else:
            print("Err : wrong bios model")
        
    def get_file_name(bios_type_num):
        if bios_type_num in Asus.resLienList.keys():
            bios_type_num = re.sub(" ", "_", bios_type_num)
            return bios_type_num + ".zip"
    
    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        1. 从typeId开始请求数据 -> 获得产品系列 -> 获得产品型号
        2. 根据型号再次请求获得下载地址
        3. 储存至resLienList
        """
        # init 
        print("start collecting lien for Asus \n\n\n") 

        # 获得产品系列
        product_serie = []
        for typeId in Asus.typeId_list:
            # param for request lien 
            param1 ={
                "website" : "cn",
                "type" : "1",
                "typeid" : typeId,
                "productflag" : "0",
            }
            reponse1 = requests.get(url=url, params=param1, headers=Asus.header)
            jsonDate1 = reponse1.json() # type == <class 'dict'>

            # parse json data 
            itemList = jsonDate1["Result"]["ProductLevel"]["Products"]["Items"]
            for item in itemList:
                product_serie.append(item["Id"])
        
        # 获得产品型号        
        info_model_list = []
        for productId in product_serie:
            # param for request lien 
            param2 ={
                "website" : "cn",
                "type" : "2",
                "typeid" : productId,
                "productflag" : "1",
            }
            reponse2 = requests.get(url=url, params=param2, headers=Asus.header)
            jsonDate2 = reponse2.json() # type == <class 'dict'>

            # parse json data 
            itemList = jsonDate2["Result"]["Product"]
            for item in itemList:
                info_model_list.append(item)
        
        # 根据型号再次请求获得下载地址
        random_list = []
        count = 0
        while count < Asus.maxNum:
            while 1:
                random_num = random.randint(0, len(info_model_list) - 1)
                if random_num not in random_list:
                    random_list.append(random_num)
                    break
            
            info_model = info_model_list[random_num]
            # param for request lien 
            param3 ={
                "website" : "cn",
                "pdid" : info_model["PDId"],
                "pdhashedid" : info_model["PDHashedId"],
                "model" : info_model["PDName"]
            }
            reponse3 = requests.get("https://www.asus.com.cn/support/api/product.asmx/GetPDSupportTab", params=param3, headers=Asus.header)
            jsonDate3 = reponse3.json() # type == <class 'dict'>

            
            # parse json data 
            if jsonDate3["Result"] != None:
                if len(jsonDate3["Result"]["Obj"][0]["Items"]) >= 2:
                    download_lien = jsonDate3["Result"]["Obj"][0]["Items"][1]["Url"]
                    key = info_model["PDName"]
                    if re.match("https://www.asus.com.cn/supportonly/", download_lien):
                        print(f"reach file correspond : {download_lien}")
                        Asus.resLienList.update({key : download_lien})
                        count += 1
            
        return Asus.resLienList
    
    def print_res_list():
        for key in Asus.resLienList.keys():
            print(key)
            print(Asus.resLienList[key])
        print(len(Asus.resLienList))

class Lenovo:
    resLienList = dict()
    file_path = "downloads/Lenovo"
    home_url = "http://www.smxdiy.com/thread-3220-1-1.html"
    header = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    def download_bios():
        """
        下载文件
        """
        Lenovo.resLienList = Lenovo.get_liens_list(Lenovo.home_url)

        for bios_type in Lenovo.resLienList.keys():
            # print(bios_type in Lenovo.resLienList.keys())
            fileName = Lenovo.get_file_name(bios_type)
            download_lien = Lenovo.get_real_lien(bios_type)
            
            if download_lien != None:
                print(f"start downloading, file name : {fileName}")
                print(fileName)
                # Lenovo.get_data_from_lien(download_lien, fileName)
                print(f"finish downloading\n")
            
        print("the end of downloading for Lenovo \n")

    def get_real_lien(bios_type):
        """
        通过访问子网站，获取真正的下载链接(mirror)
        """

        # 网站加载与定位方式与主网站相似
        driver = init_driver(20)
        if bios_type in Lenovo.resLienList.keys():
            text = css_select(driver, Lenovo.resLienList[bios_type], 'table-downloads-button')
            soup = BeautifulSoup(text, "html.parser")
            buttons = soup.find_all('a', attrs={"class":"table-downloads-button"})
            for button in buttons:
                string = button.get("href")
                if string.endswith('.iso'):
                    return string
            else:
                return None
        else:
            print("Err : wrong bios model")
            return None
        
    def get_data_from_lien(url, file_name):
        get_data(url, Lenovo.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in Lenovo.resLienList.keys():
            bios_type_num = re.sub(" ", "_", bios_type_num)
            bios_type_num = re.sub(r"\(", "", bios_type_num)
            bios_type_num = re.sub(r"\)", "", bios_type_num)
            return bios_type_num + ".iso"
    
    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """
        # init 
        print("start collecting lien for Lenovo \n\n\n")

        # request for url , method : get
        response = requests.get(url = url, headers = Lenovo.header)
        
        # pass to bs4
        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.find_all('tr')
        for tr in trs:
            # html 结构：
            # <tr>
            #   <td> product </td>
            #   <td> version </td>
            #   <td> 链接 </td>
            # </tr>
            td_tags = tr.find_all('td')
            # 判断是否存在该标签
            if len(td_tags) >= 3 and tr.td.div != None:
                text = re.match("ThinkStation", tr.td.div.text)

                if text and td_tags[2].div.font.font.a != None:
                    file_name = text.string
                    file_url = td_tags[2].div.font.font.a.get('href')
                    # 存储数据
                    Lenovo.resLienList.update({file_name:file_url})
                    print(f"reach file correspond : {file_url}")  
                    time.sleep(1)
        return Lenovo.resLienList

    def print_res_list():
        for key in Lenovo.resLienList.keys():
            print(key)
            print(Lenovo.resLienList[key])
        print(len(Lenovo.resLienList))

class Dell:
    resLienList = dict()
    file_path = "downloads/Dell"
    home_url = "https://www.dell.com/support/home/zh-cn/drivers/driversdetails?driverid=0mhfx"
    header = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    maxDownloadNum = 10

    def download_bios():
        """
        下载文件
        """
        Dell.resLienList = Dell.get_liens_list()

        for bios_type in Dell.resLienList.keys():
            # print(bios_type in Lenovo.resLienList.keys())
            fileName = Dell.get_file_name(bios_type)
            download_lien = Dell.get_real_lien(bios_type)
            
            if download_lien != None:
                print(f"start downloading, file name : {fileName}")
                print(download_lien)
                Dell.get_data_from_lien(download_lien, fileName)
                print(f"finish downloading\n")
        print("the end of downloading for Dell \n")

    def get_real_lien(bios_type):
        """
        通过访问子网站，获取真正的下载链接(mirror)
        """

        # 网站加载与定位方式与主网站相似
        driver = init_driver(20)
        if bios_type in Dell.resLienList.keys():
            text = css_select(driver, Dell.resLienList[bios_type], 'download-button.default-cursor.text-nowrap')
            soup = BeautifulSoup(text, "html.parser")
            liens = soup.find_all('a')
        
            for lien in liens:
                if lien.text == "下载" and "BIOS" in lien.get("aria-label").split():
                    # print(lien.get("aria-label"))
                    return lien.get("href")
            
        else:
            print("Err : wrong bios model")
            return None
        
    def get_data_from_lien(url, file_name):
        get_data(url, Dell.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in Dell.resLienList.keys():
            return bios_type_num + ".exe"
    
    def add_to_list(file_name, file_url):
        Dell.resLienList.update({file_name: file_url})
        time.sleep(1)

    def get_liens_list():
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """

        # init 
        print("start collecting lien for Dell \n\n\n")

        file_data_list = {
            "G5_5090" : "https://www.dell.com/support/home/zh-cn/product-support/product/g-series-5090-desktop/drivers",
            "XPS_18_1810" : "https://www.dell.com/support/home/zh-cn/product-support/product/xps-18-1810/drivers",
            "G15_5515_Ryzen" : "https://www.dell.com/support/home/zh-cn/product-support/product/g-series-15-5515-laptop/drivers",
            "G5_5530" : "https://www.dell.com/support/home/zh-cn/product-support/product/g-series-15-5530-laptop/drivers",
            "G3_15_3500" : "https://www.dell.com/support/home/zh-cn/product-support/product/g-series-15-3500-laptop/drivers",
            "Chromebox_3010" : "https://www.dell.com/support/home/zh-cn/product-support/product/chromebox-3010/drivers",
            "ChengMing_3967" : "https://www.dell.com/support/home/zh-cn/product-support/product/chengming-3967-desktop/drivers",
            "Inspiron_16_7610" : "https://www.dell.com/support/home/zh-cn/product-support/product/inspiron-16-7610-laptop/drivers",
            "Surface_Pro_4" : "https://www.dell.com/support/home/zh-cn/product-support/product/surface-pro-4-tablet/drivers",
            "Mobile_Steak_10_Pro" : "https://www.dell.com/support/home/zh-cn/product-support/product/mobile-streak-10-pro/drivers",
        }

        for file_name in file_data_list.keys():
            lien = file_data_list[file_name]
            Dell.add_to_list(file_name, lien)
            print(f"reach file correspond : {lien}")
        
        return Dell.resLienList

    def print_res_list():
        for key in Dell.resLienList.keys():
            print(key)
            print(Dell.resLienList[key])
        print(len(Dell.resLienList))

class BMC:
    resLienList = dict()
    file_path = "downloads/BMC"
    home_url = "https://www.dell.com/support/kbdoc/zh-cn/000178115/idrac9-%E7%89%88%E6%9C%AC-%E5%92%8C-%E5%8F%91%E8%A1%8C-%E8%AF%B4%E6%98%8E"
    header = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    def download_bmc():
        """
        下载文件
        """
        BMC.resLienList = BMC.get_liens_list(BMC.home_url)

        for bios_type in BMC.resLienList.keys():
            # print(bios_type in Lenovo.resLienList.keys())
            fileName = BMC.get_file_name(bios_type)
            download_lien = BMC.get_real_lien(bios_type)
            
            if download_lien != None:
                print(f"start downloading, file name : {fileName}")
                # print(download_lien)
                BMC.get_data_from_lien(download_lien, fileName)
                print(f"finish downloading\n")
            
        print("the end of downloading for Lenovo \n")

    def get_real_lien(bmc_type):
        """
        通过访问子网站，获取真正的下载链接(mirror)
        """

        # 网站加载与定位方式与主网站相似
        if bmc_type in BMC.resLienList.keys():
            response = requests.get(url=BMC.resLienList[bmc_type], headers=BMC.header)
            soup = BeautifulSoup(response.text, "html.parser")
            # html 结构
            # <div class="my-5 container">
            #   <div class="row"> 
            #       <span> 文件格式:</span>
            #       <span> </span>
            #   </div>
            #   <div class="row"> </div>
            #   <div class="row"> </div>
            #   <div class="row"> </div>
            #   <div class="row"> 
            #       <div> </div>
            #       <div> <span> <a href="xxxx"> </span> </div>
            #   <div>
            # </div>
            divs = soup.find_all('div', attrs={"class": "my-5 container"})
            for div in divs:
                if div.div.find_all('span')[1].text == "MS Windows（64位）的更新包。":
                    lien = div.find_all('div')[4].find_all('div')[1].span.a.get("href")
                    return lien
        else:
            print("Err : wrong bios model")
        
        return None
        
    def get_data_from_lien(url, file_name):
        get_data(url, BMC.file_path, file_name)

    def get_file_name(bios_type_num):
        if bios_type_num in BMC.resLienList.keys():
            bios_type_num = re.sub(r"\.", "_", bios_type_num)
            return bios_type_num + ".EXE"
    
    def get_liens_list(url):
        """
        从主网站(url)爬取数据
        通过selenium定位对应的tag,将获取的子网站链接储存至resLienList:
            key是bios型号, value是文件链接
        """
        # init 
        print("start collecting BMC lien from Dell \n\n\n")

        # request for url , method : get
        response = requests.get(url = url, headers = BMC.header)
        
        # pass to bs4
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all('table')
        for table in tables:
            # html 结构：
            # <table>
            #   <thead> 
            #       <tr>
            #           <th> iDRAC9 版本下载</th>
            #           <th> 发布日期</th>
            #           <th> 优先级</th>
            #           <th> 发行说明</th>
            #           <th> 文档</th>
            #       </tr>
            #   </thead>
            #   <tbody> lien </tbody>
            # </table>
            tr_label = table.thead.tr
            ths = tr_label.find_all('th')
            
            # 判断是否存在该标签
            if len(ths) == 5 and ths[0].text == "iDRAC9 版本下载":
                tbody = table.tbody 
                trs = tbody.find_all('tr')
                for tr in trs:
                    file_name = tr.td.a.text
                    file_url = tr.td.a.get("href")
                    # 存储数据
                    print(f"reach file correspond : {file_url}")  
                    BMC.resLienList.update({file_name: file_url})
                    # time.sleep(1)
        return BMC.resLienList

    def print_res_list():
        for key in BMC.resLienList.keys():
            print(key)
            print(BMC.resLienList[key])
        print(len(BMC.resLienList))

def get_fake_ua(browser_type):
    list_browser_type = {
        "chrome" : "chrome", "Chrome" : "chrome", "CHROME" : "chrome",
        "IE" : "IE", "Ie" : "IE", "ie" : "IE", 
        "Edge" : "Edge", "EDGE" : "Edge", "edge" : "Edge", 
        "Safari" : "Safari", "SAFARI" : "Safari", "safari" : "Safari", 
        "FireFox" : "FireFox", "FIREFOX" : "FireFox", "FIREFox" : "FireFox", "FireFOX" : "FireFox",
        "fireFOX" : "FireFox", "FIREfox" : "FireFox", "firefox" : "FireFox", 
        "Opera" : "Opera", "OPERA" : "Opera", "opera" : "Opera", 
    }

    if browser_type in list_browser_type.keys():
        ua = UserAgent()
        if list_browser_type[browser_type] == "chorme":
            ua.chrome
        if list_browser_type[browser_type] == "IE":
            ua.ie
        if list_browser_type[browser_type] == "Edge":
            ua.edge
        if list_browser_type[browser_type] == "Safari":
            ua.safari
        if list_browser_type[browser_type] == "FireFox":
            ua.firefox
        if list_browser_type[browser_type] == "Opera":
            ua.opera
        return ua
    else:
        print("Err : wrong type of browser ")

if __name__=='__main__':
    # download by the order of :
    # 1. Inter
    # 2. Dell
    # 3. ASRock
    # 4. Lenovo
    # 5. Asus
    # 6. GigaByte

    craber_option = argparse.ArgumentParser(
        description = "download bios/uefi firmware from Intel, ASRock, Asus, GigaByte, Lenovo, Dell")
    craber_option.add_argument(
        '-i', "--Intel", default=False, action="store_true",
        help='The input is to download bios/uefi for Intel.')
    craber_option.add_argument(
        '-ar', "--ASRock", default=False, action="store_true",
        help='The input is to download bios/uefi for ASRock.')
    craber_option.add_argument(
        '-a', "--Asus", default=False, action="store_true",
        help='The input is to download bios/uefi for Asus.')
    craber_option.add_argument(
        '-gb', "--GigaByte", default=False, action="store_true",
        help='The input is to download bios/uefi for GigaByte.')
    craber_option.add_argument(
        '-l', "--Lenovo", default=False, action="store_true",
        help='The input is to download bios/uefi for Lenovo.')
    craber_option.add_argument(
        '-d', "--Dell", default=False, action="store_true",
        help='The input is to download bios/uefi for Dell.')
    craber_option.add_argument(
        '-b', "--BMC", default=False, action="store_true",
        help='The input is to download BMC firmware from Dell.')
    craber_option.add_argument(
        '-A', "--ALL", default=False, action="store_true",
        help='The input is to download all bios/uefi that we mention above.')
    craber_option.add_argument(
        '-c', "--clean", default=False, action="store_true",
        help='Clean the file.')
    
    args = craber_option.parse_args()

    if args.ALL:
        args.Intel = True
        args.ASRock = True
        args.Asus = True
        args.GigaByte = True
        args.Lenovo = True
        args.Dell = True
        args.BMC = True

    # 首先清空文件夹
    if args.Intel or args.ASRock or args.Asus or args.GigaByte or args.Lenovo or args.Dell or args.BMC:
        args.clean = True
    
    if args.clean:
       remove_all()

    # 爬虫部分执行  
    if args.Intel:
        Intel.download_bios()
    if args.ASRock:
        ASRock.download_bios()
    if args.Asus:
        Asus.download_bios()
    if args.GigaByte:
        GigaByte.download_bios()
    if args.Lenovo:
        Lenovo.download_bios()
    if args.Dell:
        Dell.download_bios()
    if args.BMC:
        BMC.download_bmc()

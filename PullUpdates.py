import json 
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver(headless=False):
    # support to get response status and headers
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument("--disable-xss-auditor")
    opt.add_argument("--disable-web-security")
    opt.add_argument("--allow-running-insecure-content")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-setuid-sandbox")
    opt.add_argument("--disable-webgl")
    opt.add_argument("--disable-popup-blocking")
    opt.add_argument("--disable-notifications")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    #opt.binary_location = "./chromedriver.exe"
    # prefs = {"profile.managed_default_content_settings.images": 2,
    #          'notifications': 2,
    #          }
    # opt.add_experimental_option("prefs", prefs)
    ChromeDriverManager().install()
    browser = webdriver.Chrome(options=opt,desired_capabilities=d,service=Service(ChromeDriverManager().install()))
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(20)
    return browser 

def get_chapter_from_web_text(web_text):
    split_string = re.split(':| |\n',web_text)
    for index, word in enumerate(split_string):
        #print (word)
        if word.lower() == "chapter" and index < len(split_string):
            #print(split_string[index], split_string[index+1])
            chapter_num = split_string[index+1]
            if chapter_num.isdigit():
                return int(chapter_num)
            else:
                return float(chapter_num)
    return -1


chromeDriver = get_chrome_driver(headless=True)

  
# get all anchor elements

def get_latest_chapter(url):
    chromeDriver.get(url)
    chromeDriver.refresh()
    chromeDriver.implicitly_wait(5)
    all_anchor_elements = chromeDriver.find_elements(By.TAG_NAME,'a')

    # find the latest chapters among the first 4 anchor elements that contain chapter in its text
    max_chapter = 0
    max_chapter_link = "N/A"
    count = 0
    for element in all_anchor_elements:
        lowered_text = element.text.lower()
        if lowered_text.__contains__('chapter') and count < 2:
            if element.text is not None: 
                chapter = get_chapter_from_web_text(element.text)
                if (chapter > max_chapter):
                    max_chapter = chapter
                    max_chapter_link = element.get_attribute('href')
            count += 1
    print ("============== ",max_chapter, max_chapter_link)
    return (max_chapter, max_chapter_link)

def get_all_chapters(url):
    
    chromeDriver.get(url)
    all_anchor_elements = chromeDriver.find_elements(By.TAG_NAME,'a')

    for element in all_anchor_elements:
        lowered_text = element.text.lower()
        if lowered_text.__contains__('chapter'):
            print(element.get_attribute("class"))
            print(element.get_attribute('outerHTML'))


update_file = open('update.json')

# 
update_data = json.load(update_file)

for comic in update_data:
    comic_url = update_data[comic]['url']
    print ("Getting latest chapter for ",comic)
    latest_chapter, chapter_link = get_latest_chapter(comic_url)
    
    # if the json file doesn't have a latest chapter, set to 1
    if update_data[comic].get('latest chapter') is None: 
        update_data[comic]['latest chapter'] = 1
        continue
    # if the latest chapter is not newer than the current chapter
    if update_data[comic]['latest chapter'] >= latest_chapter: continue
    # if there is no link, continue
    if chapter_link is None: continue

    print ("Setting latest chapter to",latest_chapter,chapter_link)
    update_data[comic]['latest chapter'] = latest_chapter
    update_data[comic]['chapter link'] = chapter_link
        
    
    #print(comic + " has url " + comic_url)

# update the entire list with the latest chapter
with open("update.json", "w") as data_file:
    json.dump(update_data, data_file, indent=2)

# closing the driver
chromeDriver.close()
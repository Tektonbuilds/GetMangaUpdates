import json 

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


chromeDriver = get_chrome_driver(headless=True)

chromeDriver.get("https://onepiecechapters.com/mangas/13/chainsaw-man")
  
# printing the content of entire page
all_list_elements = chromeDriver.find_elements(By.TAG_NAME,'a')
#print (all_list_elements)

for element in all_list_elements:
    lowered_text = element.text.lower()
    if lowered_text.__contains__('chapter'):
        print("==================================================")
        link = element.get_attribute('href')
        print(element.text)
        if link is not None:
            print(link)

def get_latest_chapter(url):
    return 10

update_file = open('update.json')

# 
update_data = json.load(update_file)

for comic in update_data:
    comic_url = update_data[comic]['url']
    latest_chapter = get_latest_chapter(comic_url)
    # if the current chapter is older
    if update_data[comic].get('latest chapter') is not None and update_data[comic]['latest chapter'] < latest_chapter:
       update_data[comic]['latest chapter'] = latest_chapter
    else:
        update_data[comic]['latest chapter'] = latest_chapter
    
    #print(comic + " has url " + comic_url)

# update the entire list with the latest chapter
with open("update.json", "w") as data_file:
    json.dump(update_data, data_file, indent=2)
# closing the driver
#chromeDriver.close()
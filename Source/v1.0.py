import urllib, urllib.request
import requests
import shutil
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from UserClass import UserInfo, PostDownload

#res.status_code == requests.codes.ok/200

'''The code written in here is the firt version of the
    Instagram Image Downloader (InstaLoad) app.'''

def get_username():
    url = 'https://www.instagram.com/'
    username = str(input('Enter username: @'))
    userpage = url + username + '/'

    return username, userpage

def open_userpage(userpage):
    driver = webdriver.PhantomJS(executable_path = r'C:\Users\Wahhaj\AppData\Roaming\npm\node_modules\phantomjs-prebuilt\lib\phantom\bin\phantomjs')
    #driver = webdriver.Chrome(executable_path = r'C:\Users\Wahhaj\AppData\Local\Programs\Python\Python35\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')
    driver.get(userpage)
    driver.set_window_size(1920, 1200)
    time.sleep(3)
    element = driver.find_element_by_xpath('/html/body')
    element.send_keys(Keys.END)
    time.sleep(3)
    driver.find_element_by_link_text('Load more').click()
    
    return driver

def scroll_to_end(driver):
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    holder = []
    for span in soup.findAll('span', {'class':'_bkw5z'}):
        posts = span.text
        holder.append(posts)

    posts = holder[0].replace(',', '')    
    hrefs = get_image_links(soup)

    
    while len(hrefs) < int(posts):
        element = driver.find_element_by_xpath('/html/body')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #element.send_keys(Keys.END)
        time.sleep(3)
        soup_1 = BeautifulSoup(driver.page_source, 'lxml')
        time.sleep(2)
        hrefs = get_image_links(soup_1)

    return hrefs

def get_image_links(soup):
    
    hrefs = []
    for a in soup.findAll('a'):
        href = a.get('href')
        if href.startswith('/p/'):
            hrefs.append(href)

    return hrefs     

def get_url(hrefs, driver):

    img_links = []
    vid_links = []
    url = 'https://www.instagram.com'
    for href in hrefs:
        post_url = url + href
        driver.get(post_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        album_check = soup.findAll('a', {'class':'_90kqf _qwk2e coreSpriteRightChevron'})

        if album_check:
            for img in soup.findAll('img', {'class':'_icyx7'}):
                img_link = img.get('src')
                img_links.append(img_link)

            for vid in soup.findAll('video', {'class':'_c8hkj'}):
                vid_link = vid.get('src')
                vid_links.append(vid_link)
            
            while album_check:
                print('In album loop')
                driver.find_element_by_css_selector('._90kqf._qwk2e.coreSpriteRightChevron').click()
                time.sleep(5)
                soup_2 = BeautifulSoup(driver.page_source, 'lxml')
                time.sleep(2)
                
                for img in soup_2.findAll('img', {'class':'_icyx7'}):
                    img_link = img.get('src')
                    img_links.append(img_link)

                for vid in soup_2.findAll('video', {'class':'_c8hkj'}):
                    vid_link = vid.get('src')
                    vid_links.append(vid_link)
                    
                album_check = soup_2.findAll('a', {'class':'_90kqf _qwk2e coreSpriteRightChevron'})

        else:            
            for img in soup.findAll('img', {'class':'_icyx7'}):
                img_link = img.get('src')
                img_links.append(img_link)

            for vid in soup.findAll('video', {'class':'_c8hkj'}):
                vid_link = vid.get('src')
                vid_links.append(vid_link)

    return img_links, vid_links

def make_file(username):
    path = os.getcwd()
    filename = username
    full_path = os.path.join(path, filename)
    os.mkdir(full_path)

def make_cat_file(username):
    path = os.getcwd() + '\\' + username
    image_file = 'Images'
    video_file = 'Videos'
    video = os.path.join(path, video_file)    
    image = os.path.join(path, image_file)
    os.mkdir(image)
    os.mkdir(video)

def save_images(username, img_links):
    
    num_list = list(range(1,len(img_links)+1))
    num_list = [str(x) for x in num_list]
    for x,y in zip(img_links, num_list):
        filename = y
        path = os.getcwd() + '\\' + username + '\\Images\\'
        fullpath = os.path.join(path, filename) + '.jpg'
        urllib.request.urlretrieve(x, fullpath)
    
def save_videos(username, vid_links):
    
    num_list = list(range(1,len(vid_links)+1))
    num_list = [str(x) for x in num_list]
    for x,y in zip(vid_links, num_list):
        filename = y
        path = os.getcwd() + '\\' + username + '\\Videos\\'
        fullpath = os.path.join(path, filename) + '.mp4'
        #urllib.request.urlretrieve(x, fullpath)
        #urllib.request.FancyURLopener().retrieve(x, fullpath)
        r = requests.get(x, stream=True)
        with open(fullpath, 'wb') as f_obj:
            shutil.copyfileobj(r.raw, f_obj)

def main():             
    username, userpage = get_username()
    account = UserInfo(username, userpage)
    driver = account.open_userpage(userpage)
    hrefs = account.scroll_to_end(driver)
    img_links, vid_links = account.get_url(hrefs, driver)
    download = PostDownload(username, img_links, vid_links)
    download.make_file(username)
    download.make_cat_file(username)
    download.save_images(username, img_links)
    download.save_videos(username, vid_links)


if __name__ == '__main__':
    main()

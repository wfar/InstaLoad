import sys
import urllib, urllib.request
import requests
import shutil
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Scraper():
    ''' Class for connecting and scraping all Instagram account information.

        The class is initialized using @staticmethods.

        Parameters:
            username is the profile account name.
            userpage is direct url to profile account.
            driver is active PhantomJS window used to automate scraping proces.

        hrefs, img_links, and vid_links are lists used to contain scraped information.
        '''
    
    def __init__(self, username, userpage, driver):
        
        self.username = username
        self.userpage = userpage
        self.driver = driver
        self.hrefs = []
        self.img_links = []
        self.vid_links = []

    def open_userpage(self):
        '''Gets profile, sets window size, and clicks "Load more" button.'''
        
        self.driver.get(self.userpage)
        self.driver.set_window_size(1920, 1200)
        time.sleep(3)
        check_point_1 = self.check_page()
        if check_point_1:
            element = self.driver.find_element_by_xpath('/html/body')
            element.send_keys(Keys.END)
            time.sleep(3)
            try:
                self.driver.find_element_by_link_text('Load more').click()
            except Exception:
                pass
        else:
            time.sleep(4)
            self.driver.quit()
            sys.exit()
            
    def check_page(self):
        '''Checks to see if the profile is active and not private (if not logged in).'''
        
        soup_3 = BeautifulSoup(self.driver.page_source, 'lxml')
        error_message_1 = "Sorry, this page isn't available."
        error_message_2 = "This Account is Private"
        check_point_1 = True
        for text in soup_3.findAll():
            if error_message_1 in text:
                print('The profile you entered doesnt exist or has been deleted.')
                check_point_1 = False
            elif error_message_2 in text:
                print('This is a private account. If it is your account, please login first or set account to public.')
                check_point_1 = False

        return check_point_1

    def scroll_to_end(self):
        '''Scrapes all image links from profile while scrolling through profile.'''
        
        print('Searching...')
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        holder = []
        for span in soup.findAll('span', {'class':'_bkw5z'}):
            posts = span.text
            holder.append(posts)

        posts = holder[0].replace(',', '')
        self.get_image_links(soup)
        
        if int(posts) > 0:
            while len(self.hrefs) < int(posts):
                element = self.driver.find_element_by_xpath('/html/body')
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                #element.send_keys(Keys.END)    #execute_script works better than send_keys for scrolling.
                time.sleep(3)
                soup_1 = BeautifulSoup(self.driver.page_source, 'lxml')
                time.sleep(2)
                del self.hrefs[:]
                self.get_image_links(soup_1)
        else:
            print('This profile does not have any posts to download.')
            time.sleep(2)
            self.driver.quit()
            sys.exit()

    def get_image_links(self, soup):
        '''Scrapes each post for the image links (hrefs).'''
        
        for a in soup.findAll('a'):
            href = a.get('href')
            if href.startswith('/p/'):
                self.hrefs.append(href)      

    def get_url(self):
        '''Connects to each posts' page and scrapes the image url.'''
        
        url = 'https://www.instagram.com'
        for href in self.hrefs:
            post_url = url + href
            self.driver.get(post_url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            album_check = soup.findAll('a', {'class':'_90kqf _qwk2e coreSpriteRightChevron'})

            if album_check:
                for img in soup.findAll('img', {'class':'_icyx7'}):
                    img_link = img.get('src')
                    self.img_links.append(img_link)

                for vid in soup.findAll('video', {'class':'_c8hkj'}):
                    vid_link = vid.get('src')
                    self.vid_links.append(vid_link)
                
                while album_check:
                    self.driver.find_element_by_css_selector('._90kqf._qwk2e.coreSpriteRightChevron').click()
                    time.sleep(5)
                    soup_2 = BeautifulSoup(self.driver.page_source, 'lxml')
                    time.sleep(2)
                    
                    for img in soup_2.findAll('img', {'class':'_icyx7'}):
                        img_link = img.get('src')
                        self.img_links.append(img_link)

                    for vid in soup_2.findAll('video', {'class':'_c8hkj'}):
                        vid_link = vid.get('src')
                        self.vid_links.append(vid_link)
                        
                    album_check = soup_2.findAll('a', {'class':'_90kqf _qwk2e coreSpriteRightChevron'})

            else:            
                for img in soup.findAll('img', {'class':'_icyx7'}):
                    img_link = img.get('src')
                    self.img_links.append(img_link)

                for vid in soup.findAll('video', {'class':'_c8hkj'}):
                    vid_link = vid.get('src')
                    self.vid_links.append(vid_link)

    def run(self):
        '''Runs the entire profile scrape process.'''
        
        try:
            print('Run start')
            self.open_userpage()
            print('userpage opened')
            self.scroll_to_end()
            print('Scrolled to end')
            self.get_url()
            print('Run completed')
        except Exception:
            print('There was an unknown error in the image scraping process. Please restart and try again.')
            self.driver.quit()
            sys.exit()

    @staticmethod
    def get_username():
        '''Gets username of desired profile and creates proper url.'''
        
        url = 'https://www.instagram.com/'
        username = str(input('Enter the username to download from: @'))
        if len(username) < 1:
            print('You have to enter a valid username in order to continue.')
            time.sleep(2)
            get_username()
        
        userpage = url + username + '/'

        return username, userpage

    @staticmethod
    def get_account_info(driver):
        '''Determines whether user wants to login.'''
        
        answer = input('Do you want to login to your account (y/n)? ')
        logged_in = False
        if answer.lower() == 'y':
            account_name = input('Enter username: ')
            account_password = input('Enter password: ')
            if len(account_name) > 1  and len(account_password) > 1:
                Scraper.account_login(driver, account_name, account_password)
                logged_in = True
            else:
                print('Please enter a valid username and password')
                time.sleep(2)
                Scraper.get_account_info(driver)
        elif answer.lower() == 'n':
            pass
        else:
            print('Invalid response. Please try again.')
            time.sleep(2)
            Scraper.get_account_info(driver)

        return logged_in

    @staticmethod
    def account_login(driver, account_name, account_password):
        '''Logs user into instagram profile.'''
        
        url = 'https://www.instagram.com/accounts/login/'
        driver.get(url)
        time.sleep(2)
        username = driver.find_element_by_name('username')
        username.send_keys(account_name)
        password = driver.find_element_by_name('password')
        password.send_keys(account_password)
        driver.find_element_by_tag_name('button').click()
        time.sleep(2)

        try:
            login_fail = driver.find_element_by_id('slfErrorAlert')
            if login_fail:
                print('Sorry, login failed.')
                time.sleep(1)
                Scraper.get_account_info(driver)
        except Exception:
            print('Login succesful.')

    @staticmethod
    def account_logout(driver):
        '''Logs out of account.'''
        
        logout_url = 'https:www.instagram.com/accounts/logout/'
        driver.get(logout_url)
        time.sleep(3)
    
class Downloader():
    '''Class for compiling all posts and saving to desktop.

        Parameters:
            username is used to create appropriate dir.

            img_links and vid_links contain jpeg and mp4 links
            respectively that are set to be downloaded.

        '''
    
    def __init__(self, username, img_links, vid_links):
        
        self.username = username
        self.img_links = img_links
        self.vid_links = vid_links

    def make_file(self):
        '''Creates new dir of profile username.'''
        
        print('Downloading...')
        path = os.getcwd()
        filename = self.username
        full_path = os.path.join(path, filename)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        else:
            shutil.rmtree(full_path)
            os.mkdir(full_path)

    def make_cat_file(self):
        '''Creates "Images" and "Videos" files within profile dir.'''
        
        path = os.getcwd() + '\\' + self.username
        image_file = 'Images'
        video_file = 'Videos'
        video = os.path.join(path, video_file)    
        image = os.path.join(path, image_file)
        os.mkdir(image)
        os.mkdir(video)

    def save_images(self):
        '''Uses scraped links in self.img_links to download images.'''
        
        num_list = list(range(1,len(self.img_links)+1))
        num_list = [str(x) for x in num_list]
        for x,y in zip(self.img_links, num_list):
            try:
                filename = y
                path = os.getcwd() + '\\' + self.username + '\\Images\\'
                fullpath = os.path.join(path, filename) + '.jpg'
                urllib.request.urlretrieve(x, fullpath)
            except:
                print('Error occurred while downloading this image.\nSource: ' + x)
                continue
        
    def save_videos(self):
        '''Uses scraped links in self.vid_links to download videos.'''
        
        num_list = list(range(1,len(self.vid_links)+1))
        num_list = [str(x) for x in num_list]
        for x,y in zip(self.vid_links, num_list):
            try:
                filename = y
                path = os.getcwd() + '\\' + self.username + '\\Videos\\'
                fullpath = os.path.join(path, filename) + '.mp4'
                #urllib.request.urlretrieve(x, fullpath)    #urllib doesn't work as well as requests for videos.
                r = requests.get(x, stream=True)
                with open(fullpath, 'wb') as f_obj:
                    shutil.copyfileobj(r.raw, f_obj)
            except:
                print('Error occurred while downloading this video.\nSource: ' + x)
                continue

    def run(self):
        '''Runs the entire download process.'''
        
        try:
            self.make_file()
            self.make_cat_file()
            self.save_images()
            self.save_videos()
        except Exception:
            print('There was an unknown error in the image downloading process. Please restart and try again.')
            time.sleep(1)
            sys.exit()

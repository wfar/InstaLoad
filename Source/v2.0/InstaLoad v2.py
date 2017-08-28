import sys
import urllib, urllib.request
import requests
import shutil
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from SDClass import Scraper, Downloader
import config


def main():
    '''Runs InstaLoad application.'''
    
    print('Initializing...')
    
    #Scraping process.
    driver = webdriver.PhantomJS(executable_path = config.pjs_path)
    
    if len(sys.argv) == 2:
    #User does not want to log in to account but entered username arg.
        logged_in = False
        url = 'https://www.instagram.com/'
        username = sys.argv[1]
        userpage = url + username
        print(userpage)
        
    elif len(sys.argv) == 4:
    #User does want to log in to account with all required args.
        logged_in = False
        account_name = sys.argv[2]
        account_password = sys.argv[3]
        if len(account_name) > 1  and len(account_password) > 1:
            Scraper.account_login(driver, account_name, account_password)
            logged_in = True
        else:
            print('Please enter a valid username and password')
            time.sleep(2)
            sys.exit()

        url = 'https://www.instagram.com/'
        username = sys.argv[1]
        userpage = url + username

    else:
    #Runs without command line args, incorrect number of args, or when .exe clicked.
        logged_in = Scraper.get_account_info(driver)
        username, userpage = Scraper.get_username()
        
    scrape = Scraper(username, userpage, driver)
    scrape.run()
    
    if logged_in:
        Scraper.account_logout(driver)
        driver.quit()
    else:
        driver.quit()

    #Downloading process.
    download = Downloader(username, scrape.img_links, scrape.vid_links)
    download.run()
    
    print('Completed.')
    time.sleep(2)
    


if __name__ == '__main__':
    main()




        
        
    


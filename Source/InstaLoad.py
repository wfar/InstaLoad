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




        
        
    


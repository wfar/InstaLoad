import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

''' All functions in this file were added to Scraper class in SDClass.py as @staticmethods.
    The return values for these functions are used to initialize Scraper class.'''


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

def get_account_info(driver):
    '''Determines whether user wants to login.'''
    
    answer = input('Do you want to login to your account (y/n)? ')
    logged_in = False
    if answer.lower() == 'y':
        account_name = input('Enter username: ')
        account_password = input('Enter password: ')
        if len(account_name) > 1  and len(account_password) > 1:
            account_login(driver, account_name, account_password)
            logged_in = True
        else:
            print('Please enter a valid username and password')
            time.sleep(2)
            get_account_info(driver)
    elif answer.lower() == 'n':
        pass
    else:
        print('Invalid response. Please try again.')
        time.sleep(2)
        get_account_info(driver)

    return logged_in

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
            get_account_info(driver)
    except Exception:
        print('Login succesful.')

def account_logout(driver):
    '''Logs user out of their account.'''
    
    logout_url = 'https:www.instagram.com/accounts/logout/'
    driver.get(logout_url)
    time.sleep(3)

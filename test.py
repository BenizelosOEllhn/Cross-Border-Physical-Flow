from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import datetime


URL = 'https://transparency.entsoe.eu/transmission-domain/physicalFlow/show#'
username = 'panospanopoulos5@gmail.com'
password = 'confirmpassword!'

def open_login_page(url):
    # Create webdriver object and open login page
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def login(driver, username, password):
    # Close pop-up and open login form
    close_button = driver.find_element('id', 'close-button')
    close_button.click()
    login = driver.find_element('id', 'login-dialog-visible')
    login.click()

    # Enter login information and submit form
    username_input = driver.find_element('name', 'username')
    password_input = driver.find_element('name', 'password')
    submit_button = driver.find_element('name', 'login')
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()

def choose():
    answer = input("\nDo you want the whole year or a specific date?(For whole year press enter for date write the date like(day.month.year) 03.05.2023)")
    if answer == "":
        return 0
    else: 
        return answer

def get_date(driver, requested_date):
    date_time = datetime.datetime.now() #gets current datetime
    current_date = date_time.strftime("%d.%m.%Y") #formats current datetime (DD.MM.YYYY)
    link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="YEAR" and @exporttype="CSV"]')
    download_url = link_element.get_attribute("href")
    new = download_url.replace(f"{current_date}",f"{requested_date}")
    driver.get(new)

def get_country(driver, number):
    checkbox = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = checkbox.find_element(By.XPATH, '..')
    country = parent_element.find_element(By.XPATH, './/a[@href]')
    hover = ActionChains(driver).move_to_element(country)
    hover.perform()
    country.click()


def download_file(driver, url):
    # Navigate to file download page
    driver.get(url)

    # Prompt user to select a country
    print('1:AL\t2:AT\t3:BE\t4:BA\t5:BG\n6:HR\t7:CZ\t8:DE\t9:EE\t10:FI\n11:FR\t12:GE\t13:DE\t14:GR\t15:HU\n16:IE\t17:IT\t18:XK\t19:LV\t20:LT\n21:LU\t22:MT\t23:MD\t24:ME\t25:NL\n26:MK\t27:NO\t28:PL\t29:PT\t30:RO\n31:RS\t32:SK\t33:SI\t34:ES\t35:SE\n36:CH\t37:TR\t38:UA\t39:UK')
    number = input("Give a number from 1 to 39 for the desired country")

    # Select the desired country and open the download dropdown
    get_country(driver, number)
    answer = choose()
    #If you want whole year 
    if answer == 0:       
        dropdown = driver.find_element('id', 'dv-export-data')
        dropdown.click()
        # Wait for download link to be available and get download link URL
        link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="YEAR" and @exporttype="CSV"]')
        hover = ActionChains(driver).move_to_element(link_element)
        hover.perform()
        link_element.click()
    #For specific date
    else:
        get_date(driver, answer)
        dropdown = driver.find_element('id', 'dv-export-data')
        dropdown.click()
        # Wait for download link to be available and get download link URL
        link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="DEFAULT" and @exporttype="CSV"]')
        hover = ActionChains(driver).move_to_element(link_element)
        hover.perform()
        link_element.click()


def close_driver(driver):
    # Close the driver
    driver.quit()


def main():
    driver = open_login_page(URL)
    login(driver, username, password)
    
    download_file(driver, URL)
    time.sleep(20)
    close_driver(driver)


if __name__ == '__main__':
    main()

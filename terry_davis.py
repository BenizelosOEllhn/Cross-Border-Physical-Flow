from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.action_chains import ActionChains
from os import path
import time
import csv


URL = 'https://transparency.entsoe.eu/transmission-domain/physicalFlow/show#'
username = 'panospanopoulos5@gmail.com'
password = 'confirmpassword!'



def open_login_page(url):
    # Create webdriver object and open login page
    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    # Changing download directory for session to running file  path. Future iterations should include path options
    dir_path = path.dirname(path.realpath(__file__))
    prefs = {'download.default_directory' : dir_path}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
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


def get_country(driver, number):
    checkbox = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = checkbox.find_element(By.XPATH, '..')
    # child_elements = parent_element.find_elements(By.XPATH, "./*")
    # print(parent_element) don't delete
    country = parent_element.find_element(By.XPATH, './/a[@href]')
    hover = ActionChains(driver).move_to_element(country)
    hover.perform()
    country.click()


def download_file(driver, url):
    # Navigate to file download page
    driver.get(url)

    # Prompt user to select a country
    print('1:AL\t2:AT\t3:BE\t4:BA\t5:BG\n6:HR\t7:CZ\t8:DE\t9:EE\t10:FI\n11:FR\t12:GE\t13:DE\t14:GR\t15:HU\n16:IE\t17:IT\t18:XK\t19:LV\t20:LT\n21:LU\t22:MT\t23:MD\t24:ME\t25:NL\n26:MK\t27:NO\t28:PL\t29:PT\t30:RO\n31:RS\t32:SK\t33:SI\t34:ES\t35:SE\n36:CH\t37:TR\t38:UA\t39:UK')
    number = input("Give a number from 1 to 39 for the desired country: ")


    # Select the desired country and open the download dropdown
    get_country(driver, number)
    dropdown = driver.find_element('id', 'dv-export-data')
    dropdown.click()

    # Wait for download link to be available and get download link URL
    element = driver.find_element(By.XPATH, "//div[@class='export-item']//a[@dataitem='ALL' and @timerange='YEAR' and @exporttype='CSV']")
    driver.execute_script("arguments[0].click();", element) #clicking normally doesn't work. asking driver to click using javascript
def get_sum():
    with open("Cross-Border Physical Flow_202301010000-202401010000.csv", newline='') as my_data:
        # Create a CSV reader object
        reader = csv.reader(my_data, delimiter=',')
        next(reader)

        # Create an empty list to store the data
        data = [0,0]
        all_imported_data=[0,0]
        all_exported_data=[0,0]

        # Loop over each row in the CSV file
        for row in reader:
            # Create a dictionary to store the data for this row
            row_data = {}

            # Extract the values from the row and store them in the dictionary
            if  row[1] and row[1]!="N/A" and row[1]!="-":
                row_data['imported'] = int(row[1])
                row_data['exported'] = int(row[2])

            # Add the dictionary to the list of data
                data[0]+=row_data['imported']
                data[1]+=row_data['exported']
                all_imported_data.append(row_data['imported'])
                all_exported_data(row['exported'])
            else:
                continue

        print(f'Imported: {data[0]},Exported :{data[1]}')
        return (data[0],data[1],all_imported_data,all_exported_data)
def get_difference():
    x1,x2=get_sum()
    diff=abs(x1-x2)
    print(diff)
    return diff


def get_extrema():
    pass


def close_driver(driver):
    # Close the driver
    driver.quit()


def main():
    driver = open_login_page(URL)
    login(driver, username, password)
    download_file(driver, URL)
    time.sleep(20)
    close_driver(driver)
    get_sum()
    get_difference()


if __name__ == '__main__':
    main()

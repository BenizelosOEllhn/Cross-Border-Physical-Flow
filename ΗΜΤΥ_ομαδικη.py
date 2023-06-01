from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import csv
import numpy
URL = 'https://transparency.entsoe.eu/transmission-domain/physicalFlow/show#'
username = 'panospanopoulos5@gmail.com'
password = 'confirmpassword!'

def open_login_page(url):
    # Set the path to the directory where the running file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Configure Selenium to use the desired download directory
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': current_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    
    # Create webdriver object and open login page
    driver = webdriver.Chrome(options=chrome_options)
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
    answer = input("\nDo you want the whole year or a specific date?(For whole year press enter for date write the date like(day.month.year) 03.05.2023):")
    if answer == "":
        return 0
    else: 
        return answer

def get_date(driver, requested_date):
    date_time = datetime.datetime.now() #gets current datetime
    current_date = date_time.strftime("%d.%m.%Y") #formats current datetime (DD.MM.YYYY)
    current_url = driver.current_url
    new = current_url.replace(f"{current_date}",f"{requested_date}")
    driver.get(new)

def get_country(driver, number):
    checkbox = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = checkbox.find_element(By.XPATH, '..')
    country = parent_element.find_element(By.XPATH, './/a[@href]')
    hover = ActionChains(driver).move_to_element(country)
    hover.perform()
    country.click()

def get_bdz(driver, number):
    country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = country.find_element(By.XPATH, '..')
    grandparent_element = parent_element.find_element(By.XPATH, '..')
    greatgrandparent_element = grandparent_element.find_element(By.XPATH, '..')
    mparmpas = greatgrandparent_element.find_element(By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
    bdzs = mparmpas.find_elements(By.XPATH, './/div[@class="dv-filter-checkbox"]')
    for bdz in bdzs:
        bdz_link = bdz.find_element(By.XPATH, './/a[@href]')
        hover = ActionChains(driver).move_to_element(bdz_link)
        hover.perform()
        bdz_link.click()
def download_file(driver, url):
    first_time = True
    i = 0
    flag = False
    count=0
    # Navigate to file download page
    driver.get(url)

    # Prompt user to select a country
    print('1:AL\t2:AT\t3:BE\t4:BA\t5:BG\n6:HR\t7:CZ\t8:DE\t9:EE\t10:FI\n11:FR\t12:GE\t13:DE\t14:GR\t15:HU\n16:IE\t17:IT\t18:XK\t19:LV\t20:LT\n21:LU\t22:MT\t23:MD\t24:ME\t25:NL\n26:MK\t27:NO\t28:PL\t29:PT\t30:RO\n31:RS\t32:SK\t33:SI\t34:ES\t35:SE\n36:CH\t37:TR\t38:UA\t39:UK')
    number = input("Give a number from 1 to 39 for the desired country:")

    # Select the desired country and open the download dropdown
    get_country(driver, number)
    answer = choose() 
    country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = country.find_element(By.XPATH, '..')
    grandparent_element = parent_element.find_element(By.XPATH, '..')
    greatgrandparent_element = grandparent_element.find_element(By.XPATH, '..')
    mparmpas = greatgrandparent_element.find_element(By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
    bdzs = mparmpas.find_elements(By.XPATH, './/div[@class="dv-filter-checkbox"]')
    for bdz in bdzs:
        country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
        parent_element = country.find_element(By.XPATH, '..')
        grandparent_element = parent_element.find_element(By.XPATH, '..')
        greatgrandparent_element = grandparent_element.find_element(By.XPATH, '..')
        mparmpas = greatgrandparent_element.find_element(By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
        bdzs = mparmpas.find_elements(By.XPATH, './/div[@class="dv-filter-checkbox"]')
        bdz_link = bdzs[i].find_element(By.XPATH, './/a[@href]') # for special date specialize the class
        bdz_link.click()
        dropdown = driver.find_element('id', 'dv-export-data')
        dropdown.click()
        if answer == 0:
            if flag == True:
                dropdown = driver.find_element('id', 'dv-export-data')
                dropdown.click()
            time.sleep(4)
            link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="YEAR" and @exporttype="CSV"]')         
            hover = ActionChains(driver).move_to_element(link_element)
            hover.perform()
            link_element.click()
            time.sleep(4)
            flag = True
        else:
            if first_time == True:
                get_date(driver, answer)
            dropdown = driver.find_element('id', 'dv-export-data')
            dropdown.click()
            link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="DEFAULT" and @exporttype="CSV"]')
            first_time = False
            time.sleep(1)
            hover = ActionChains(driver).move_to_element(link_element)
            hover.perform()
            link_element.click()
            time.sleep(4)
        count=count+1
        i = i + 1
    return answer,count

def one_day(date, count):
    my_cwd=os.getcwd()
    filenames=os.listdir(my_cwd)
    i=0
    imported_sum=[]
    exported_sum=[]
    imported = []
    exported = []
    my_dict = {"imported": 0, "exported": 0}
    for i in range(count) :
        imported_sum.append(0)
        exported_sum.append(0)
        if ((filenames[i][-1]=='v') and (filenames[i][0]=='C') and (filenames[i][6]=='B')):
            file_name=filenames[i]
            with open(file_name, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    split_data = [s.strip('"') for s in row]
                    if((split_data[1] or split_data[2])!='n/e' and (split_data[1] or split_data[2])!='-' and  (split_data[1] or split_data[2])!='N/A' and  (split_data[1] or split_data[2])!=''):
                        my_dict["imported"] = int(split_data[1])
                        my_dict["exported"] = int(split_data[2])
                        imported_sum[i]+=my_dict["imported"]
                        exported_sum[i]+=my_dict["exported"]
                        imported.append(my_dict["imported"])
                        exported.append(my_dict["exported"])
                    else:
                        continue
        else:
            continue
    

    mean_imp=numpy.mean(imported)
    mean_exp=numpy.mean(exported)
    imp_variance=numpy.var(imported)
    exp_variance=numpy.var(exported)
    imp_deviation=numpy.sqrt(imp_variance)
    exp_deviation=numpy.sqrt(exp_variance)
    max_imported_value=numpy.max(imported)
    min_imported_value=numpy.min(imported)
    max_exported_value=numpy.max(exported)
    min_exported_value=numpy.min(exported)    
    final_imp_list=[mean_imp,imp_deviation,max_imported_value,min_imported_value]
    final_exp_list=[mean_exp,exp_deviation,max_exported_value,min_exported_value]
    
    return imported_sum,exported_sum,final_exp_list,final_imp_list
    
def delete_files(count):
    my_cwd=os.getcwd()
    filenames=os.listdir(my_cwd)
    for i in range(count):
        if(filenames[i][-1]!='y'):
            os.remove(filenames[i])
        else:
            continue
            


    
def close_driver(driver):
    # Close the driver
    driver.quit()

def main():
    driver = open_login_page(URL)
    login(driver, username, password)
    while(1):
        date,count = download_file(driver, URL)
        imported_sum,exported_sum,exported_list,imported_list=one_day(date,count)
        delete_files(count)
        print(imported_sum,exported_sum)
    close_driver(driver)

if __name__ == '__main__':
    main()

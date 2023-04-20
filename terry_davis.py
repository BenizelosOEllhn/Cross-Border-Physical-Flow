from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.action_chains import ActionChains

# Create webdriver object and open login page
driver = webdriver.Chrome()
url = 'https://transparency.entsoe.eu/transmission-domain/physicalFlow/show#'
driver.get(url)

# Close pop-up and open login form
close_button = driver.find_element('id', 'close-button')
close_button.click()
login = driver.find_element('id', 'login-dialog-visible')
login.click()

# Enter login information and submit form
username = 'panospanopoulos5@gmail.com'
password = 'confirmpassword!'
username_input = driver.find_element('name', 'username')
password_input = driver.find_element('name', 'password')
submit_button = driver.find_element('name', 'login')
username_input.send_keys(username)
password_input.send_keys(password)
submit_button.click()


# wait for login to complete and navigate to file download page
driver.get(url)
print('1:AL\t2:AT\t3:BE\t4:BA\t5:BG\n6:HR\t7:CZ\t8:DE\t9:EE\t10:FI\n11:FR\t12:GE\t13:DE\t14:GR\t15:HU\n16:IE\t17:IT\t18:XK\t19:LV\t20:LT\n21:LU\t22:MT\t23:MD\t24:ME\t25:NL\n26:MK\t27:NO\t28:PL\t29:PT\t30:RO\n31:RS\t32:SK\t33:SI\t34:ES\t35:SE\n36:CH\t37:TR\t38:UA\t39:UK')
number = input("Give a number from 1 to 39 for the desired country")
def get_country(number):
    checkbox = driver.find_element(By.XPATH, '//input[@id="{}"]'.format(number))
    parent_element = checkbox.find_element(By.XPATH, '..')
    country = parent_element.find_element(By.XPATH, './/a[@href]')
    print(country)
    hover = ActionChains(driver).move_to_element(country)
    hover.perform()
    country.click()
get_country(number)
dropdown = driver.find_element('id', 'dv-export-data')
dropdown.click()

# Wait for download link to be available and get download link URL
link_element = driver.find_element(By.XPATH, '//a[@dataitem="ALL" and @timerange="YEAR" and @exporttype="CSV"]')
download_url = link_element.get_attribute("href")

# Download the file using requests and save to disk
response = requests.get(download_url)
with open("downloaded_file.csv", "wb") as file:
    file.write(response.content)

# Close the driver
driver.quit()

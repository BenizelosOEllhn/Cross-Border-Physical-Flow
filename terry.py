from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

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

# Wait for login to complete and navigate to file download page
driver.get(url)
driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/show?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime=19.04.2023+00:00|UTC|DAY&border.values=CTY|10YGR-HTSO-----Y!BZN_BZN|10YGR-HTSO-----Y_BZN_BZN|10YAL-KESH-----5&dateTime.timezone=UTC&dateTime.timezone_input=UTC')
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

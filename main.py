from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import csv
import re
import numpy as np

URL = 'https://transparency.entsoe.eu/transmission-domain/physicalFlow/show#'
username = 'panospanopoulos5@gmail.com'
password = 'confirmpassword!'


class Controller:
    def __init__(self, page):
        self.page = page
        self.build()

    def build(self):

        self.resetb = ft.ElevatedButton(text="Reset", on_click=self.reset)
        self.t = ft.Text("Choose country:")
        self.b = ft.ElevatedButton(text="Submit", on_click=self.submit)
        self.dd = ft.Dropdown(
            width=400,
            options=[
                ft.dropdown.Option("1:AL"),
                ft.dropdown.Option("2:AT"),
                ft.dropdown.Option("3:BE"),
                ft.dropdown.Option("4:BA"),
                ft.dropdown.Option("5:BG"),
                ft.dropdown.Option("6:HR"),
                ft.dropdown.Option("7:CZ"),
                ft.dropdown.Option("8:DE"),
                ft.dropdown.Option("9:EE"),
                ft.dropdown.Option("10:FI"),
                ft.dropdown.Option("11:FR"),
                ft.dropdown.Option("12:GE"),
                ft.dropdown.Option("13:DE"),
                ft.dropdown.Option("14:GR"),
                ft.dropdown.Option("15:HU"),
                ft.dropdown.Option("16:IE"),
                ft.dropdown.Option("17:IT"),
                ft.dropdown.Option("18:XK"),
                ft.dropdown.Option("19:LV"),
                ft.dropdown.Option("20:LT"),
                ft.dropdown.Option("21:LU"),
                ft.dropdown.Option("22:MT"),
                ft.dropdown.Option("23:MD"),
                ft.dropdown.Option("24:ME"),
                ft.dropdown.Option("25:NL"),
                ft.dropdown.Option("26:MK"),
                ft.dropdown.Option("27:NO"),
                ft.dropdown.Option("28:PL"),
                ft.dropdown.Option("29:PT"),
                ft.dropdown.Option("30:RO"),
                ft.dropdown.Option("31:RS"),
                ft.dropdown.Option("32:SK"),
                ft.dropdown.Option("33:SI"),
                ft.dropdown.Option("34:ES"),
                ft.dropdown.Option("35:SE"),
                ft.dropdown.Option("36:CH"),
                ft.dropdown.Option("37:TR"),
                ft.dropdown.Option("38:UA"),
                ft.dropdown.Option("39:UK")
            ],
        )

        self.tb = ft.TextField(
            label="Date", hint_text="ex. 03.05.2023. For this year leave blank", width=400
        )
        self.help = [self.t, self.dd, self.tb, self.b]
        self.page.scroll='always'
        self.nav1 = ft.Column(self.help, visible=True, scroll= 'always', wrap=True)
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.add(self.nav1)
        self.page.update()

    def submit(self, e):
        
        prefixes_to_delete = ["csv", "graph"]
        delete_files_starting_with(prefixes_to_delete)

        driver = open_login_page(URL)
        login(driver, username, password)
        download_file(driver, URL, self.dd.value.split(":")[0], self.tb.value)
        close_driver(driver)

        folder_path = os.getcwd()
        # Get all files in the current working directory
        files = os.listdir(folder_path)
        # Search for files that start with "Cross"
        matching_files = [file for file in files if file.startswith("Cross")]
        names = []
        i = 0
        for csv_file in matching_files:
            print(csv_file)
            output_file = 'graph.png'
            with open(csv_file, 'r') as file:
                # Get the first row of the CSV file
                header_row = next(csv.reader(file))
                # Generate output file name
                output_file = f"graph_{header_row[1]}_{header_row[2]}.png"
                name = f"csv_{header_row[1]}_{header_row[2]}.csv"
                names.append(name)
                plot_graph(file, output_file, header_row[1], header_row[2])

                self.help.append(
                    ft.Image(
                        src=f"{sanitize_filename(output_file)}.png",
                        width=750,
                        height=500,
                        fit=ft.ImageFit.FILL,
                        border_radius=ft.border_radius.all(10)
                    )
                )

        for csv_file in matching_files:
            os.rename(csv_file, no_spaces(names[i]))
            i = i + 1

        
        self.page.update()

    def reset(self):
        self.page.controls = []
        self.build()
        self.page.update()


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


def get_date(driver, requested_date):
    date_time = datetime.datetime.now()  # gets current datetime
    # formats current datetime (DD.MM.YYYY)
    current_date = date_time.strftime("%d.%m.%Y")
    current_url = driver.current_url
    new = current_url.replace(f"{current_date}", f"{requested_date}")
    driver.get(new)


def get_country(driver, number):
    checkbox = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = checkbox.find_element(By.XPATH, '..')
    country = parent_element.find_element(By.XPATH, './/a[@href]')
    hover = ActionChains(driver).move_to_element(country)
    hover.perform()
    time.sleep(1)
    country.click()


def get_bdz(driver, number):
    country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = country.find_element(By.XPATH, '..')
    grandparent_element = parent_element.find_element(By.XPATH, '..')
    greatgrandparent_element = grandparent_element.find_element(By.XPATH, '..')
    mparmpas = greatgrandparent_element.find_element(
        By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
    bdzs = mparmpas.find_elements(
        By.XPATH, './/div[@class="dv-filter-checkbox"]')
    for bdz in bdzs:
        bdz_link = bdz.find_element(By.XPATH, './/a[@href]')
        hover = ActionChains(driver).move_to_element(bdz_link)
        hover.perform()
        bdz_link.click()


def download_file(driver, url, countryselector, date):
    first_time = True
    i = 0
    flag = False
    # Navigate to file download page
    driver.get(url)

    # Prompt user to select a country
    number = countryselector

    # Select the desired country and open the download dropdown
    get_country(driver, number)

    answer = date

    country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
    parent_element = country.find_element(By.XPATH, '..')
    grandparent_element = parent_element.find_element(By.XPATH, '..')
    greatgrandparent_element = grandparent_element.find_element(By.XPATH, '..')
    mparmpas = greatgrandparent_element.find_element(
        By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
    bdzs = mparmpas.find_elements(
        By.XPATH, './/div[@class="dv-filter-checkbox"]')
    for bdz in bdzs:
        country = driver.find_element(By.XPATH, f'//input[@id="{number}"]')
        parent_element = country.find_element(By.XPATH, '..')
        grandparent_element = parent_element.find_element(By.XPATH, '..')
        greatgrandparent_element = grandparent_element.find_element(
            By.XPATH, '..')
        mparmpas = greatgrandparent_element.find_element(
            By.XPATH, './/div[@class="dv-sub-filter-hierarchic-wrapper"]')
        bdzs = mparmpas.find_elements(
            By.XPATH, './/div[@class="dv-filter-checkbox"]')
        # for special date specialize the class
        bdz_link = bdzs[i].find_element(By.XPATH, './/a[@href]')
        bdz_link.click()
        dropdown = driver.find_element('id', 'dv-export-data')
        dropdown.click()
        if answer == '':
            if flag == True:
                dropdown = driver.find_element('id', 'dv-export-data')
                dropdown.click()
            time.sleep(4)
            link_element = driver.find_element(
                By.XPATH, '//a[@dataitem="ALL" and @timerange="YEAR" and @exporttype="CSV"]')
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
            link_element = driver.find_element(
                By.XPATH, '//a[@dataitem="ALL" and @timerange="DEFAULT" and @exporttype="CSV"]')
            first_time = False
            time.sleep(1)
            hover = ActionChains(driver).move_to_element(link_element)
            hover.perform()
            link_element.click()
            time.sleep(4)
        i = i + 1


def close_driver(driver):
    # Close the driver
    driver.quit()


def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric or underscore
    sanitized = re.sub(r"[^\w\s-]", "", filename)
    # Replace spaces and hyphens with underscores
    sanitized = re.sub(r"[-\s]+", "_", sanitized)
    return sanitized


def no_spaces(filename):
    sanitized = re.sub(r"[-\s]+", "_", filename)
    modified_name = re.sub(r'[<>:/\\|?*]', '_', sanitized)
    modified_name = modified_name.replace('[', '(').replace(']', ')')
    return modified_name

def delete_files_starting_with(prefixes):
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)

    for file_name in files_in_directory:
        for prefix in prefixes:
            if file_name.startswith(prefix):
                file_path = os.path.join(current_directory, file_name)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

def plot_graph(csv_file, output_file, y1_label, y2_label):
    plt.clf()
    x = []
    y1 = []
    y2 = []

    reader = csv.reader(csv_file)

    for row in reader:
        if (row[1] and row[2] != 'n/e') and (row[1] and row[2] != 'N/A') and (row[1] and row[2] != '-'):
            time_range = row[0]
            # Extract the hour from the time range
            hour = int(time_range.split(" ")[-1].split(":")[0])
            x.append(hour)
            # Convert the second column to integer for orange column
            y1.append(int(row[1]))
            # Convert the third column to integer for purple column
            y2.append(-int(row[2]))

    # Set the width of the bars and the gap between them
    bar_width = 0.75
    gap_width = 0.25
    
    mean_imp = np.mean(y1)
    mean_exp = np.mean(y2)
    meanimp = f"Mean of imports:{mean_imp:.2f}"
    meanexp= f"Mean of exports:{mean_exp:.2f}"
    max_imported_value = np.max(y1)
    min_imported_value = np.min(y1)
    max_y2_value = np.max(y2)
    min_y2_value = np.min(y2)
    max1 = f"Max imported:{max_imported_value:.2f}"
    min2 =  f"Min imported:{min_imported_value:.2f}"
    max11 = f"Min exported:{max_y2_value:.2f}"
    min22 =  f"Max exported:{min_y2_value:.2f}"
    sum_y1 = sum(y1)
    sum_y2 = sum(y2)
    sum_y1_label = f"Imported sum: {sum_y1}"
    sum_y2_label = f"Exported sum: {sum_y2}"
    
    plt.figtext(0.05, 0.95, meanimp, ha='left', va='top', color='black')
    plt.figtext(0.05, 0.03, meanexp, ha='left', va='bottom', color='black')
    plt.figtext(0.5, 0.95, max1, ha='center', va='top', color='black')
    plt.figtext(0.5, 0.03, min2, ha='center', va='bottom', color='black')
    plt.figtext(0.75, 0.95, max11, ha='left', va='top', color='black')
    plt.figtext(0.75, 0.03, min22, ha='left', va='bottom', color='black')
    plt.text(0.95, 0.5, sum_y1_label, ha='right', va='center', transform=plt.gca().transAxes, color='black')
    plt.text(0.95, 0.45, sum_y2_label, ha='right', va='center', transform=plt.gca().transAxes, color='black')
       
    # Shift the x positions for the bars to create gaps between them
    x1 = np.array(x) - (bar_width + gap_width) / 2
    x2 = np.array(x) + (bar_width + gap_width) / 2
    plt.bar(x1, y1, width=bar_width, color='orange', label=y1_label)
    plt.bar(x2, y2, width=bar_width, color='purple', label=y2_label)
    plt.xlabel('Hour')
    plt.ylabel('Value')
    plt.title('CSV Data Graph')
    plt.grid(True)
    plt.legend()
    sanitized_output_file = sanitize_filename(output_file)
    plt.savefig(sanitized_output_file)

def main(page: ft.Page):
    page.title = "Cross Border Physicsl Flows Analysis"
    page.padding = 20
    Controller(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir=os.getcwd())

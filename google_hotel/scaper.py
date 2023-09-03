from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


import time

driver = webdriver.Chrome()
search_result = ''

wait = WebDriverWait(driver, 5)  # Maximum wait time of 10 seconds (adjust as needed)


def launch():
    chrome_driver_path = '/Applications/Google\ Chrome.app'

    # Navigate to the Google Hotels URL
    url = 'https://www.google.com/travel/search?ts=CAESABoAKgIKAA&ved=0CAAQ5JsGahcKEwjAtrPvzYyBAxUAAAAAHQAAAAAQCw&ictx=3'
    driver.get(url)

def update_search_results():
    global search_result
    element = driver.find_element(By.XPATH, '//div[@class="GDEAO"]')
    search_result = element.text
    search_result = re.search(r'\d+', search_result).group()

def wait_for_loading():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'VfPpkd-JGcpL-P1ekSe') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-A9y3zc') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-DMahoc-hxXJme') and @role='progressbar']")))
    wait.until_not(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'VfPpkd-JGcpL-P1ekSe') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-A9y3zc') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-DMahoc-hxXJme') and @role='progressbar']")))

def search(region: str):
    global search_result
    region = region.title()
    # Find the search bar element by its attributes
    search_bar = driver.find_element(By.XPATH, '//input[@placeholder="Search for places, hotels and more"]')

    # Type something into the search bar

    search_bar.clear()
    search_bar.send_keys(region)

    time.sleep(.1)

    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN)
    actions.perform()

    # time.sleep(5)

    element = wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="GDEAO"]'), region))
    update_search_results()

    # time.sleep(5)

def apply_filters():
    apply_star_limit()
    select_date()



def apply_star_limit():
    global search_result
    # try:
        # Find and click the button to apply the 4-5 star filter

    button_element = driver.find_element(By.XPATH, '//button[@aria-label="4- or 5-star, Hotel class, Not selected"]')

        # Click the button element
    button_element.click()

    element = wait.until_not(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="GDEAO"]'), search_result))
    wait_for_loading()
    update_search_results()

    print("4-5 star filter applied successfully.")
    # except Exception as e:
    #     raise(f"Error applying 4-5 star filter: {e}")

def select_date():
    elements = driver.find_elements(By.XPATH, '//button[@jsname="a1ZUMe" and @data-delta="1"]')

    for _ in range (4):
        for element in reversed(elements):
            for _ in range(25):
                element.click()
        wait_for_loading()
        # time.sleep(5)
    
def scrape_current_page(count, total):
    hotel_cards = driver.find_elements(By.XPATH, "//a[@class='PVOOXe']")

    # Create a list to store the hotel names
    hotel_names = []

    # Iterate through the hotel cards and extract the hotel name
    for card in hotel_cards:
        if count == total:
            break
        hotel_name = card.get_attribute("aria-label")
        if hotel_name:
            hotel_names.append(hotel_name)
        count += 1
    return hotel_names

def pull_results():
    total_sites = int(search_result)
    hotel_names = []

    while len(hotel_names) < total_sites:
    # Call the function to scrape the current page
        hotel_names = hotel_names + scrape_current_page(len(hotel_names), total_sites)

        # Check if len(hotel_names) is still less than total_sites
        if len(hotel_names) < total_sites:
            # Find and click the "next" button to load more results
            next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]/ancestor::button")
            next_button.click()            
            time.sleep(3)
        else:
            break

    return hotel_names



if __name__ == '__main__':

    # launch()
    # update_search_results()

    region = 'charleston'
    launch()
    search(region)
    apply_filters()
    hotels = pull_results()

    print('here')
    

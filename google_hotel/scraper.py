from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import config

# from config import testing

import time

class GoogleScraper:
    region: str
    driver: WebDriver
    search_result: str
    wait: WebDriverWait

    def __init__(
        self, 
        region : str, 
        url = 'https://www.google.com/travel/search?ts=CAESABoAKgIKAA&ved=0CAAQ5JsGahcKEwjAtrPvzYyBAxUAAAAAHQAAAAAQCw&ictx=3'
    ):
        self.region = region.title()
        # Navigate to the Google Hotels URL
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 10)

    def quit(self):
        self.driver.quit()


    def update_search_results(self):
        global search_result
        element = self.driver.find_element(By.XPATH, '//div[@class="GDEAO"]')
        search_result = element.text
        search_result = re.search(r'\d+', search_result).group()

    def wait_for_loading(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'VfPpkd-JGcpL-P1ekSe') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-A9y3zc') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-DMahoc-hxXJme') and @role='progressbar']")))
        self.wait.until_not(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'VfPpkd-JGcpL-P1ekSe') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-A9y3zc') and contains(@class, 'VfPpkd-JGcpL-P1ekSe-OWXEXe-DMahoc-hxXJme') and @role='progressbar']")))

    def search(self):
        global search_result
        # Find the search bar element by its attributes
        search_bar = self.driver.find_element(By.XPATH, '//input[@placeholder="Search for places, hotels and more"]')

        # Type something into the search bar

        search_bar.clear()
        search_bar.send_keys(self.region)

        time.sleep(.1)

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN)
        actions.perform()

        time.sleep(5)

        element = self.wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="GDEAO"]'), self.region))
        self.update_search_results()

        # time.sleep(5)

    def apply_filters(self):
        self.apply_star_limit()
        self.select_date()



    def apply_star_limit(self):
        global search_result
        # try:
            # Find and click the button to apply the 4-5 star filter

        button_element = self.driver.find_element(By.XPATH, '//button[@aria-label="4- or 5-star, Hotel class, Not selected"]')

            # Click the button element
        button_element.click()

        element = self.wait.until_not(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="GDEAO"]'), search_result))
        self.wait_for_loading()
        time.sleep(1)
        self.update_search_results()

        print("4-5 star filter applied successfully.")
        # except Exception as e:
        #     raise(f"Error applying 4-5 star filter: {e}")

    def select_date(self):
        elements = self.driver.find_elements(By.XPATH, '//button[@jsname="a1ZUMe" and @data-delta="1"]')
        months = 5 if not config.testing else 1
        for _ in range (1):
            for element in reversed(elements):
                for _ in range(25):
                    element.click()
            self.wait_for_loading()
            # time.sleep(5)
        
    def scrape_current_page(self, count, total):
        hotel_cards = self.driver.find_elements(By.XPATH, "//a[@class='PVOOXe']")

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

    def pull_results(self):
        total_sites = int(search_result)
        hotel_names = []

        while len(hotel_names) < total_sites:
        # Call the function to scrape the current page
            hotel_names = hotel_names + self.scrape_current_page(len(hotel_names), total_sites)

            # Check if len(hotel_names) is still less than total_sites
            if len(hotel_names) < total_sites:
                # Find and click the "next" button to load more results
                next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]/ancestor::button")
                next_button.click()            
                time.sleep(3)
            else:
                break

        return hotel_names



if __name__ == '__main__':

    # launch()
    # update_search_results()

    region = 'charleston'
    gs = GoogleScraper(region)
    gs.search()
    gs.apply_filters()
    hotels = gs.pull_results()
    print(hotels)

    print('here')
    

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from utils import find_best_matching_link
import requests
from bs4 import BeautifulSoup

class TravelWeekly:
    url: str
    driver: WebDriver
    wait: WebDriverWait

    def __init__(self) -> None:
        self.url = r'https://www.travelweekly.com/Hotels'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)  # Maximum wait time of 10 seconds (adjust as needed)

    def quit(self):
        self.driver.quit()

    def go_to_page(self, url: str = 'https://www.travelweekly.com/Hotels') -> None:
        self.driver.get(url)

    def search_hotels(self, hotel_name):
        search_input = self.driver.find_element(By.ID, "txtHotelSearch")

        # Type the hotel name into the search bar
        search_input.send_keys(hotel_name)

        # Simulate pressing the Enter key to submit the search
        search_input.send_keys(Keys.ENTER)
                
    def select_hotel_link(self, hotel_name):
        all_links = self.driver.find_elements(By.TAG_NAME, "a")

        # Define your search query
        search_query = hotel_name

        # Filter links based on text content similarity

        matching_links = [find_best_matching_link(all_links, search_query)]
        
        # if matching_links:
        self.go_to_page(matching_links[0].get_attribute("href"))
        

def get_hotel_data(url: str) -> dict[str,str]:

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the HTML content of the webpage
        html_content = response.text

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the <td> element with class "rooms"
        rooms_element = soup.find("td", class_="rooms")
        rate_element = soup.find("td", class_="rates")

        
        # Extract the text content from the elements
        rooms = rooms_element.get_text(strip=True)
        rate = rate_element.get_text(strip=True)

        if len(rate) > 1:
            # Find the <li> element with the class "label" containing "Standard Room:"
            standard_room_element = soup.find("span", class_="label", text="Standard Room:")
            standard_room_rate = standard_room_element.next_sibling
        else:
            standard_room_rate = ""


        return {'rooms' : rooms, 'rate' : standard_room_rate}
    else:
        return (f"Failed to retrieve content. Status code: {response.status_code}")


def convert_rates(raw):
    # Define a regular expression pattern to match currency amounts with optional commas and periods
    pattern = r'\$[0-9,.]+'  # This pattern matches currency amounts

    # Use re.findall to find all matching currency amounts in the text
    currency_amounts = re.findall(pattern, raw)

    # Extract the individual currency amounts and convert them to floats
    extracted_amounts = []
    for currency_amount in currency_amounts:
        # Remove the dollar sign and any commas
        currency_amount_cleaned = currency_amount.replace('$', '').replace(',', '')
        # Convert to float
        extracted_amounts.append(float(currency_amount_cleaned))

    # Determine the result based on the number of extracted amounts
    if len(extracted_amounts) == 0:
        result = None
    elif len(extracted_amounts) == 1:
        result = extracted_amounts[0]
    else:
        # Calculate the average of the extracted amounts
        result = sum(extracted_amounts) / len(extracted_amounts)

    return result


if __name__ == '__main__':
    raw = ' from $313-$339 (USD) - approx 400 sq ft'
    rates = convert_rates(raw)


    hotel = 'Market Pavilion Hotel'

    travel_weekly = TravelWeekly()
    travel_weekly.search_hotels(hotel)
    travel_weekly.select_hotel_link(hotel)
    travel_weekly.go_to_page('https://www.travelweekly.com/Hotels/Charleston/Market-Pavilion-Hotel-p3989887')
    data = get_hotel_data(travel_weekly.driver.current_url)


    print('here')
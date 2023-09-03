from google_hotel.scaper import select_date
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup

class TravelWeekly:
    url: str
    driver: WebDriver

    def __init__(self) -> None:
        self.url = r'https://www.travelweekly.com/Hotels'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)


    def go_to_page(self, url: str = 'https://www.travelweekly.com/Hotels') -> None:
        self.driver.get(url)

    def search_hotels(self, hotel_name):
        search_input = self.driver.find_element(By.ID, "txtHotelSearch")

        # Type the hotel name into the search bar
        search_input.send_keys(hotel_name)

        # Simulate pressing the Enter key to submit the search
        search_input.send_keys(Keys.ENTER)
                


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

        # Extract the text content from the <td> element
        rooms = rooms_element.get_text(strip=True)
        rate = rate_element.get_text(strip=True)
        # Print the extracted room number
        return {'rooms' : rooms, 'rate' : rate}
    else:
        return (f"Failed to retrieve content. Status code: {response.status_code}")

    



if __name__ == '__main__':
    travel_weekly = TravelWeekly()
    travel_weekly.search_hotels("Market Pavilion Hotel")
    # travel_weekly.go_to_page('https://www.travelweekly.com/Hotels/Charleston/Market-Pavilion-Hotel-p3989887')
    # travel_weekly.get_hotel_data()

    print('here')
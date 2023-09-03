import requests
from bs4 import BeautifulSoup

# Replace this URL with the one you want to scrape
url = "https://www.travelweekly.com/Hotels/Charleston/Market-Pavilion-Hotel-p3989887"

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
    print(f"Number of rooms: {rooms}")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

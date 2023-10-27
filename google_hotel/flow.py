from google_hotel.scraper import GoogleScraper

from dataclasses import dataclass

@dataclass
class Hotel:
    name: str
    rooms: int = None
    rate: float = None
    ef: float = None

def convert_to_list_of_hotels(hotel_names: list[str]) -> list[Hotel]:
    return [Hotel(name) for name in hotel_names]

def run(region):
    gs = GoogleScraper(region)
    gs.search()
    gs.apply_filters()
    hotel_names = gs.pull_results()
    hotels = convert_to_list_of_hotels(hotel_names)
    gs.quit()
    return hotels


if __name__ == "__main__":
    run('charleston')
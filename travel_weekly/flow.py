import hotel
from google_hotel.flow import Hotel
from travel_weekly.scraper import TravelWeekly
from travel_weekly.scraper import get_hotel_data
from travel_weekly.scraper import convert_rates

def run(hotels: list[Hotel]):
    tws = TravelWeekly()
    for hotel in hotels:
        tws.search_hotels(hotel.name)
        tws.select_hotel_link(hotel.name)
        data = get_hotel_data(tws.driver.current_url)
        data['rate'] = convert_rates(data.get('rate'))
        hotel.__dict__.update(data)
        tws.go_to_page(tws.url)
    return hotels



if __name__ == '__main__':
    from google_hotel.flow import Hotel
    hotels = [Hotel('Market Pavilion Hotel')]
    run(hotels)
    print('here')
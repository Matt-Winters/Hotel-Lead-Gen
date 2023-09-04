import hotel
from google_hotel.flow import Hotel
from travel_weekly.scraper import TravelWeekly
from travel_weekly.scraper import get_hotel_data
from travel_weekly.scraper import convert_rates

def run(hotels: list[Hotel]):
    tws = TravelWeekly()
    for hotel in hotels:
        print(f'Extracting: {hotel.name}')
        tws.search_hotels(hotel.name)
        try:
            tws.select_hotel_link(hotel.name)
        except Exception as e:
            print("failed to find Travel Weekly Link")
            tws.go_to_page(tws.url)
            continue
        data = get_hotel_data(tws.driver.current_url)
        data['rate'] = convert_rates(data.get('rate'))
        hotel.__dict__.update(data)
        tws.go_to_page(tws.url)
    return hotels



if __name__ == '__main__':
    from google_hotel.flow import Hotel
    hotels = [
        'Mills House Charleston, Curio Collection by Hilton', 
        'The Restoration Charleston', 'Planters Inn', 'The Vendue', 
        'Charleston Harbor Resort and Marina', 'Mills House Charleston, Curio Collection by Hilton', 
        'Hotel Bella Grace', 'The Spectator Hotel', 'French Quarter Inn', 'Emeline', 
        'HarbourView Inn', 'Market Pavilion Hotel', 'Grand Bohemian Hotel Charleston, Autograph Collection', 
        'The Charleston Place', 'The Lindy Renaissance Charleston Hotel', 
        'The Palmetto Hotel, Charleston', 'Hotel Bennett', 'The Dewberry Charleston', 
        'Luxury Hotel Suites @ 493 King', 'The Restoration Charleston', 
        'The Pinch Charleston', 'Charleston Harbor Resort and Marina', 'Zero George', 
        'French Quarter Inn', 'Zero George', 'The Pinch Charleston'
    ]
    hotels = [Hotel(name) for name in hotels]
    # hotels = [Hotel('Mills House Charleston')]
    run(hotels)
    print('here')
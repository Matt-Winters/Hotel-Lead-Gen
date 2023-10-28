from google_hotel import flow as google_flow
from travel_weekly import flow as tw_flow
import csv
import io
import config
import logging
from google_sheets import GoogleSheets
from google_hotel.flow import Hotel


def convert_to_csv(hotels):
    # Create an in-memory file-like object
    memory_file = io.StringIO()
    
    # Create a CSV writer using the memory file
    writer = csv.writer(memory_file)
    
    # Write the header row
    writer.writerow(['Name', 'Rooms', 'Rate'])
    
    # Write the hotel data rows
    for hotel in hotels:
        writer.writerow([hotel.name, hotel.rooms, hotel.rate])
    
    # Move the file pointer to the beginning of the memory file
    memory_file.seek(0)
    
    # Read the contents of the memory file
    csv_contents = memory_file.getvalue()
    
    return csv_contents

def convert_to_csv_string(hotels):
    # Create a header row
    header = "Name,Rooms,Rate, "
    
    # Create data rows
    data_rows = [f"{hotel.name},{hotel.rooms},{hotel.rate}" for hotel in hotels]
    
    # Combine header and data rows into a single string
    csv_string = "\n".join([header] + data_rows)
    
    return csv_string

def convert_to_csv_file(hotels, filename):
    # Define the CSV file's field names
    field_names = ["Name", "Rooms", "Rate", "EF Score"]

    # Create a list of dictionaries for each hotel
    hotel_data = [{"Name": hotel.name, "Rooms": hotel.rooms, "Rate": hotel.rate, "EF Score": hotel.ef} for hotel in hotels]

    # Write the data to a CSV file
    with open(filename, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()  # Write the header row
        writer.writerows(hotel_data)  # Write the data rows

def remove_duplicates(list_of_hotels: list[Hotel]):
    gs = GoogleSheets()
    contacted_hotels = gs.download_sheet_data('1g9zwbC3w0ROna5k5ybOJtlV2SY_4b4RC-pHDeQSvyT8')
    for hotel in list_of_hotels.copy():
        if hotel.name in contacted_hotels:
            list_of_hotels.remove(hotel)
    return list_of_hotels
    
def run_script(region) -> str:
    logging.info("Running google flow")
    list_of_hotels = google_flow.run(region)
    logging.info(f"Finished running google flow: Hotels found - {len(list_of_hotels)}")
    list_of_hotels2 = remove_duplicates(list_of_hotels)
    print(f'og list count: {len(list_of_hotels)} - new count: {len(list_of_hotels2)}')
    if config.testing:
        list_of_hotels = list_of_hotels[:3]
        logging.info(f"testing mode enabled hotels to extract: {len(list_of_hotels)}")

    logging.info('Running Travel Weekly flow')
    list_of_hotels = tw_flow.run(list_of_hotels)
    logging.info('Completed Travel Weekly extraction')
    # data = convert_to_csv_string(list_of_hotels)
        
    return list_of_hotels

if __name__ == '__main__':
    region = 'charleston'
    data = run_script(region)
    from google_hotel.flow import Hotel


    # hotels = [Hotel('Market Pavilion Hotel')]
    convert_to_csv_file(data, region + ".csv")
    gs = GoogleSheets()
    gs.upload_csv(region+'.csv', region + ' - scraped data')

    logging.info('here')
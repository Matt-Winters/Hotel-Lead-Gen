from google_hotel import flow as google_flow
from travel_weekly import flow as tw_flow
import csv
import io


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


def run_script(region) -> str:

    list_of_hotels = google_flow.run(region)

    list_of_hotels = tw_flow.run(list_of_hotels)

    data = convert_to_csv(list_of_hotels)
        
    return data

if __name__ == '__main__':
    run_script('charleston')
    from google_hotel.flow import Hotel
    hotels = [Hotel('Market Pavilion Hotel')]
    data = convert_to_csv(hotels)
    print('here')
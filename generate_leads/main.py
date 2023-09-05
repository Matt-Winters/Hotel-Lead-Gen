from google_hotel import flow as google_flow
from travel_weekly import flow as tw_flow
import csv
import io
import config

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
    header = "Name,Rooms,Rate"
    
    # Create data rows
    data_rows = [f"{hotel.name},{hotel.rooms},{hotel.rate}" for hotel in hotels]
    
    # Combine header and data rows into a single string
    csv_string = "\n".join([header] + data_rows)
    
    return csv_string


def run_script(region) -> str:
    list_of_hotels = google_flow.run(region)

    if config.testing:
        list_of_hotels = list_of_hotels[:3]

    list_of_hotels = tw_flow.run(list_of_hotels)

    # data = convert_to_csv_string(list_of_hotels)
        
    return list_of_hotels

if __name__ == '__main__':
    data = run_script('charleston')
    from google_hotel.flow import Hotel
    hotels = [Hotel('Market Pavilion Hotel')]
    data = convert_to_csv(hotels)
    print('here')
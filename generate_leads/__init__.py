import logging
import azure.functions as func
from generate_leads.main import run_script
import config
import csv
import io


def convert_to_csv_binary(hotels):
    # Create a list of dictionaries containing the data
    data_list = [{"Name": hotel.name, "Rooms": hotel.rooms, "Rate": hotel.rate} for hotel in hotels]

    # Create a CSV file in-memory
    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=["Name", "Rooms", "Rate"])
    csv_writer.writeheader()
    csv_writer.writerows(data_list)

    # Convert the CSV content to bytes
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    return csv_bytes


def parse_bool_param(param_value, default=False):
    return param_value.lower() in ['1', 'true'] if param_value else default


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    region = req.params.get("region")
    testing_param = req.params.get('testing')
    headless_param = req.params.get('headless')
    
    config.testing = parse_bool_param(testing_param)
    config.headless = parse_bool_param(headless_param, False) 

    try:

        logging.info('starting script')
        hotels_data = run_script(region)
        
        logging.info('converting to csv')
        # Convert your list of hotels to CSV binary data
        csv_data = convert_to_csv_binary(hotels_data)
        logging.info('csv generated')
        # Set appropriate HTTP headers
        headers = {
            "Content-Disposition": "attachment; filename=hotels.csv",
            "Content-Type": "text/csv"
        }

        return func.HttpResponse(
            csv_data,
            status_code=200,
            headers=headers
        )
        
    except Exception as e:
        logging.exception("Top level failure: returning 500")
        return func.HttpResponse(
            str(e),
            status_code=500
        )

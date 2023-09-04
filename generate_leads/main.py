from google_hotel import flow as google_flow
from travel_weekly import flow as tw_flow


def convert_to_csv(data):
    return data


def run_script(region):

    list_of_hotels = google_flow.run(region)

    data = tw_flow.run(list_of_hotels)

    csv = convert_to_csv(data)

        
    return csv
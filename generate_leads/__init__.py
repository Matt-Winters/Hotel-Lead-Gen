import logging

import azure.functions as func

from generate_leads.main import run_script

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pararms = req.params.get("region")

    try:
        data = run_script(pararms)
        return func.HttpResponse(
            data,
            200
        )
        
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500
        )

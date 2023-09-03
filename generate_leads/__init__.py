import logging

import azure.functions as func

from generate_leads.main import run_script

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pararms = req.params

    try:
        run_script()
        
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500
        )

import json
import logging

import azure.functions as func
from weasyprint import HTML


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
        html, options = payload['html'], payload['options']

        logging.info(
            '[html-to-pdf] Python HTTP trigger function processed a request.')
        logging.info(f'html={html}\n')
        logging.info(f'options={json.dumps(options, indent=4)}\n')

        pdfBytes = HTML(string=str(html)).write_pdf(options)

        return func.HttpResponse(
            pdfBytes,
            status_code=200,
            mimetype="application/pdf"
        )
    except Exception as e:
        logging.error(e)

        # key not found or value errors
        if type(e) is ValueError or KeyError:
            return func.HttpResponse(
                e.__repr__(),
                status_code=400,
            )

        # other errors
        return func.HttpResponse(
            e.__repr__(),
            status_code=500,
        )

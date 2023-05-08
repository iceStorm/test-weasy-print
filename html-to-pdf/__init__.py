import json
import logging

import azure.functions as func
from weasyprint import CSS, HTML

from .PdfOptions import *

"""
Read the docs: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#quickstart
"""


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
        html, options = payload['html'], payload['options']

        if type(html) is not str:
            raise TypeError('"html" must be a string')

        if type(options) is not dict:
            raise TypeError('"options" must be an object')

        logging.info('[html-to-pdf] Start generating PDF from HTML.')
        logging.info(f'html={html}')
        logging.info(f'options={json.dumps(options, indent=4)}\n')

        # type cast
        pdf_options = PdfOptions(options)

        # https://developer.mozilla.org/en-US/docs/Web/CSS/@page
        layoutStyle = CSS(
            string="@page { size: %s; margin: %s;  }" % (pdf_options.size, pdf_options.margin))

        document = HTML(string=html).render(
            stylesheets=[layoutStyle])

        pdf = document.write_pdf()

        return func.HttpResponse(
            pdf,
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

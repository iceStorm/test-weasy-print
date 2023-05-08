

import json


class PdfOptions():
    # https://developer.mozilla.org/en-US/docs/Web/CSS/@page/size#syntax
    size: str
    margin: str

    def __init__(self, options: dict):
        self.size = options.get('size', 'auto')
        self.margin = options.get('margin', '20px')

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

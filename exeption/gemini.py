
class ResponseError(Exception):
    def __init__(self, code, text):
        self.code = code
        self.text = text

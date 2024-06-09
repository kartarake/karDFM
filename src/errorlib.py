class karDFM_TypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class karDFM_TypeDefError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class karDFM_DocNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
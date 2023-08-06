class NotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class LibraryUpdateAvailable(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


def CheckException(data):
    errorCode: str = data["error"]
    errorMessage: str = data["response"]

    if errorCode != "true": raise NotFound(errorMessage)
    else: raise Exception(errorMessage)
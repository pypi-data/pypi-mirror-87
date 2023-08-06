class FileNotFoundError(Exception):
    """
        Exception raised when file does not exists.
        Attributes:
            entity -- name of the entity that file represents
            date -- 
    """
    def __init__(self, entity, date):
        self.entity = entity
        self.date = date
    def __str__(self):
        return f"No files found for {self.entity} on date {self.date}."


class ColumnNotFoundError(Exception):
    """
        Exception raised when column of file does not exists.
        Attributes:
            entity -- name of the entity
            column -- name of the column
    """
    def __init__(self, entity, column):
        self.entity = entity
        self.column = column


class ClientResponseError(Exception):
    """
        Exception raised when client service return an error
        Attributes:
            name -- error name
            status_code -- http response error code
    """
    def __init__(self, name, status_code):
        self.name = name
        self.status_code = status_code


class ApiResponseError(Exception):
    """
        Exception raised when client service return an error
        Attributes:
            name -- error name
            status_code -- http response error code
    """
    def __init__(self, name, status_code, data = None):
        self.name = name
        self.status_code = status_code
        self.data = data


class SaveFileError(Exception):
    """
        Exception raised when save a file with data loaded return an error
        Attributes:
            entity -- name of the entity that file represents
    """
    def __init__(self, entity):
        self.entity = entity


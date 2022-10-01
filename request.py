from exceptions import InvalidRequest


class Request:
    """
    Class for parsing a user request into single words
    """
    def __init__(self, request: str):
        request_as_list = request.lower().split(' ')
        if len(request_as_list) != 7:
            raise InvalidRequest

        self.where_from = request_as_list[4]
        self.where_to = request_as_list[6]
        self.amount = int(request_as_list[1])
        self.product = request_as_list[2]

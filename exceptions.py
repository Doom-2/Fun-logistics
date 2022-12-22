class BaseError(Exception):
    message = '\nAn unexpected error has occurred.'


class InvalidRoute(BaseError):
    message = '\nThe route was not found. Try again'


class InvalidRequest(BaseError):
    message = '\nIncorrect request. Try again.'


class NotEnoughSpace(BaseError):
    message = '\nThe recipient does not have enough space. Ask him for a storage extension.'


class NotEnoughProduct(BaseError):
    message = '\nThe sender does not have enough items. Try ask him for a smaller quantity.'


class InvalidProduct(BaseError):
    message = '\nThe sender does not have this item in stock.'


class TooManyDifferentProducts(BaseError):
    message = '\nThe recipient has exhausted the product range limit. He can store a maximum of 5 items.'


class ZeroQuantity(BaseError):
    message = '\nZero quantity of items has been entered. Try again.'


class NegativeQuantity(BaseError):
    message = '\nThe quantity of an item cannot be negative. Try again.'

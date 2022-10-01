class BaseError(Exception):
    message = '\nНепредвиденная ошибка.'


class InvalidRoute(BaseError):
    message = '\nМаршрут не найден. Попробуйте снова.'


class InvalidRequest(BaseError):
    message = '\nНеправильный запрос. Попробуйте снова.'


class NotEnoughSpace(BaseError):
    message = '\nНедостаточно места у получателя. Нужно чтобы он освободил или расширил хранилище.'


class NotEnoughProduct(BaseError):
    message = '\nНедостаточно товара у отправителя. Попробуйте запросить меньшее количество.'


class InvalidProduct(BaseError):
    message = '\nУ отправителя нет в наличии такого товара.'


class TooManyDifferentProducts(BaseError):
    message = '\nУ получателя исчерпан лимит на ассортимент товаров. Может хранить максимум 5 наименований.'


class ZeroQuantity(BaseError):
    message = '\nВы ввели нулевое количество товара. Попробуйте снова.'


class NegativeQuantity(BaseError):
    message = '\nКоличество товара не может быть отрицательным. Попробуйте снова.'

from request import Request
from store import Store
from shop import Shop
from exceptions import BaseError, InvalidRequest, NotEnoughSpace, InvalidRoute, TooManyDifferentProducts


# Defining instances of each storage and all storages dict
store = Store(items={
    "книги": 12,
    "смартфоны": 15,
    "мониторы": 8,
    "телевизоры": 14,
    "печеньки": 15,
    "кофе": 15,
    "пиццы": 20
})

shop = Shop(items={
    "книги": 3,
    "елки": 4,
    "кофе": 2
})

storages = {
    "склад": store,
    "магазин": shop
}


def main():
    while True:

        # Printing information on all storages
        for storage in storages:
            print(f'\nВ {storage} хранится:')
            for item in storages[storage].get_items.items():
                print(f'{item[0].capitalize()} : {item[1]}')

        user_input = input(
            '\nВведите задание курьеру в формате\033[33m Доставить 3 печеньки из склад в магазин\033[0m\n'
            'Слова\033[33m склад\033[0m и\033[33m магазин\033[0m можно менять местами\n'
            'Чтобы завершить работу введите \033[1m\'stop\' или \'стоп\'\033[0m\n'
        )

        if user_input.lower() in ['stop', 'стоп']:
            print('Всего доброго. Приходите к нам еще.')
            break

        try:
            request = Request(user_input)
        except InvalidRequest as error:
            print(error.message)
            continue

        try:
            # If points of departure and destination are correct
            if request.where_from == "склад" and request.where_to == "магазин":
                if storages["магазин"].get_unique_items_count >= 5 \
                        and request.product not in storages["магазин"].get_items:
                    raise TooManyDifferentProducts

                # If the item has left the sender
                storages["склад"].remove(request.product, request.amount)
                print(f'Курьер забрал {request.amount} {request.product} из {request.where_from}')

                # If the item has arrived to the recipient
                storages["магазин"].add(request.product, request.amount)
                print(f'Курьер доставил {request.amount - storages["магазин"].excess} {request.product} '
                      f'из {request.where_from} в {request.where_to}')

                # If there is an Excess quantity of item that need to be returned to the sender
                if storages["магазин"].excess:
                    storages["склад"].add(request.product, storages["магазин"].excess)
                    storages["магазин"].excess = 0

            # Changing places of departure and destination
            elif request.where_from == "магазин" and request.where_to == "склад":
                storages["магазин"].remove(request.product, request.amount)
                print(f'Курьер забрал {request.amount} {request.product} из {request.where_from}')

                storages["склад"].add(request.product, request.amount)
                print(f'Курьер доставил {request.amount - storages["склад"].excess} {request.product} '
                      f'из {request.where_from} в {request.where_to}')

                if storages["склад"].excess:
                    storages["магазин"].add(request.product, storages["склад"].excess)
                    storages["склад"].excess = 0
            else:
                raise InvalidRoute

        # Catching a specific exception
        except NotEnoughSpace as error:
            if request.where_from == "склад":
                storages["склад"].add(request.product, request.amount)
            elif request.where_from == "магазин":
                storages["магазин"].add(request.product, request.amount)
            print(error.message)

        # Catching all possible exceptions
        except BaseError as error:
            print(error.message)


if __name__ == '__main__':
    main()

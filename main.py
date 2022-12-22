from request import Request
from store import Store
from shop import Shop
from exceptions import BaseError, InvalidRequest, NotEnoughSpace, InvalidRoute, TooManyDifferentProducts

# Defining instances of each storage and all storages dict
store = Store(items={
    "books": 12,
    "smartphones": 15,
    "monitors": 8,
    "laptops": 14,
    "cookies": 15,
    "coffee": 15,
    "pizza": 20
})

shop = Shop(items={
    "books": 3,
    "consoles": 4,
    "coffee": 2
})

storages = {
    "store": store,
    "shop": shop
}


def main():
    user_input_is_correct = True
    while True:

        # Printing information on all storages if user input is correct
        if user_input_is_correct:
            for storage in storages:
                print(f'\nIn the {storage} are stored:')
                for item in storages[storage].get_items.items():
                    print(f'{item[0].capitalize()} : {item[1]}')

        user_input = input(
            '\nEnter the task to the courier in the following format\033[33m Deliver 3 cookies from the store to the shop\033[0m\n'
            'Words\033[33m store\033[0m and\033[33m shop\033[0m can be swapped\n'
            'For finish type \033[1m\'stop\' or \'end\'\033[0m\n> '
        )

        if user_input.lower() in ['stop', 'end']:
            print('Have a nice day. Come again.')
            break

        try:
            request = Request(user_input)
        except InvalidRequest as error:
            user_input_is_correct = False
            print(error.message)
            continue

        try:
            # If points of departure and destination are correct
            user_input_is_correct = True
            if request.where_from == "store" and request.where_to == "shop":
                if storages["shop"].get_unique_items_count >= 5 \
                        and request.product not in storages["shop"].get_items:
                    raise TooManyDifferentProducts

                # If the item has left the sender
                storages["store"].remove(request.product, request.amount)
                print(f'The courier has taken {request.amount} {request.product} from the {request.where_from}')

                # If the item has arrived to the recipient
                storages["shop"].add(request.product, request.amount)
                print(f'The courier has delivered {request.amount - storages["shop"].excess} {request.product} '
                      f'from the {request.where_from} to the {request.where_to}')

                # If there is an Excess quantity of item that need to be returned to the sender
                if storages["shop"].excess:
                    storages["store"].add(request.product, storages["shop"].excess)
                    storages["shop"].excess = 0

            # Changing places of departure and destination
            elif request.where_from == "shop" and request.where_to == "store":
                storages["shop"].remove(request.product, request.amount)
                print(f'The courier has taken {request.amount} {request.product} from the {request.where_from}')

                storages["store"].add(request.product, request.amount)
                print(f'The courier has delivered {request.amount - storages["store"].excess} {request.product} '
                      f'from the {request.where_from} to the {request.where_to}')

                if storages["store"].excess:
                    storages["shop"].add(request.product, storages["store"].excess)
                    storages["store"].excess = 0
            else:
                # user_input_is_correct = False
                raise InvalidRoute

        # Catching a specific exception
        except NotEnoughSpace as error:
            if request.where_from == "store":
                storages["store"].add(request.product, request.amount)
            elif request.where_from == "shop":
                storages["shop"].add(request.product, request.amount)
            print(error.message)
            user_input_is_correct = False

        # Catching all possible exceptions
        except BaseError as error:
            print(error.message)
            user_input_is_correct = False


if __name__ == '__main__':
    main()

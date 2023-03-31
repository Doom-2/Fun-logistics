import marshmallow_dataclass
import requests
from .exchange_rate_schema import DailyCurrency


class CurrencyCBRRates:
    """
    Gets actual currency rates from CBR API
    """

    def get_url(self):
        return 'https://www.cbr-xml-daily.ru/daily_json.js'

    def get_all_rates(self, ) -> DailyCurrency:
        response = requests.get(self.get_url()).json()
        rates_schema = marshmallow_dataclass.class_schema(DailyCurrency)
        obj = rates_schema().load(response)
        return obj

    def get_rate_by_code(self, currency_name: str) -> float:
        """
        Passes as an argument a specific currency code, 3 capital letters
        """
        try:
            response = requests.get(self.get_url()).json()
            rates_schema = marshmallow_dataclass.class_schema(DailyCurrency)
            obj = rates_schema().load(response)
            return obj.Valute[currency_name].Value

        except KeyError:
            print('There is no such currency code')


# Get actual USD exchange rate from CBR API
current_rates = CurrencyCBRRates()
USD_RATE = current_rates.get_rate_by_code('USD')

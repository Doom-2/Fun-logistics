from dataclasses import dataclass
from typing import Dict
from marshmallow import EXCLUDE


@dataclass
class Currency:
    ID: str
    Name: str
    Value: float

    class Meta:
        unknown = EXCLUDE


@dataclass
class DailyCurrency:
    Date: str
    Valute: Dict[str, Currency]

    class Meta:
        unknown = EXCLUDE

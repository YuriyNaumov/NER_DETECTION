import re

from yargy import (
    rule, Parser, or_, and_
)
from yargy.interpretation import fact, const
from yargy.predicates import eq, caseless, length_eq, in_, normalized, type as _type



def normalize_integer(value):
    integer = re.sub(r'[\s.,]+', '', value)
    return int(integer)


def normalize_fraction(value):
    fraction = value.ljust(2, '0')
    return int(fraction)

def get_money(s):
    Money = fact(
        'Money',
        ['multiplier', 'amount', 'currency']
    )

    DOT = eq('.')
    INT = _type('INT')

    ############
    #
    #  MULTIPLIER
    #
    ##########

    MILLIARD = or_(
        rule(caseless('млрд'), DOT.optional()),
        rule(normalized('миллиард'))
    ).interpretation(
        const(10 ** 9)
    )

    MILLION = or_(
        rule(caseless('млн'), DOT.optional()),
        rule(normalized('миллион'))
    ).interpretation(
        const(10 ** 6)
    )

    THOUSAND = or_(
        rule(caseless('тр'), DOT.optional()),
        rule(caseless('т'), caseless('р'), DOT.optional()),
        rule(caseless('т'), DOT.optional()),
        rule(normalized('тысяча'))
    ).interpretation(
        const(10 ** 3)
    )

    MULTIPLIER = or_(
        MILLIARD,
        MILLION,
        THOUSAND
    ).interpretation(
        Money.multiplier
    )

    RUBLES = or_(
        rule(normalized('рубль')),
        rule(
            or_(
                caseless('руб'),
                caseless('р'),
                caseless('тр'),
                eq('₽')
            ),
            DOT.optional()
        )
    )

    CURRENCY = or_(
        RUBLES
    ).interpretation(
        Money.currency
    )

    PART = and_(
        INT,
        length_eq(3)
    )

    SEP = in_(',. ')

    INTEGER = or_(
        rule(INT),
        rule(INT, PART),
        rule(INT, SEP, INT, SEP, INT),
        rule(INT, PART, PART),
        rule(INT, SEP, PART),
        rule(INT, SEP, PART, SEP, PART)
    )

    AMOUNT = rule(
        INTEGER,
        rule(SEP).optional(),
        INTEGER.optional(),
    ).interpretation(Money.amount.custom(normalize_integer))

    MONEY = rule(
        AMOUNT,
        MULTIPLIER.optional(),
        CURRENCY

    ).interpretation(
        Money
    )

    parser = Parser(MONEY)
    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    money = {}
    money['money'] = {}
    money_amount = []
    money_multiplier = []
    money_currency = []

    if matches:
        for match in matches:
            if match.fact.multiplier:
                money_multiplier.append(match.fact.multiplier)
            else:
                money_multiplier.append(not_data)
            if match.fact.amount:
                money_amount.append(match.fact.amount)
            else:
                money_amount.append(match.fact.amount)
            if match.fact.currency:
                money_currency.append(match.fact.currency)
            else:
                money_currency.append(not_data)
    else:
        money_multiplier.append(not_data)
        money_amount.append(not_data)
        money_currency.append(not_data)

    money['money']['amount'] = money_amount
    money['money']['currency'] = money_currency
    money['money']['multiplier'] = money_multiplier

    return money



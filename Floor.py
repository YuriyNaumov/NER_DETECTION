from yargy import (
    rule, Parser, or_, not_
)
from yargy.interpretation import fact
from yargy.predicates import eq, caseless, in_, type as _type


def clear_etaj(value):
    try:
        k = int(value.split('/')[0])
    except:
        k = value
    return k

def clear_storey(value):
    try:
        k = int(value.split('/')[1])
    except:
        k = value
    return k


def find_etaj(s):
    Floor = fact(
        'Floor',
        ['floor', 'storeys', 'unit']
    )
    SEP = in_('/-')
    DOT = in_('.')
    INT = _type('INT')

    Unit = or_(
        rule(caseless('этаж'), DOT.optional()),
        rule(caseless('эт'), DOT.optional())).interpretation(Floor.unit)

    Etaj_options = or_(
        rule(INT, Unit.optional()),
        rule(INT, SEP, INT)
    )

    Etaj = rule(Etaj_options).interpretation(Floor.floor.custom(clear_etaj))

    Etajnost_options = or_(
        rule(SEP, INT))

    Etajnost = rule(Etajnost_options).interpretation(Floor.storeys.custom(clear_storey))

    FLOOR = or_(
        rule(Etaj, Etajnost.optional(), Unit),
        rule(Etaj, Etajnost)
    ).interpretation(Floor)

    parser = Parser(FLOOR)
    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    etaj = {}
    floors = []
    storey = []
    unit = []

    etaj['etaj'] = {}
    if matches:
        try:
            for match in matches:
                if match.fact.floor:
                    floors.append(match.fact.floor)
                else:
                    floors.append(not_data)
                if match.fact.storeys:
                    storey.append(match.fact.storeys)
                else:
                    storey.append(not_data)
                if match.fact.unit:
                    unit.append(match.fact.unit)
                else:
                    unit.append(not_data)
        except:
            floors.append(not_data)
            storey.append(not_data)
            unit.append(not_data)
    else:
        floors.append(not_data)
        storey.append(not_data)
        unit.append(not_data)

    etaj['etaj']['floor'] = floors
    etaj['etaj']['storey'] = storey
    etaj['etaj']['unit'] = unit

    return etaj


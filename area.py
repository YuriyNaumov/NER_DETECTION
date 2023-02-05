from yargy import (
    rule, Parser, or_
)
from yargy.interpretation import fact
from yargy.predicates import eq, caseless, in_, type as _type


def area_detection(s):
    area = fact(
        'Area',
        ['amount', 'unit']
    )

    DOT = eq('.')
    INT = _type('INT')
    Unit = or_(
        rule(caseless('кв'), DOT.optional(), caseless('м')),
        rule(caseless('квм'), DOT.optional()),
        rule(caseless('м2')),
        rule(caseless('кв.')),
        rule(caseless('м'), caseless('2')),
        rule(eq('кв.м.'))
    ).interpretation(
        area.unit)

    DELIMETER = in_('/')
    SEP = in_(',.')

    INTEGER = or_(
        rule(INT),
        rule(INT, SEP.optional()),
        rule(INT, SEP.optional(), INT),
        rule(INT, SEP, INT, SEP, INT),
    ).interpretation(area.amount)

    INTEGER_ALL_AREA = or_(
        rule(INT, DELIMETER.optional(), INT, DELIMETER.optional(), INT),
    ).interpretation(area.amount)

    AREA = or_(rule(INTEGER, Unit),
               rule(INTEGER_ALL_AREA)).interpretation(area)

    parser = Parser(AREA)
    matches = list(parser.findall(s))

    not_data = 'Нет данных'
    object_area = {}
    area_size = []
    area_unit = []
    object_area['area'] = {}

    if matches:
        for match in matches:
            if match.fact.amount:
                area_size.append(match.fact.amount)
            else:
                area_size.append(not_data)
            if match.fact.unit:
                area_unit.append(match.fact.unit)
            else:
                area_unit.append(not_data)
    else:
        area_size.append(not_data)
        area_unit.append(not_data)

    object_area['area']['size'] = area_size
    object_area['area']['unit'] = area_unit

    return object_area

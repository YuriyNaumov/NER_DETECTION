from yargy import (
    rule, Parser, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    type, in_)
from yargy.pipelines import morph_pipeline


def find_street(s, NSK_STREETS, STREETS_TYPE):
    Streets = fact(
        'Streets',
        ['name', 'type', 'home_number']
    )


    Streets_name = morph_pipeline(
        NSK_STREETS
    ).interpretation(Streets.name)



    Street_type_name = morph_pipeline(
        STREETS_TYPE
    ).interpretation(Streets.type)

    SEP = in_('/-абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    INT = type('INT')

    HOME_NUMBER_OPTIONS = or_(
        rule(INT),
        rule(INT, SEP),
        rule(INT, SEP, INT)
    )

    HOME_NUMBER = rule(
        HOME_NUMBER_OPTIONS,

    ).interpretation(Streets.home_number)

    STREETS_DEFINITION = rule(
        Street_type_name.optional(),
        SEP.optional(),
        Streets_name,
        SEP.optional(),
        Street_type_name.optional(),
        HOME_NUMBER.optional()
    ).interpretation(
        Streets)

    parser = Parser(STREETS_DEFINITION)
    matches = list(parser.findall(s))

    not_data = 'Нет данных'
    streets = {}
    steets_name = []
    streets_type = []
    streets_homeN = []

    streets["Streets"] = {}

    if matches:
        for match in matches:

            if match.fact.name:
                steets_name.append(match.fact.name)
            else:
                steets_name.append(not_data)

            if match.fact.type:
                streets_type.append(match.fact.type)
            else:
                streets_type.append(not_data)

            if match.fact.home_number:
                streets_homeN.append(match.fact.home_number)
            else:
                streets_homeN.append(not_data)

    else:
        streets["Streets"]['Streets_name'] = not_data
        streets["Streets"]['Street_type'] = not_data
        streets["Streets"]['home_number'] = not_data

    streets["Streets"]['Streets_name'] = steets_name
    streets["Streets"]['Street_type'] = streets_type
    streets["Streets"]['home_number'] = streets_homeN

    return streets

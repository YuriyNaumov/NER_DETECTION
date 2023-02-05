from yargy import (
    rule, Parser, or_
)
from yargy.interpretation import fact
from yargy.predicates import ( in_caseless, normalized, caseless, gram)
from yargy.pipelines import morph_pipeline

def raion_detection(s, NSK_DISTRICTS):
    Raion = fact(
        'Raion',
        ['name', 'type'])

    RAION_WORDS = or_(
        rule(caseless('р'), '-', in_caseless({'он', 'не'})),
        rule(normalized('район'))
    ).interpretation(
        Raion.type.const('район'))

    ADJF = gram('ADJF')

    MODIFIER = ADJF.interpretation(
        Raion.name.normalized()
    )

    RAION_NAMES = morph_pipeline(
        NSK_DISTRICTS,
    ).interpretation(Raion.name)

    RAION_DEFINITION = rule(
        #MODIFIER,
        RAION_NAMES,
        RAION_WORDS.interpretation(Raion.type).optional(),

    ).interpretation(Raion)

    parser = Parser(RAION_DEFINITION)
    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    districts = {}
    districts['raion'] = {}
    districts_names = []
    districts_types = []

    if matches:
        for match in matches:
            if match.fact.name:
                districts_names.append(match.fact.name)
            else:
                districts_names.append(not_data)

            if match.fact.type:
                districts_types.append(match.fact.type)
            else:
                districts_types.append(not_data)
    else:
        districts_names.append(not_data)
        districts_types.append(not_data)

    districts['raion']['name'] = districts_names
    districts['raion']['type'] = districts_types
    return districts
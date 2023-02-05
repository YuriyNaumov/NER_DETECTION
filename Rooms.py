from yargy import (
    rule, Parser, or_
)
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    type, in_)


def komnatnost(s):
    komnatnost = fact('komnatnost',
                      ['rooms_number'])

    rooms_number = []

    DOT = in_('.')
    STUDIA = morph_pipeline([
        'студия',
    ]).interpretation(komnatnost.rooms_number.const('студия'))

    ONE_ROOM = morph_pipeline([
        'однокомнатная',
        '1 ком',
        '1ая',
        '1-ая',
        '1-комн',
        '1-ка',
        '1ком',
        '1 комн'
        '1ком',
        '1ка',
        '1 кВ'
    ]).interpretation(komnatnost.rooms_number.const('1'))

    TWO_ROOM = morph_pipeline([
        'двухкомнантная',
        '2 ком',
        '2ая',
        '2-ая',
        '2-комн',
        '2-ка',
        '2ком',
        '2 комн'
        '2ком',
        '2ка',
        '2 кВ'
    ]).interpretation(komnatnost.rooms_number.const('2'))

    THREE_ROOM = morph_pipeline([
        'трехкомнатная',
        'трёхкомнатная',
        '3 ком',
        '3ая',
        '3-ая',
        '3-комн',
        '3-ка',
        '3ком',
        '3 комн'
        '3ком',
        '3ка',
        '3 кВ'
    ]).interpretation(komnatnost.rooms_number.const('3'))

    FOUR_ROOM =   morph_pipeline([
        'четырехкомнатная',
        'четырёхкомнатная'
        '4 ком',
        '4ая',
        '4-ая',
        '4-комн',
        '4-ка',
        '4ком',
        '4 комн'
        '4ком',
        '4 кВ'
    ]).interpretation(komnatnost.rooms_number.const('4'))

    FIVE_ROOM = morph_pipeline([
        'пятикомнатная',
        '5 ком',
        '5ая',
        '5-ая',
        '5-комн',
        '5-ка',
        '5ком',
        '5 комн'
        '5ком',
        '5 кВ'
    ]).interpretation(komnatnost.rooms_number.const('5'))

    NUMBER_OF_ROOMS = rule(
        or_(STUDIA, ONE_ROOM, TWO_ROOM, THREE_ROOM, FOUR_ROOM, FIVE_ROOM),
        DOT.optional()
    ).interpretation(komnatnost)

    parser = Parser(NUMBER_OF_ROOMS)

    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    rooms = {}
    rooms['room'] = {}
    rooms_number = []
    if matches:
        for match in matches:
            if match.fact.rooms_number:
                rooms_number.append(match.fact.rooms_number)
            else:
                rooms_number.append(not_data)
    else:
        rooms_number.append(not_data)

    rooms['room']['number_of_rooms'] = rooms_number
    return rooms

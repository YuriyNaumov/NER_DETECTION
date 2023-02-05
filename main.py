import pandas as pd

import Floor
import streets as ta
import raion as tr
import object_type as ot
import Rooms
import money
import area
import action as act

import argparse
import json
import re


def get_parser_argument():
    parser = argparse.ArgumentParser(description='String for clarification')
    parser.add_argument('s', type=str, help='String decipher')
    args = parser.parse_args()
    return args


def get_string_parametrs(s, OBJECT_TYPES, NSK_STREETS, STREETS_TYPE, NSK_DISTRICTS):
    action = act.actions_type(s)
    raions = tr.raion_detection(s, NSK_DISTRICTS = NSK_DISTRICTS)
    streets = ta.find_street(s, NSK_STREETS=NSK_STREETS, STREETS_TYPE=STREETS_TYPE)
    object_type = ot.object_type_detection(s, OBJECT_TYPES=OBJECT_TYPES)
    rooms = Rooms.komnatnost(s)
    cost = money.get_money(s)
    flat_area = area.area_detection(s)
    etaj = Floor.find_etaj(s)

    merged_dict = {**action, **raions, **streets, **object_type, **rooms, **cost, **flat_area, **etaj}
    return merged_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # args = get_parser_argument()
    # raions = tr.raion_detection(args.s)
    # streets = ta.find_street(args.s)
    # object_type = ot.object_type_detection(args.s)
    # rooms = Rooms.komnatnost(args.s)
    # money = money.get_money(args.s)

    # s1 = 'привет '
    # s2 = '2ком квартиру в ленинском р-не 2 500 000 руб'
    # s3 = ' Продам 2 комн. 1 этаж. 4/7. 46м2 Народная 41. Отличное состояние, квартира с ремонтом и мебелью. Цена 3490 т.р '
    # s4 = 'Сдается трехкомантная квартира. 60,3 кв.м . Узаконена перепланировка из 3ки. 3/5 этаж. Обременение ВТБ. 15000'
    #lines  = [s3]
    test_df = pd.read_excel('test_df_200.xlsx')
    lines = list(test_df['text'])
    # lines  = [s3]

    OBJECT_TYPES = []
    with open('References/Object_types.txt', encoding="utf-8") as file:
        for line in file:
            name = line.rstrip()
            OBJECT_TYPES.append(name)

    NSK_STREETS = []
    with open('References/Nsk_streets.txt', encoding="utf-8") as file:
        for line in file:
            name = line.rstrip()
            NSK_STREETS.append(name)

    STREETS_TYPE = []
    with open('References/Street_type.txt', encoding="utf-8") as file:
        for line in file:
            name = line.rstrip()
            STREETS_TYPE.append(name)

    NSK_DISTRICTS = []
    with open('References/Nsk_districts.txt', encoding="utf-8") as file:
        for line in file:
            name = line.rstrip()
            NSK_DISTRICTS.append(name)

    all_lines = {}
    i = 1
    for line in lines:
        all_lines[line] = get_string_parametrs(line, OBJECT_TYPES, NSK_STREETS, STREETS_TYPE, NSK_DISTRICTS)
        print(i)
        i = i + 1
    r = json.dumps(all_lines, indent=4, ensure_ascii=False).encode('utf8')
    r_decoded = r.decode()
    #print(r_decoded)


    text_file = open("file.txt", "wt", encoding='utf-8')
    n = text_file.write(r_decoded)
    text_file.close()

    # df = pd.DataFrame(all_lines.items(), columns=['text', 'value'])
    # df.to_excel('test_check.xlsx')
    # print(df)

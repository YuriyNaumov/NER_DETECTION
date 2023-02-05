from yargy import (
    rule, Parser, or_
)
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

def actions_type(s):
    transactions = fact(
        'transactions',
        ['trans']
    )

    SALES = morph_pipeline([
        "продается", "продам",
        "продаю", "продаем", "продажа"]).interpretation(transactions.trans.const('Продажа'))

    RENT = morph_pipeline([
        "аренда",
        "сдается",
        "сдаем"]).interpretation(transactions.trans.const('Аренда'))

    type_of_trans = rule(or_(SALES, RENT)).interpretation(transactions)

    parser = Parser(type_of_trans)
    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    transactions = {}
    transactions['actions'] = {}
    transactions_names = []

    if matches:
        for match in matches:
            if match.fact.trans:
                transactions_names.append(match.fact.trans)
            else:
                transactions_names.append(not_data)
    else:
        transactions_names.append(not_data)

    transactions['actions']['name'] = transactions_names
    return transactions



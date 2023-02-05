from yargy import (
    rule, Parser
)
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline


def object_type_detection(s, OBJECT_TYPES):
    Obj = fact('Obj',
               ['name'])

    Object_type = morph_pipeline(
        OBJECT_TYPES
    ).interpretation(Obj.name.normalized())

    OBJECT_DEFINITION = rule(
        Object_type.interpretation(Obj.name),
    ).interpretation(Obj)

    parser = Parser(OBJECT_DEFINITION)

    matches = list(parser.findall(s))
    not_data = 'Нет данных'
    obj_type = {}
    object_types = []
    obj_type['obj_type'] = {}
    if matches:
        for match in matches:
            if match.fact.name:
                object_types.append(match.fact.name)
            else:
                object_types.append(not_data)
    else:
        object_types.append(not_data)

    obj_type['obj_type']['object'] = object_types
    return obj_type


import json

prelude = '''
from enum Import Enum
import attr

@attr.s
class Model(object):
    def serialize(self):
        return attr.asdict(self)
'''

class_template = '''
@attr.s
class {name}(Model):
'''

field_template = '    {} = attr.ib({}){}'

type_maps = {
    'string': 'str',
    'integer': 'int',
    'number': 'float',
    'boolean': 'bool',
    'object': 'dict',
    'array': 'list',
}

def def_to_code(name, definition):
    code = class_template.format(
        name=name,
    )
    if 'description' in definition:
        code += '    """{}"""\n'.format(definition['description'])
    for name, property in definition['properties'].items():
        args_code = []
        type = type_maps.get(property.get('type'))
        if name not in definition['required']:
            if type in ['list', 'object']:
                args_code += ['default=attr.Factory({})'.format(type)]
            else:
                args_code += ['default=None']
        type_comment = '  # type: ' + type if type else ''
        field_code = field_template.format(name, ', '.join(args_code), type_comment)
        code += field_code + '\n'
    return code + '\n'


def schema_to_code(schema):
    code = prelude
    for name, definition in schema['definitions'].items():
        code += def_to_code(name, definition)
    code += def_to_code(schema['title'], schema)
    return code


def main():
    with open('schema2.json', 'r') as fp:
        schema = json.load(fp)
    print(schema_to_code(schema))

main()

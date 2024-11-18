from marshmallow import Schema, fields, pre_load


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class CharacterSchema(Schema):
    name = fields.Str(required=True)
    universe = fields.Str(required=False, allow_none=True)
    education = fields.Str(required=False, allow_none=True)
    weight = fields.Float(required=False, allow_none=True)
    height = fields.Float(required=False, allow_none=True)
    identity = fields.Str(required=False, allow_none=True)
    other_aliases = fields.Str(required=False, allow_none=True)

    @pre_load
    def process_weight(self, data, **kwargs):
        if 'weight' in data:
            data['weight'] = parse_float(data['weight'])
        return data


class CharactersListSchema(Schema):
    result = fields.List(fields.Nested(CharacterSchema()), required=True)


class CharacterResponseSchema(Schema):
    result = fields.Nested(CharacterSchema(), required=True)


class DeleteResponseSchema(Schema):
    result = fields.List(fields.Str(), required=True)

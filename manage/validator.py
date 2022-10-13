from marshmallow import Schema, fields, ValidationError, validate, validates_schema
import re

dataTypes = ["double", "string", "object", "array", "binData", "undefined", "objectId", "bool", "date", "null", "regex", "dbPointer", "javascript", "symbol", "javascriptWithScope", "int", "timestamp", "long", "decimal", "minKey", "maxKey" ]

class stripName(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return value.replace(" ", '')
        except ValueError as error:
            raise ValidationError("Pin codes must contain only digits.") from error


class Validates(Schema):
    len_min = fields.Integer()
    len_max = fields.Integer()
    oneof = fields.List(fields.String())

class Fields(Schema):
    name = stripName()
    type = fields.String(validate=validate.OneOf(dataTypes), required=True)
    validate = fields.Nested(Validates)
    object = fields.List(fields.Nested(lambda: Fields()), required=False)

    @validates_schema
    def validate_required_fields(self, data, **kwargs):
        if data['type'] == "object" and "object" not in data:
            raise ValidationError('Missing fields object')

class collectionSchema(Schema):
    name = stripName()
    fields = fields.List(fields.Nested(Fields, required=True))
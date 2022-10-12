from marshmallow import Schema, fields, ValidationError, validate
import re


class PhoneNumber(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        rgxpattern = "^\+1[0-9]{10}$"
        regexp = re.compile(rgxpattern)
        if not regexp.match(value):
            msg = "Not a valid phone number."
            raise ValidationError(msg)

class Address(Schema):
    country = fields.String(required=True)
    state = fields.String(required=True)
    city = fields.String(required=True)

class UserSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=2))
    middle_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email()
    phone = PhoneNumber()
    password = fields.String(required=True)
    address = fields.Nested(Address, required=True)
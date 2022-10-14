from marshmallow import *
from marshmallow import validate

class fulladdressSchema(Schema):
    country = fields.String(required=True, )
    state = fields.String(required=False, )
    city = fields.String(required=False, )

                

class infoSchema(Schema):
    fulladdress = fields.Nested( fulladdressSchema,required=True, )
    gender = fields.String(required=True, validate = validate.OneOf(['Male', 'Female']))

                
class UserSchema(Schema):
    first_name = fields.String(required=False, )
    info = fields.Nested( infoSchema,required=False, )
    email = fields.Email(required=True, )

                
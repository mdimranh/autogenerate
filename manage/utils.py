import os
from dataclasses import fields

from __main__ import app

#
# from manage.urls import url_pattern
#
# for urls in url_pattern:
#     for url in urls:
#         app.add_url_rule(url[0], methods=url[1], view_func=url[2])

dataTypes = {
    "double": "Float",
    "string": "String",
    "object": "Dict",
    "array": "List",
    "objectId": "Dict",
    "bool": "Boolean",
    "date": "DateTime",
    "int": "Integer",
    "timestamp": "TimeDelta",
    "decimal": "Decimal",
    "email": "Email",
    "json": "Dict",
}

# validation schema generator

class formGenerate:
    def __init__(self, schema, coll):
        self.schema = schema
        self.coll = coll
        self.root = os.path.join(app.root_path, f'collection/{self.coll}')

        with open(os.path.join(self.root, "forms.py"), "w") as file:
            file.write(
                "from marshmallow import *\nfrom marshmallow import validate"
            )
        file.close()

    def generate(self):
        root = os.path.join(app.root_path, f'collection/{self.coll}')
        with open(os.path.join(root, "forms.py"), "a+") as file:
            file.write(
                f"""
class {self.coll}Schema(Schema):
{self.fields(self.schema['fields'])}
                """
            )

        return True

    def fields(self, data):
        fld = """"""
        for field in data:
            if 'validate' in field:
                validate_str = self.validator(field['validate'])
            else:
                validate_str = ''
            if field['type'] == 'json':
                fld+=f"    {field['name']} = fields.Nested( {self.dicts(field)},required={field['required']}, {validate_str})\n"
            elif field['type'] == 'object':
                fld+=f"    {field['name']} = fields.List(fields.Nested({self.dicts(field)},required={field['required']}))\n"
            else:
                fld+=f"    {field['name']} = fields.{dataTypes.get(field['type'])}(required={field['required']}, {validate_str})\n"

        return fld

    def dicts(self, data):
        with open(os.path.join(self.root, "forms.py"), "a") as file:
            file.write(
                f"""

class {data['name']}Schema(Schema):
{self.fields(data['object'])}
                """
            )
            file.close()
        return f"{data['name']}Schema"

    def validator(self, data):
        if "oneof" in data:
            validate = f"validate = validate.OneOf({data['oneof']})"
        else:
            validate = ''
        return validate



# api generator

class apiGenerate:
    def __init__(self, schema, coll):
        self.schema = schema
        self.coll = coll
        self.root = os.path.join(app.root_path, f'collection/{self.coll}')

        with open(os.path.join(self.root, "views.py"), "w") as file:
            file.write(
                """
from flask import *
from __main__ import app as mainapp
from .forms import *
                """
            )
        file.close()

    def getApi(self):
        with open(os.path.join(self.root, "views.py"), "a+") as file:
            file.write(
                f"""
@mainapp.route("/{self.coll.lower()}", methods=['GET'])
def get_{self.coll.lower()}():
    args = request.args.to_dict()
    return args

@mainapp.route("/{self.coll.lower()}", methods=['POST'])
def post_{self.coll.lower()}():
    data = request.json
    try:
        serialize = {self.coll}Schema().load(data)
        return serialize
    except:
        errors = {self.coll}Schema().validate(data)
        if errors:
            return errors, 422
                """
            )
        file.close()

    def generate(self):
        self.getApi()
        return True

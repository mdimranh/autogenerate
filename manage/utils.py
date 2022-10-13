from __main__ import app
from dataclasses import fields
import os
#
# from manage.urls import url_pattern
#
# for urls in url_pattern:
#     for url in urls:
#         app.add_url_rule(url[0], methods=url[1], view_func=url[2])



class formGenerate:
    def __init__(self, schema, coll):
        self.schema = schema
        self.coll = coll

    def generate(self):
        root = os.path.join(app.root_path, f'collections/{self.coll}')
        with open(os.path.join(root, "forms.py"), "w") as file:
            file.write(
                f"""
from marshmallow import *

class {self.coll}Schema(Schema):
{self.fields()}
                """
            )

    def fields(self):
        fld = """"""
        for field in self.schema['fields']:
            fld+=f"    {field['name']} = fields.{field['type']}\n"

        return fld
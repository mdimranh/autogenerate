import os

from __main__ import app
from flask import request

from .utils import apiGenerate, formGenerate
from .validator import collectionSchema

# class CreateCollection:
#     def __init__(self, name, fields):
#         self.name = name
#         self.fields = fields
#
#     def



@app.route("/generate/collection", methods=['POST'])
def generate_collection():
    data = request.json

    try:
        result = collectionSchema().load(data)

        root = os.path.join(app.root_path, 'collection')
        if not os.path.exists(os.path.join(root, result['name'])):
            os.makedirs(os.path.join(root, result['name']))
            formGenerate(result, result['name']).generate()
            apiGenerate(result, result['name']).generate()
        else:
            formGenerate(result, result['name']).generate()
            apiGenerate(result, result['name']).generate()
        folder = './collection'
        sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
        
        with open(os.path.join(app.root_path, 'collection/urls.py'), "w") as file:
            imp = """"""
            for folder in sub_folders:
                if folder != "__pycache__":
                    imp+=f"from collection.{folder} import views\n"
            file.write(imp)
        
    except:
        errors = collectionSchema().validate(data)
        if errors:
            return errors, 422

    return result



# @app.route("/generate/collection", methods=['POST'])
# def generate_collection():
#     data = request.json
#     root = app.root_path
#     if not os.path.exists(os.path.join(root, data['name'])):
#         os.makedirs(os.path.join(root, data['name']))
#         with open(os.path.join(root, "manage/settings.py"), "r") as in_file:
#             buf = in_file.readlines()
#
#         with open(os.path.join(root, "manage/settings.py"), "w") as out_file:
#             for line in buf:
#                 if line == "apps = [\n":
#                     line = line + f'    "{data["name"]}",\n'
#                 out_file.write(line)
#     apps_path = os.path.join(root, data['name'])
#     view_path = os.path.join(apps_path, 'views.py')
#     url_path = os.path.join(apps_path, 'urls.py')
#     form_path = os.path.join(apps_path, 'forms.py')
#     with open(view_path, 'w') as f:
#         f.write(
#             """
# from flask import Flask
#             """
#         )
#     with open(url_path, 'w') as f:
#         f.write(
#             f"""
# from {data['name']} import *
#             """
#         )
#     with open(form_path, 'w') as f:
#         f.write(
#             """
# from flask import Flask
#             """
#         )
#     return "SUCCESS", 201

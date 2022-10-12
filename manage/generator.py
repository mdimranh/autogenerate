from __main__ import app
import os

from flask import request

@app.route("/generate/app", methods=['POST'])
def makeApp():
    data = request.json
    root = app.root_path
    if not os.path.exists(os.path.join(root, data['name'])):
        os.makedirs(os.path.join(root, data['name']))
        with open(os.path.join(root, "manage/settings.py"), "r") as in_file:
            buf = in_file.readlines()

        with open(os.path.join(root, "manage/settings.py"), "w") as out_file:
            for line in buf:
                if line == "apps = [\n":
                    line = line + f'    "{data["name"]}",\n'
                out_file.write(line)
    apps_path = os.path.join(root, data['name'])
    view_path = os.path.join(apps_path, 'views.py')
    url_path = os.path.join(apps_path, 'urls.py')
    form_path = os.path.join(apps_path, 'forms.py')
    with open(view_path, 'w') as f:
        f.write(
            """
from flask import Flask
            """
        )
    with open(url_path, 'w') as f:
        f.write(
            f"""
from {data['name']} import *
            """
        )
    with open(form_path, 'w') as f:
        f.write(
            """
from flask import Flask
            """
        )
    return "SUCCESS", 201
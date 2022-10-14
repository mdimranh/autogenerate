
from flask import *
from __main__ import app as mainapp
from .forms import *
                
@mainapp.route("/user", methods=['GET'])
def get_user():
    args = request.args.to_dict()
    return args

@mainapp.route("/user", methods=['POST'])
def post_user():
    data = request.json
    try:
        serialize = UserSchema().load(data)
        return serialize
    except:
        errors = UserSchema().validate(data)
        if errors:
            return errors, 422
                
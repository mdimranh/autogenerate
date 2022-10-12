from flask import request
from .forms import UserSchema
from manage.databse import db
from werkzeug.security import generate_password_hash, check_password_hash

from bson import json_util

def registration():
    data = request.json
    errors = UserSchema().validate(data)
    if errors:
        return errors, 422
    else:
        if db['User'].find_one({"email": data['email']}):
            return {'error': "User already exists!"}, 409
        else:
            data['password'] = generate_password_hash(data['password'])
            db['User'].insert_one(data)
            user = db['User'].find_one({"email": data['email']})
            return json_util.dumps(user)

def test():
    return "test"


# @app.route('/api/login', methods =['POST'])
# def logins():
#     data = request.json
#     if not data or not data['email'] or not data['password']:
#         return {"error": "Data required"}, 401

#     user = db.user.find_one({'email': data['email']})

#     if not user:
#         return {"error": 'User does not exists !!'}, 403

#     if check_password_hash(user['password'], data['password']):
#         if not user['is_active']:
#             return jsonify({'message': 'User account is not activated! Please confirm user email.'}), 401
#         else:
#             token = jwt.encode({
#                 'id': str(user['_id']),
#                 'exp' : datetime.utcnow() + timedelta(minutes = 30)
#             }, app.config['SECRET_KEY'])
#             return make_response(jsonify({'token' : token}), 201)
#             # to_number = '+8801942504420'
#             # otp = random.randint(10000, 99999)
#             # message = client.messages \
#             #                     .create(
#             #                     body=f"Your PST verification code is {otp}. The code will expired in 5 minutes.",
#             #                     from_='+17377273468',
#             #                     to=to_number
#             #                     )
#             # if message.status == 'sent':
#             #     if OtpConfirm.objects(phone = to_number).first():
#             #         confirm = 
#             #     confirm = OtpConfirm()
            
#             # return jsonify({'sid': message.sid}), 201

#     return make_response(
#         'Could not verify',
#         403
#     )
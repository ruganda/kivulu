""" This module contains all the view functions for the auth blue print"""
from functools import wraps
import uuid
from flask import jsonify, request, session, make_response
from . import auth
from ..import event_object,rsvp_object,user_object
from ..models.user import USERS
import jwt
import datetime

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    """A route to handle user"""
    if request.method == 'POST':
        
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        # pass the details to the register method
        try:
            result = user_object.register(
            username, email, password, confirm_password)
            if result == "Registration successfull":
                return jsonify(response=result), 201
            else:
                return jsonify(response=result), 409
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    return jsonify(response="Get request currently not allowed"), 405


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        result = user_object.login(username, password)
        if result == "successful":                
            token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'hard to guess string')
            return jsonify({'token' : token.decode()})
        return result
    return jsonify(response="Get request currently not allowed"), 405

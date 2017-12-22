"""This module defines a user class and methods associated to it"""
#used to validate names
import re
import uuid
import jwt
from datetime import datetime, timedelta

USERS = []
class User_details(object):
    """ A class to handle activities related to a user"""
    # id = uuid.uuid1()
    def __init__(self):
        pass    
    
    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                'hard to guess string',
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, 'hard to guess string')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


    def register(self, username, email, password, confirm_password):
        """A method to register users with correct and valid details"""

        # empty dict to hold details of the user to be created
        user_details = {}
        # check if a user with that username exists
        for user in USERS :
            if username == user['username']:
                return "Username already exists."
                break
        else:
            #validate password and username
            if not re.match("^[a-zA-Z0-9_]*$", username):
                return "Username can only contain alphanumeric characters"
            elif password != confirm_password:
                return "passwords do not match"
            elif len(password) < 6:
                return "Password too short"     
            else:
                #register user if all the details are valid
                user_details['username'] = username
                user_details['email'] = email
                user_details['password'] = password
                user_details['id'] = id
                USERS .append(user_details)
                return "Registration successfull"

    def login(self,  username, password):
        """A method to register a user given valid user details"""
        for user in USERS :    
            if username == user['username']:
                if password == user['password']:
                    return "successful"
                else:
                    return "wrong password"
                    break
        return "user does not exist"

    def find_user_by_id(self, user_id):
        """ Retrieve a user given a user id"""
        for user in USERS :
            if user['id'] == user_id:
                return user
                break

        
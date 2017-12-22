from flask import request, jsonify, abort, make_response, current_app,session
from . import api
# from models.user import User
from ..import event_object, rsvp_object, user_object
import uuid
from functools import wraps
import jwt
from ..models.user import USERS

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, 'hard to guess string')
            for user in USERS:
                if user.get("username"):
                    current_user = user['username']= data['username']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         access_token = None
#         auth_header = request.headers.get('Authorization')
#         access_token = auth_header.split(" ")[1]

#         # if 'x-access-token' in request.headers:
#         #     access_token = request.headers['x-access-token']

#         if not access_token:
#             return jsonify({'message' : 'Token is missing!'}), 401

#         try: 
#             # data = jwt.decode(access_token, 'hard to guess string')
#             current_user = user_object.decode_token(access_token)
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated


@api.route('/events', methods=['GET', 'POST'])
@token_required
def events(current_user):
    for user in USERS:     
        if request.method == 'POST':
            try:
                if current_user == user['username']:
                    event_data = request.get_json()
                    name = event_data['name']
                    description = event_data['description']
                    category = event_data['category']
                    location = event_data['location']
                    event_date = event_data['event_date']
                    createdby = current_user
                    result = event_object.create(
                        name, description, category, location, event_date, createdby)
                    if result == "event created":
                        return jsonify(response=result), 201
                    else:
                        return jsonify(response=result), 409
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401    
        if current_user != "Expired token. Please log in to get a new token" or current_user != "Invalid token. Please register or login":
            events = event_object.view_all()
            return jsonify(events), 200
    

@api.route('/events/<eventid>', methods=['PUT'])
@token_required
def update_event(current_user,eventid):
    """A route to handle event updates"""
    if not  current_user:
        abort(404)
    eventid = uuid.UUID(eventid)
    event_data = request.get_json()
    name = event_data['name']
    description = event_data['description']
    category = event_data['category']
    location = event_data['location']
    event_date = event_data['event_date']
    createdby = event_data['createdby']
    result = event_object.update(
        eventid, name, description, category, location, event_date, createdby)
    if result == "update success":
        return jsonify(response=result), 200
    elif result == "no event with given id":
        return jsonify(response=result), 404
    else:
        return jsonify(response=result), 409

@api.route('/events/<eventid>', methods=['DELETE'])
@token_required
def delete_event(current_user,eventid):
    """A route to handle deletion of events"""
    if not  current_user:
        abort(404)
    eventid = uuid.UUID(eventid)
    result = event_object.delete(eventid)
    if result == "deleted":
        return jsonify(response="event deleted"),  204
    return jsonify(response=result), 404

@api.route('/events/<eventid>', methods=['GET'])
@token_required
def get_one_event(current_user,eventid):
    """A route to handle event updates"""
    if not  current_user:
        abort(404)
    eventid = uuid.UUID(eventid)
    event = event_object.find_by_id(eventid)
    return jsonify(event), 200
    

@api.route('/events/<eventid>/rsvp', methods=['GET', 'POST'])
@token_required
def rsvps(current_user,eventid):
    
    """A route for registering a user to an event"""
    eventid = uuid.UUID(eventid)
    if request.method == 'POST':
        userid = current_user
        result = rsvp_object.create(eventid, userid)
        if result == "rsvp success":
            return jsonify(response=result), 201
        return jsonify(response=result), 409
    userids = rsvp_object.view_rsvp(eventid)
    users = [user for user in USERS if user['id'] in userids]
    return jsonify(users), 200

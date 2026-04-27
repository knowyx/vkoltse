"""This module contains api resources for working with users"""
from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.db_session import create_session
from data.users import Users


def abort_if_user_not_found(user_id):  
    """function for checking if user exists"""
    session = db_session.create_session()
    user = session.get(Users, user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


parser = (
    reqparse.RequestParser()
)  # parser for parsing request data for creating and updating users
parser.add_argument("permissions", required=True, type=str)
parser.add_argument("email", required=True, type=str)
parser.add_argument("login", required=True, type=str)
parser.add_argument("password", required=True, type=str)


class UsersResource(
    Resource
):  
    """resource for working with users, supports GET, DELETE and PUT methods"""
    def get(self, user_id):
        """returns user with the specified id, represented as a dictionary with id, 
        permissions, email and login information, if user with the specified id does 
        not exist, returns 404 error"""
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.get(Users, user_id)
        data = user.to_dict()
        return jsonify({"user": data})

    def put(self, user_id):
        """updates user with the specified id in the database, expects permissions, 
        email, login and password in the request data, if user with the specified 
        id does not exist, returns 404 error, otherwise returns success message"""
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.get(Users, user_id)

        args = parser.parse_args()
        user.permissions = args["permissions"]
        user.email = args["email"]
        user.login = args["login"]
        if args.get("password"):
            user.set_password(args["password"])

        session.commit()
        return jsonify({"success": "Ok"})

    def delete(self, user_id):
        """deletes user with the specified id from the database, if user with the 
        specified id does not exist, returns 404 error, otherwise returns success 
        message"""
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.get(Users, user_id)
        session.delete(user)
        session.commit()
        return jsonify({"success": "Ok"})


class UserListResource(
    Resource
):  
    """resource for working with users list, supports GET and POST methods"""
    def get(self):
        """returns a list of all users in the database, each user is represented 
        as a dictionary with id, permissions, email and login information"""
        session = create_session()
        users = session.query(Users).all()
        return jsonify(
            {
                "users": [
                    item.to_dict(only=("id", "permissions", "email", "login"))
                    for item in users
                ]
            }
        )

    def post(self):
        """creates a new user in the database, expects permissions, email, login 
        and password in the request data, returns the id of the created user, 
        if user with the same login already exists, returns error message"""
        args = parser.parse_args()
        session = create_session()

        if session.query(Users).filter_by(login=args["login"]).first():
            return jsonify({"error": "Login already exists"}), 400

        user = Users(
            permissions=args["permissions"], email=args["email"], login=args["login"]
        )
        user.set_password(args["password"])
        session.add(user)
        session.commit()

        return jsonify({"id": user.id}), 201

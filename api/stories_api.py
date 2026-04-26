# Thise module contains api resources for working with stories
from datetime import datetime

from data.db_session import create_session
from data.stories import Stories
from flask import jsonify
from flask_restful import Resource, abort, reqparse


def str_to_datetime(
    value,
):  # function for parsing date from string, expected format: YYYY-MM-DDTHH:MM:SS
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("Неверный формат даты, ожидается YYYY-MM-DDTHH:MM:SS")


def abort_if_not_exist(story_id):  # function for checking if story exists
    session = create_session()
    story = session.get(Stories, story_id)
    if not story:
        abort(404, message=f"Story {story_id} not found")


parser = (
    reqparse.RequestParser()
)  # parser for parsing request data for creating and updating stories
parser.add_argument("content", required=True, type=str)
parser.add_argument("title", required=True, type=str)
parser.add_argument("author_id", required=True, type=int)
parser.add_argument("review_authors_id", required=True, type=int)
parser.add_argument("date", required=True, type=str_to_datetime)
parser.add_argument("checked", required=True, type=int)


class StoriesResource(
    Resource
):  # resource for working with stories, supports GET, DELETE and PUT methods
    def get(self, story_id):
        # returns story with the specified id, represented as a dictionary with id, content, title, author_id, review_authors_id, date and checked information, if story with the specified id does not exist, returns 404 error
        abort_if_not_exist(story_id)
        session = create_session()
        story = session.get(Stories, story_id)
        data = story.to_dict()
        return jsonify({"story": data})

    def put(self, story_id):
        # updates story with the specified id in the database, expects content, title, author_id, review_authors_id, date and checked in the request data, if story with the specified id does not exist, returns 404 error, otherwise returns success message
        abort_if_not_exist(story_id)
        session = create_session()
        story = session.get(Stories, story_id)

        args = parser.parse_args()
        story.content = args["content"]
        story.title = args["title"]
        story.author_id = args["author_id"]
        story.review_authors_id = args["review_authors_id"]
        story.date = args["date"]
        story.checked = args["checked"]

        session.commit()
        return jsonify({"story": "Ok"})

    def delete(self, story_id):
        # deletes story with the specified id from the database, if story with the specified id does not exist, returns 404 error, otherwise returns success message
        abort_if_not_exist(story_id)
        session = create_session()
        story = session.get(Stories, story_id)
        session.delete(story)
        session.commit()

        return jsonify({"success": "Ok"})


class StoriesListResource(
    Resource
):  # resource for working with stories list, supports GET and POST methods
    def get(self):
        # returns a list of all stories in the database, each story is represented as a dictionary with id, content, title, author_id, review_authors_id, date and checked information
        session = create_session()
        stories = session.query(Stories).all()
        return jsonify({"stories": [s.to_dict() for s in stories]})

    def post(self):
        # creates a new story in the database, expects content, title, author_id, review_authors_id, date and checked in the request data, returns the id of the created story
        args = parser.parse_args()
        session = create_session()

        story = Stories(
            content=args["content"],
            title=args["title"],
            author_id=args["author_id"],
            review_authors_id=args["review_authors_id"],
            date=args["date"],
            checked=args["checked"],
        )
        session.add(story)
        session.commit()
        return jsonify({"id": story.id}), 201

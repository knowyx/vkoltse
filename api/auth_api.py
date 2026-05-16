"""Authentication helpers for API resources.

Provides a small token/session based auth utility that reads a session key from
the `Authorization: Bearer <key>` header and resolves the corresponding `Users`
record via the `Sessions` table. Also exposes a `require_auth` decorator for
protecting resource methods.
"""

from functools import wraps

from flask import request
from flask_restful import abort

from data.db_session import create_session
from data.sessions import Sessions
from data.users import Users


def _get_session_from_request():
	"""Extract bearer token from Authorization header and return Sessions row."""
	auth = request.headers.get("Authorization")
	if not auth:
		return None
	parts = auth.split()
	if len(parts) != 2 or parts[0].lower() != "bearer":
		return None
	token = parts[1]
	session = create_session()
	return session.query(Sessions).filter(Sessions.session_key == token).first()


def get_user_from_request():
	"""Return Users instance from request Authorization header, or None."""
	sess = _get_session_from_request()
	if not sess:
		return None
	db = create_session()
	return db.get(Users, sess.user_id)


def require_auth(allow_same_user=False, require_admin=False):
	"""Decorator for Flask-RESTful resource methods.

	- If `require_admin` is True, user must have non-zero/truthy `permissions`.
	- If `allow_same_user` is True and the request contains `user_id` either in
	  `view_args` (path param) or parsed JSON/form data, the owner may act on
	  their own resources even without admin permissions.
	"""

	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			sess = _get_session_from_request()
			if not sess:
				abort(401, message="Authentication required")

			db = create_session()
			user = db.get(Users, sess.user_id)
			if user is None:
				abort(401, message="Invalid session")

			# admin check
			if require_admin:
				# treat '0' or empty as non-admin
				if not user.permissions or str(user.permissions) == "0":
					abort(403, message="Admin permissions required")

			# owner check: look for user_id in kwargs (path) or in json/form
			if allow_same_user and not require_admin:
				target_id = None
				if "user_id" in kwargs:
					target_id = kwargs.get("user_id")
				else:
					try:
						data = request.get_json(silent=True) or {}
						target_id = data.get("user_id")
					except Exception:
						target_id = None
				if target_id is not None and int(target_id) == int(user.id):
					return func(*args, **kwargs)

			# if we got here and require_admin is False, allow any authenticated user
			if not require_admin:
				return func(*args, **kwargs)

			# otherwise require_admin was True and we've already checked admin above
			return func(*args, **kwargs)

		return wrapper

	return decorator


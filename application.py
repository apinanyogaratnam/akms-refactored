from flask_migrate import Migrate
from flask import request

from app import create_app, db

from app.models.users import Users
from app.models.api_keys import ApiKeys
from app.models.projects import Projects
from app.models.user_projects import UserProjects

from functools import wraps

from akms_hash import hash_api_key
from uuid import uuid4

import os


def is_valid_api_key(api_key: str) -> bool:
    hashed_api_key = hash_api_key(api_key, api_key)
    result = (
        ApiKeys.query_active_api_keys().filter_by(hashed_api_key=hashed_api_key).first()
    )
    return result is not None


def authenticate(auth_type=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if auth_type == "internal":
                api_key = request.headers.get("X-API-KEY")
                if api_key == os.environ.get("API_KEY"):
                    return func(*args, **kwargs)
                    # api_key = ApiKeys.query.filter_by(api_key=api_key).first()
                    # if api_key:
                    #     return func(*args, **kwargs)
                return {
                    "status": 401,
                    "message": "Unauthorized",
                }, 401
            else:
                api_key = request.headers.get("X-API-KEY")
                if api_key and is_valid_api_key(api_key):
                    return func(*args, **kwargs)
                return {
                    "status": 401,
                    "message": "Unauthorized",
                }, 401

        return wrapper

    return decorator


app = create_app()
migrate = Migrate(app, db)


@app.route("/")
def index():
    return {
        "pid": os.getpid(),
        "status": 200,
    }, 200


@app.get("/users/<string:email>")
@authenticate("internal")
def get_user(email: str) -> dict:
    user = Users.query_active_users().filter_by(email=email).first()
    if not user:
        return {
            "user": None,
            "status": 404,
            "message": "User not found",
        }, 200

    return {
        "user": user.to_dict(),
        "status": 200,
    }, 200


@app.route("/users")
@authenticate("internal")
def users():
    return {
        "users": [user.to_dict() for user in Users.query_active_users().all()],
        "status": 200,
    }, 200


@app.post("/users")
@authenticate("internal")
def create_user():
    data = request.get_json()
    email = data.get("email")
    name = data.get("name")

    if not email:
        return {
            "status": 400,
            "message": "Missing required field: email",
        }, 400

    if not name:
        return {
            "status": 400,
            "message": "Missing required field: name",
        }, 400

    user = Users.query_active_users().filter_by(email=email).first()
    if user:
        return {
            "status": 409,
            "message": "User with this email already exists",
        }, 409

    user = Users(email=email, name=name)
    db.session.add(user)
    db.session.commit()

    return {
        "user": user.to_dict(),
        "status": 200,
    }, 200


@app.route("/users/<int:user_id>/create-api-key", methods=["POST"])
@authenticate("internal")
def create_api_key(user_id: int) -> dict:
    body = request.get_json()
    generated_api_key = str(uuid4())
    hashed_api_key = hash_api_key(generated_api_key, generated_api_key)
    name = body.get("name")
    description = body.get("description")

    if not name:
        return {
            "status": 400,
            "message": "Missing required field: name",
        }, 400

    api_key = ApiKeys(
        user_id=user_id,
        hashed_api_key=hashed_api_key,
        name=name,
        description=description,
    )

    db.session.add(api_key)
    db.session.commit()

    return {
        "api_key": generated_api_key,
        "status": 200,
    }, 200


@app.route("/users/<int:user_id>/api-keys")
@authenticate("internal")
def get_api_keys(user_id: int) -> dict:
    api_keys = ApiKeys.query_active_api_keys().filter_by(user_id=user_id).all()
    serialized_api_keys = [api_key.to_dict() for api_key in api_keys]
    return {
        "api_keys": serialized_api_keys,
        "status": 200,
    }, 200


@app.route("/users/<int:user_id>/api-keys/<int:api_key_id>", methods=["PUT"])
@authenticate("internal")
def update_api_key(user_id: int, api_key_id: int) -> dict:
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")

    if not name:
        return {
            "status": 400,
            "message": "Missing required field: name",
        }, 400

    api_key = ApiKeys.query.filter_by(id=api_key_id, user_id=user_id).first()
    api_key.name = name
    api_key.description = description

    db.session.commit()

    return {
        "api_key": api_key.to_dict(),
        "status": 200,
    }, 200


@app.route("/users/<int:user_id>/api-keys/<int:api_key_id>", methods=["DELETE"])
@authenticate("internal")
def delete_api_key(user_id: int, api_key_id: int) -> dict:
    api_key = ApiKeys.query.filter_by(id=api_key_id, user_id=user_id).first()
    api_key.is_deleted = True

    db.session.commit()

    return {
        "status": 200,
    }, 200


@app.route("/validate-api-key", methods=["POST"])
def validate_api_key() -> dict:
    body = request.get_json()
    api_key = body.get("api_key")
    user_id = body.get("user_id")

    if not api_key or not user_id:
        return {
            "status": 400,
            "message": "Missing required field: api_key or user_id",
        }, 400

    hashed_api_key = hash_api_key(api_key, api_key)

    api_key = db.session.query(ApiKeys.id).filter_by(
        user_id=user_id, hashed_api_key=hashed_api_key
    ).first()

    if api_key:
        return {
            "status": 200,
            "message": "Valid API Key",
            "is_valid": True,
        }, 200

    return {
        "status": 401,
        "message": "Unauthorized",
        "is_valid": False,
    }, 401


@app.post("/users/<int:user_id>/projects")
def create_project(user_id: int) -> dict:
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")
    website = body.get("website")
    logo_url = body.get("logo_url")

    if not name or not description:
        return {
            "status": 400,
            "message": "Missing required fields: name and description",
        }, 400

    project = Projects(name=name, description=description, website=website, logo_url=logo_url)

    db.session.add(project)

    db.session.flush()

    user_project = UserProjects(user_id=user_id, project_id=project.id)

    db.session.add(user_project)


    return {
        "project": project.to_dict(),
        "status": 200,
    }, 200

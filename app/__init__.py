from flask import Flask

from app.extensions import db, cors
from dotenv import load_dotenv

import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# hosts
local_host = 'localhost'
docker_host = 'host.docker.internal'
production_host = os.environ.get('POSTGRES_HOST')

# credentials
local_user = 'postgres'
production_user = os.environ.get('POSTGRES_USER')
local_password = 'postgres'
production_password = os.environ.get('POSTGRES_PASSWORD')
local_db = 'postgres'
production_db = os.environ.get('POSTGRES_DB')

# set current credentials
current_host = production_host
current_user = production_user
current_password = production_password
current_db = production_db


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{current_user}:{current_password}@{current_host}:5432/{current_db}" # noqa: E501
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    cors.init_app(app)
    return app

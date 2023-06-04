from flask import Flask

from app.extensions import db, cors
from dotenv import load_dotenv

import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

local = 'localhost'
docker = 'host.docker.internal'
current_host = local
class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@{current_host}:5432/postgres" # noqa: E501
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    cors.init_app(app)
    return app

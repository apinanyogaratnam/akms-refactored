from flask_migrate import Migrate

from app import create_app, db

from app.models.user import Users
from app.models.api_key import ApiKeys

import os

app = create_app()
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {
        'pid': os.getpid(),
    }

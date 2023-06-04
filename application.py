from flask_migrate import Migrate

from app import create_app, db

from app.models.user import User

import os

app = create_app()
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {
        'pid': os.getpid(),
    }

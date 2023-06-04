from datetime import datetime, timezone
from app import db

from sqlalchemy import false
from sqlalchemy.dialects.postgresql import TIMESTAMP


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False, index=True)

    is_deleted = db.Column(db.Boolean, default=False, server_default=false(), nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), default=datetime.now(tz=timezone.utc), server_default=db.func.now(), nullable=False)

    @classmethod
    def query(cls):
        return super(User, cls).query.filter_by(is_deleted=False)

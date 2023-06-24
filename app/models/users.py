from datetime import datetime, timezone
from app import db

from sqlalchemy import false
from sqlalchemy.dialects.postgresql import TIMESTAMP


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False, index=True)

    is_deleted = db.Column(
        db.Boolean, default=False, server_default=false(), nullable=False
    )
    created_at = db.Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
        server_default=db.func.now(),
        nullable=False,
    )
    updated_at = db.Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
        server_default=db.func.now(),
        onupdate=datetime.now(tz=timezone.utc),
        nullable=False,
    )

    @classmethod
    def query_active_users(cls):
        return cls.query.filter_by(is_deleted=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "project_id": self.company_id,
        }

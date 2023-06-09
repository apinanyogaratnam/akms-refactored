from datetime import datetime, timezone
from app import db

from sqlalchemy import UUID, false
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.models.projects import Projects


class ApiKeys(db.Model):
    __tablename__ = "api_keys"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    hashed_api_key = db.Column(db.Text, nullable=False, index=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{Projects.__tablename__}.id"), nullable=False)

    is_deleted = db.Column(
        db.Boolean, default=False, server_default=false(), nullable=False
    )
    created_at = db.Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
        server_default=db.func.now(),
        nullable=False,
    )

    @classmethod
    def query_active_api_keys(cls):
        return cls.query.filter_by(is_deleted=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
        }

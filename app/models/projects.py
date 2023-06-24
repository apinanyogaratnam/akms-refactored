from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, UUID, false
from app import db


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, server_default=db.text("gen_random_uuid()"))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.Text, nullable=True)

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
    def query_active_projects(cls):
        return cls.query.filter_by(is_deleted=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "website": self.website,
            "logo_url": self.logo_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

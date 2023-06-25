from sqlalchemy import UUID, UniqueConstraint
from app import db
from app.models.projects import Projects
from app.models.users import Users


class UserProjects(db.Model):
    __tablename__ = "user_projects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(f"{Users.__tablename__}.id"), nullable=False, index=True
    )
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{Projects.__tablename__}.id"), nullable=False, index=True)

    UniqueConstraint(user_id, project_id, name="user_projects_user_id_project_id_key")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
        }

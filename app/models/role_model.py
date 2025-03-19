import uuid
from app.utils.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.id = str(uuid.uuid4()) 
        self.name = name

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter(Role.name.ilike(name)).first()

    @staticmethod
    def ensure_roles_exist():
        role_names = ["ADMIN", "USER", "STAFF", "MANAGER"]
        for role_name in role_names:
            if not Role.get_role_by_name(role_name):
                db.session.add(Role(name=role_name))
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

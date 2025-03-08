from app.utils.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

from .. import db

class UserGroup(db.Model):
    """ UserGroup Model for storing user group related details """
    __tablename__ = "user_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupName = db.Column(db.String(255), unique=True, nullable=False)
    createdAt  = db.Column(db.DateTime, nullable=False)
    updatedAt  = db.Column(db.DateTime, nullable=False)
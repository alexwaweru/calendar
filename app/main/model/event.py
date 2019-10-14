from .. import db

class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createdByEmail = db.Column(db.String(255), unique=False, nullable=False)
    eventDateAndTime = db.Column(db.DateTime, nullable=False)
    timeFormat = db.Column(db.String, unique=False, nullable=False)
    attendees = db.Column(db.Text , unique=False, nullable=False)
    createdAt = db.Column(db.String, unique=False, nullable=False)
    updatedAt = db.Column(db.String, unique=False, nullable=False)

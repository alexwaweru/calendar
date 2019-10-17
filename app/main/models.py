from create_app_factory import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(255), unique=False, nullable=False)
    lastName = db.Column(db.String(255), unique=False, nullable=False) 
    country = db.Column(db.String(255), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(255), unique=True, nullable=False)
    userGroup  = db.Column(db.String(255), unique=False, nullable=False)
    createdAt  = db.Column(db.DateTime, nullable=False)
    updatedAt  = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'User: { firstname: %s, lastname: %s, email: %s }' %(self.firstName, self.lastName, self.email)


class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventName = db.Column(db.String(255), unique=False, nullable=False)
    createdByEmail = db.Column(db.String(255), unique=False, nullable=False)
    eventDateAndTime = db.Column(db.String(255), unique=False, nullable=False)
    attendees = db.Column(db.Text , unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Event: { eventName: %s, DateTime: %s}' %(self.eventName, self.eventDateAndTime)



class UserGroup(db.Model):
    """ UserGroup Model for storing user group related details """
    __tablename__ = "user_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupName = db.Column(db.String(255), unique=True, nullable=False)
    createdAt  = db.Column(db.DateTime, nullable=False)
    updatedAt  = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'UserGroup: { groupName: %s }' %(self.groupName)

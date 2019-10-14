from .. import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(255), unique=False, nullable=False)
    lastName = db.Column(db.String(255), unique=False, nullable=False) 
    country = db.Column(db.String(255), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(255), unique=True, nullable=False)
    legalName = db.Column(db.String(255), unique=False, nullable=False)
    businessLegalEntity  = db.Column(db.String(255), unique=False, nullable=False)
    businessLegalEntityOrg  = db.Column(db.String(255), unique=False, nullable=False)
    insurerRepresenting  = db.Column(db.String(255), unique=False, nullable=False)
    insurerAdminEmail  = db.Column(db.String(255), unique=False, nullable=False)
    userType  = db.Column(db.String(255), unique=False, nullable=False)
    emailConfirmed  = db.Column(db.Boolean, nullable=False)
    phoneConfirmed  = db.Column(db.Boolean, nullable=False)
    profileComplete  = db.Column(db.Boolean, nullable=False)
    isActive  = db.Column(db.Boolean, nullable=False)
    createdAt  = db.Column(db.String(255), unique=False, nullable=False)
    updatedAt  = db.Column(db.String(255), unique=False, nullable=False)
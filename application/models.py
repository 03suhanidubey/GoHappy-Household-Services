from .database import db

class Customers(db.Model):
    userid=db.Column(db.Integer(), nullable=False, primary_key=True)
    fullname=db.Column(db.String(), nullable=False)
    contactno=db.Column(db.Integer(), nullable=False)
    emailid=db.Column(db.String(), nullable=False, unique = True)
    pswd=db.Column(db.String(), nullable=False)
    address=db.Column(db.String(), nullable=False)
    searchaddress=db.Column(db.String(), nullable=False)
    pincode=db.Column(db.Integer(), nullable=False)
    servicerequest = db.relationship('Servicerequest', backref='customers')

class Professionals(db.Model):
    userid=db.Column(db.Integer(), nullable=False, primary_key=True)
    fullname=db.Column(db.String(), nullable=False)
    contactno=db.Column(db.Integer(), nullable=False)
    emailid=db.Column(db.String(), nullable=False, unique = True)
    pswd=db.Column(db.String(), nullable=False)
    service=db.Column(db.String(), nullable=False)
    experience=db.Column(db.Integer(), nullable=False)
    address=db.Column(db.String(), nullable=False)
    searchaddress=db.Column(db.String(), nullable=False)
    pincode=db.Column(db.Integer(), nullable=False)
    avg_rating=db.Column(db.Float(), nullable=True)
    docs=db.Column(db.String, nullable=True)
    rating_sum=db.Column(db.Integer(), nullable=True)
    ratings_count=db.Column(db.Integer(), nullable=True)
    active=db.Column(db.String(), nullable=False)
    servicerequest = db.relationship('Servicerequest', backref='professionals')

class Servicerequest(db.Model):
    bookingid=db.Column(db.Integer(), primary_key=True)
    custid=db.Column(db.String(), db.ForeignKey("customers.userid"), nullable=False)
    profesid=db.Column(db.String(), db.ForeignKey("professionals.userid"), nullable=False)
    datecreated=db.Column(db.String(), nullable=False)
    datecompleted=db.Column(db.String(), nullable=True)
    status=db.Column(db.String(), nullable=False)
    ratings=db.Column(db.Float(), nullable=True)
    remarks=db.Column(db.String(), nullable=True)

class Services(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(), nullable=False)
    baseprice=db.Column(db.Integer(), nullable=False)
    descr=db.Column(db.String(), nullable=False)
    searchdescr=db.Column(db.String(), nullable=False)
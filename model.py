from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
 
#creating database models


class User(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    fullname=db.Column(db.String(),nullable=False)
    contact_no=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(),nullable=False)

class Admin(db.Model):
    __tablename__="admin"
    admin_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)

class Service(db.Model):
    __tablename__="service"
    service_id=db.Column(db.Integer,primary_key=True)
    service_name=db.Column(db.String(),unique=True,nullable=False)
    service_price=db.Column(db.String(),nullable=False)
    service_time_required=db.Column(db.String(),nullable=False)
    service_description=db.Column(db.String(),nullable=True)

class Professional(db.Model):
    __tablename__="professional"
    pr_id=db.Column(db.Integer,primary_key=True)
    pr_user_name=db.Column(db.String(),unique=True,nullable=False)
    pr_password=db.Column(db.String(),nullable=False)
    pr_fullname=db.Column(db.String(),unique=True,nullable=False)
    pr_service_name=db.Column(db.String(),db.ForeignKey('service.service_name'),nullable=False)
    pr_experience=db.Column(db.String(),nullable=False)
    pr_contact_no=db.Column(db.Integer,nullable=False)
    pr_address=db.Column(db.String(),nullable=False)
    pr_pincode=db.Column(db.Integer,nullable=False)
    pr_status=db.Column(db.String(),nullable=False)
    service = db.relationship('Service',backref='professional',lazy=True)


class Service_requests(db.Model):
    __tablename__="service_requests"
    id = db.Column(db.Integer,primary_key=True)
    service_id =db.Column(db.Integer,db.ForeignKey('service.service_id'),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey('professional.pr_id'),nullable=True)
    date_of_request=db.Column(db.Date,nullable=False)
    date_of_completion=db.Column(db.Date,nullable=True)
    service_status=db.Column(db.String(10))
    remarks=db.Column(db.String(),nullable=True)
    customer = db.relationship('User', backref='service_requests')
    service = db.relationship('Service',backref='service_requests') 
    professional = db.relationship('Professional',backref='service_requests')
    

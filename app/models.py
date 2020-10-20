from app import db, login_manager
from flask_login import UserMixin
########
import os
import base64
import onetimepass
# pip install onetimepass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    useremail = db.Column(db.String(120), unique=True, nullable=False)
    useraddr = db.Column(db.String(200), nullable=False)
    userpwd = db.Column(db.String(60), nullable=False)
    usertlf = db.Column(db.Integer(), unique=True,  nullable=False)
    accounts = db.relationship('Account',  backref='holder', lazy=True)
    logs = db.relationship('Log', backref='logger', lazy=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8') #Generate a random secret
        
    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Banken:{0}?secret={1}&issuer=2FA-Banken' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.useremail}', '{self.useraddr}', '{self.usertlf}', '{self.accounts}','{self.logs}')"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accname = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float)
    accuser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"account('{self.accname}', '{self.balance}', '{self.accuser}')"

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loguser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logfrom = db.Column(db.String(20), nullable=False)
    logto = db.Column(db.String(20), nullable=False)
    logsum = db.Column(db.Float , nullable=False)
    logtime = db.Column(db.String(20), nullable=False) 

    def __repr__(self):
        return f"log('{self.logfrom}','{self.logto}','{self.logsum}','{self.logtime}')"



def createaccs(user):
    acc1 = Account(accname="Brukerkonto", balance=10000, accuser=user)
    acc2 = Account(accname="Sparekonto", balance=100000, accuser=user)
    db.session.add(acc1)
    db.session.add(acc2)
    db.session.commit()

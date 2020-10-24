from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError, Optional
from app.models import User, Account, Log
import phonenumbers as pn
import re

class RegistrationForm(FlaskForm):
    username = StringField('Brukernavn', validators=[Required(), Length(min=5, max=20)])
    email = StringField('Email', validators= [Required(), Email()])
    password = PasswordField('Passord', validators=[Required(), Length(min=12, max=64)])
    confirm_password = PasswordField('Bekreft Passord', validators=[Required(), EqualTo('password')])
    tlf = StringField('Telefonnummer', validators=[Required()])
    addr = StringField('Addresse', validators=[Required(), Length(min=5)])
    submit = SubmitField('Registrer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dette brukernavnet er allerede i bruk, vennligst bruk et annet brukernavn')

    def validate_email(self, email):
        user = User.query.filter_by(useremail=email.data).first()
        if user:
            raise ValidationError('Denne epost addressen er allerede i bruk, vennligst bruk en annen epost')

    def validate_tlf(self, tlf):
        user = User.query.filter_by(usertlf=tlf.data).first()
        if user:
            raise ValidationError('Dette telefonnummeret er allerede i bruk, vennligst bruk et annet telefonnummer')
        if len(str(tlf.data)) >= 9 or len(str(tlf.data)) <= 7:
         raise ValidationError('telefonnummeret må ha 8 siffer')
        number = pn.parse(tlf.data, "NO")
        if not pn.is_possible_number(number):
            raise ValidationError('telefonnummeret må ha 8 siffer, og være et mulig telefonnummer')
    
    def validate_password(self, password):
        password = password.data
        message = 'Your password should have at least an uppercase, lowercase, special character: [_,@,$,!,?] and a number character.'
        #Check for lowercase character
        if not re.findall('.*[a-z].*', password):
            raise ValidationError(message)
        #Check for uppercase character
        if not re.findall('.*[A-Z].*', password):
            raise ValidationError(message)
        #Check for number character
        if not re.findall('.*[0-9].*', password):
            raise ValidationError(message)
        #Check for special characters
        if not re.findall('.*[_@$!?].*', password):
            raise ValidationError(message)


class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[Required(), Length(min=5, max=20)])
    password = PasswordField('Passord', validators=[Required(), Length(min=8)])
    token = StringField('Token (2FA)', validators=[Required(), Length(6, 6)])
    submit = SubmitField('Logg inn')

    def validate_token(self, token):
        token = token.data
        if len(str(token)) != 6:
            raise ValidationError("error")
        if re.findall('.*[_@$!?].*', token):
            raise ValidationError()
        if re.findall('.*[a-z].*', token):
            raise ValidationError()
        if re.findall('.*[A-Z].*', token):
            raise ValidationError()

class Editform(FlaskForm):
    email = StringField('Email', validators= [Email() , Optional()])
    tlf = StringField('Telefonnummer', validators=[Optional()])
    addr = StringField('Addresse', validators=[Length(min=5), Optional()])
    submit = SubmitField('Endre opplysninger')

    def validate_email(self, email):
        user = User.query.filter_by(useremail=email.data).first()
        if user:
            raise ValidationError('Denne epost addressen er allerede i bruk, vennligst bruk en annen epost')

    def validate_tlf(self, tlf):
        user = User.query.filter_by(usertlf=tlf.data).first()
        if user:
            raise ValidationError('Dette telefonnummeret er allerede i bruk, vennligst bruk et annet telefonnummer')
        if len(str(tlf.data)) >= 9 or len(str(tlf.data)) <= 7:
         raise ValidationError('telefonnummeret må ha 8 siffer')
        number = pn.parse(tlf.data, "NO")
        if not pn.is_possible_number(number):
            raise ValidationError('telefonnummeret må ha 8 siffer, og være et mulig telefonnummer')

class Transferform(FlaskForm):
    tfrom = SelectField('Velg Konto: ')
    tto = SelectField('Overfør til: ', validators=[Required()])
    tsum = StringField('Sum', validators=[Required()])
    submit = SubmitField('Bekreft overføring')

    def validate_tsum(self,tsum):
        user_id = current_user.get_id()
        acc = Account.query.filter_by(accuser=user_id,accname=self.tfrom.data).first()
        try:
            float(tsum.data)
        except ValueError:
            raise ValidationError('Ikke en gyldig sum')
        if acc.balance<float(tsum.data):
            raise ValidationError('Du har ikke nokk penger til å overføre denne mengden')
        if float(tsum.data)<0:
            raise ValidationError('Ikke en gyldig sum')

    def getchoices(self):
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        usersTo = User.query.all()
        self.tfrom.choices = [(acc.accname,acc.accname) for acc in user.accounts]
        self.tto.choices = [(u.username,u.username) for u in usersTo]


class Transferlocalform(FlaskForm):
    tfrom = SelectField('Velg Konto: ')
    tto = SelectField('Velg Konto: ')
    tsum = StringField('Sum', validators=[Required()])
    submit = SubmitField('Bekreft overføring')

    def validate_tsum(self,tsum):
        user_id = current_user.get_id()
        acc = Account.query.filter_by(accuser=user_id,accname=self.tfrom.data).first()
        try:
            float(tsum.data)
        except ValueError:
            raise ValidationError('Ikke en gyldig sum')
        if acc.balance<float(tsum.data):
            raise ValidationError('Du har ikke nokk penger til å overføre denne mengden')
        if float(tsum.data)<0:
            raise ValidationError('Ikke en gyldig sum')
    
    def getchoicesfrom(self):
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        self.tfrom.choices = [(acc.accname,acc.accname) for acc in user.accounts]
    
    def getchoicesto(self):
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        self.tto.choices = [(acc.accname,acc.accname) for acc in user.accounts]

   
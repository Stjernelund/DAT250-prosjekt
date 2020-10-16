from flask import render_template, url_for, redirect, request, flash, session, abort
from app import app, db, bcrypt, limiter
from app.models import User, Account, Log, createaccs
from app.forms import RegistrationForm, LoginForm, Editform, Transferform
from flask_login import login_user, current_user, logout_user, login_required, login_manager
import phonenumbers as pn
import datetime as dt
import io
import pyqrcode
from app.logger import log, log_transaction
from datetime import datetime
from app.mail import send_mail
#pip install PyQRCode

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("6/5minutes")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.userpwd, form.password.data) or \
                not user.verify_totp(form.token.data):
            flash('Feil brukernavn, passord eller token, vennligst prøv på nytt', 'danger')
            log(form.username.data, "Unsuccessful")
            return redirect(url_for('login'))
        if user and bcrypt.check_password_hash(user.userpwd, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            log(form.username.data, "Successful")
            return redirect(next_page) if next_page else redirect(url_for('mainpage'))
        else:
            flash("Feil brukernavn eller passord, vennligst prøv på nytt", 'danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10/day")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        phonenr = pn.parse(form.tlf.data, "NO")
        user = User(username=form.username.data, useremail=form.email.data,
                    userpwd=hashed_password, usertlf= pn.format_number(phonenr, pn.PhoneNumberFormat.NATIONAL), useraddr=form.addr.data)
        db.session.add(user)
        db.session.commit()
        createaccs(user.id)
        db.session.commit()
        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username #!!
        return redirect(url_for('two_factor_setup'))
        #flash(f'Brukeren din har blitt registert, du kan nå logge inn!', 'success')
        #return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('index'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('twofactor.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@app.route("/editprofile", methods=['GET', 'POST'])
@login_required
def editprofile():
    form = Editform()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        if form and len(form.addr.data) ==0 and len(form.email.data) ==0 and len(form.tlf.data) ==0:
            flash("Vennligst sett inn verdiene du vil oppdatere", 'info')
            return render_template("editprofile.html", form=form)
        if len(form.addr.data) != 0:
           user.useraddr=form.addr.data 
        if len(form.tlf.data) != 0: 
            phonenr = pn.parse(form.tlf.data, "NO")
            user.usertlf=pn.format_number(phonenr, pn.PhoneNumberFormat.NATIONAL)
        if len(form.email.data) !=0:
            user.useremail=form.email.data
        db.session.add(user)
        db.session.commit()
        flash(f'Dine personlige opplysninger har blitt oppdatert', 'success')
        return redirect(url_for('account'))
    return render_template("editprofile.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html')

@app.route("/myaccs")
@login_required
def myaccs():
    return render_template('myaccs.html')
    
@app.route("/logs")
@login_required
def logs():
    return render_template('logs.html')

@app.route("/mainpage")
@login_required
def mainpage():
    return render_template('mainpage.html')

@app.route("/kontakt")
def kontakt():
    return render_template('kontakt.html')

@app.route("/om")
def om():
    return render_template('om.html')

@app.route("/transaction", methods=['GET','POST'])
@login_required
def transaction():
    form = Transferform()
    form.getchoices()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        acc = Account.query.filter_by(accuser=user_id, accname=form.tfrom.data).first()
        newsum = acc.balance - float(form.tsum.data)
        acc.balance = newsum
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        loggen = Log(loguser=user_id, logfrom = form.tfrom.data, logto=form.tto.data, logsum=form.tsum.data, logtime=time)
        db.session.add(loggen)
        db.session.commit()
        #send_mail(email, f"Du har overført {penger}kr fra {konto} til {konto2}")
        #log_transaction(user_id, form.tfrom.data, form.tto.data, form.tsum, now)
        return redirect(url_for('myaccs'))
    return render_template('transaction.html', form=form)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = dt.timedelta(minutes=10)
    session.modified = True

#Bruker redirectes etter for mange feil login forsøk
@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Du har brukt for mange usuksessfulle login forsøk, prøv på nytt om 5 minutter", 'danger')
    return redirect(url_for("index"))
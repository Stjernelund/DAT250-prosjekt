#Initialiserer app med de fleste importer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_paranoid import Paranoid


app = Flask(__name__)

# any time the session is detected to come from a different IP address or user agent, the extension will block the request, clear the user session and the Flask-Login remember cookie (if found) and then issue a redirect to the root URL of the site.
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

#Lager secret key og database addresse
app.config['SECRET_KEY'] = '9cd062ffbbcb3a51fdf4e3ac9a75ae674cb7ff89a04627b372072d77b1eb4409'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDB.db'

# Makes sure a cookie will never be sent on an unenctypted wire
SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True
# Browsers hide HTTP-only cookies from JavaScript, but they still send them with outgoing requests.
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True

#activerer imports
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'


limiter = Limiter(app, key_func=get_remote_address)

from app import routes
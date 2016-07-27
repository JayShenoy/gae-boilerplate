from flask import Flask, render_template, request, url_for, redirect, make_response
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
import jinja2

import hashlib
import random
import string
import os

from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

class User(ndb.Model):
	username = ndb.StringProperty()
	password = ndb.StringProperty()
	salt = ndb.StringProperty()

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	def check_password_hash(self, form_password):
		m = hashlib.sha512()
		m.update(self.salt)
		m.update(form_password)
		return self.password == m.hexdigest()

# Login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def create_user(username, password):
	# Generate random salt
	salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(0, 15))

	# Generate password hash
	m = hashlib.sha512()
	m.update(salt)
	m.update(password)
	password_hash = m.hexdigest()

	return User(username=username, password=password_hash, salt=salt)

@login_manager.user_loader
def load_user(userid):
	return User.query().filter(User.username == userid).get()

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	pass

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	pass
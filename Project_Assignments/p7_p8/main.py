from flask import Flask,render_template,redirect,request,url_for,flash ,session
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,PasswordField,validators,BooleanField,Form
from wtforms.validators import InputRequired ,Email,Required,EqualTo,DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_required,logout_user,current_user,login_user
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/register.db'
app.config['SECRET_KEY'] = "Thisissecret"
app.config['UPLOAD_FOLDER'] = "/home/karan_dream/Desktop/upload_folder"



#------------------- Sqlite + Flask SQL Alchemy -------------------#

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class Register(UserMixin,db.Model):
	id = db.Column('register_id',db.Integer,primary_key = True)
	name = db.Column(db.String(100))
	profession = db.Column(db.String(100))
	affiliation = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))

	def __init__(self,name,profession,affiliation,email,password):
		self.name = name
		self.profession = profession
		self.affiliation = affiliation
		self.email = email 
		self.password = password
		
# -- so till now created initial database and tables -- when create all is executed.

@login_manager.user_loader
def load_user(user_id):
	return Register.query.get(int(user_id))





#------------------- Login and Register Class ------------------#

class LoginForm(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	email = StringField('Email',validators=[InputRequired(),Email()])
	password = PasswordField('Password',
			[
				validators.Length(min=2),
				validators.DataRequired(),
			])



class RegisterForm(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	profession = SelectField('Profession',choices=[('Software Engineer','Software Engineer'),('Artist','Artist'),('Player','Player'),('Cook','Cook'),('Musician','Musician')])
	affiliation = StringField('Affiliation')
	email = StringField('Email',validators=[InputRequired(), Email()])
	password = PasswordField('Password',
		[
			validators.Length(min=5),
			validators.DataRequired(),
		])

#--------------------Decorator function --------------#

@app.route('/',methods=['GET','POST'])
def register():
		form = RegisterForm() # instantiate
		if request.method == 'POST':
			name = form.name.data
			profession = form.profession.data
			affiliation = form.affiliation.data
			email = form.email.data
			password = sha256_crypt.encrypt(str(form.password.data)) # --- task 6 1st half
			register_data = Register(name,profession,affiliation,email,password)
			db.session.add(register_data)
			db.session.commit()
			register = register_data.query.all()
			return redirect(url_for('login'))
			#return render_template('data.html',register=register) #-- querying all to display the output.
		return render_template('index.html',form=form) #-- proper form for input using wtf





#-------------------Login-----------------------#


@app.route('/login',methods=['GET','POST'])
def login():
		form = LoginForm()
		if request.method == 'POST':
			email_login = form.email.data
			password_login = form.password.data
			email = Register.query.filter_by(email=email_login).first()
			if email:
				if sha256_crypt.verify(password_login,email.password):
					login_user(email)
					return redirect(url_for('secret'))
			flash('You are not logged in')
			return redirect(url_for('login'))
		return render_template('login.html',form=form)




@app .route('/secret')
@login_required
def secret():
	return render_template('secret.html',name=current_user.email)

@app .route('/error')
def error():
	return render_template('error.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))



#---------------------------Password change------#


class PasswordForm(Form):

    new_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email',validators=[InputRequired(),Email()])



@app.route('/change', methods=['GET', 'POST'])
@login_required
def change_p():
    form = PasswordForm(request.form) 
    if request.method == 'POST' and form.validate():
    	email_login = form.email.data 
    	email = Register.query.filter_by(email=email_login).first()
    	if email:
    		email.password = form.new_password.data 
        	flash('Thanks for changing password')
        return redirect(url_for('login'))
    return render_template('change_p.html', form=form)




#-------------------File & Upload-----------------------------#

@app.route('/upload')
def upload():
		return render_template('upload.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Hey no file selected')
			return redirect(url_for('upload'))
		else:
			file = request.files['file'] # fetches files 
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			num_lines = 0
			with open('/home/karan_dream/Desktop/upload_folder/doc1.txt','r') as f: 
				for line in f:
					num_lines = num_lines + 1
			print(num_lines)
			
			flash('File uploaded to folder')
			return render_template('upload.html',filename=filename,num_lines=num_lines)



#---------------------Password ------------------#



#--------------------App.run------------------------#
if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)



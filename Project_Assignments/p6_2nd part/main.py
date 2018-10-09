'''
Task 6
Extend registration form to include a password field. How will you stop password related information? Create a login page where you can ask user to enter password and email and confirm if credentials are correct.

'''

from flask import Flask,render_template,redirect,request,url_for,flash 
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,PasswordField,validators,BooleanField
from wtforms.validators import InputRequired ,Email,Required,EqualTo,DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from passlib.hash import sha256_crypt
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/register.db'
app.config['SECRET_KEY'] = "Thisissecret"
app.config['UPLOAD_FOLDER'] = "/home/karan_dream/Desktop/upload_folder"



#------------------- Sqlite + Flask SQL Alchemy -------------------#

db = SQLAlchemy(app)


class Register(db.Model):
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




#------------------- Login and Register Class ------------------#

class LoginForm(FlaskForm):
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
			validators.Length(min=2),
			validators.DataRequired(),
		])
# changes to be done.




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
					return redirect(url_for('dashboard'))
			return redirect(url_for('error'))
		return render_template('login.html',form=form)




@app .route('/dashboard')
def dashboard():
	return render_template('dashboard.html')



@app .route('/error')
def error():
	return render_template('error.html')






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



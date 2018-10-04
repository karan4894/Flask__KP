'''
#Task 4
Create a complete new page for URL ‘/upload’. This page should display a form which will allow file to be uploaded by the user. On the Flask end, you must be able to store the file in a specific location. Where exactly the file will be stored is something you should be able to store in a configuration file or parameter. The output given to the user should be “File uploaded successfully.

Task 5
Extend the above task in do the following. Take the file uploaded by the user, count the number of lines present in the file and return an output to the user who uploaded the file saying that “Your file contains so-and-so lines”.
'''





from flask import Flask,render_template,redirect,request,url_for,flash 
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import InputRequired ,Email,Required
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
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

	def __init__(self,name,profession,affiliation,email):
		self.name = name
		self.profession = profession
		self.affiliation = affiliation
		self.email = email 
		
# -- so till now created initial database and tables -- when create all is executed.

#------------------- Flask Class -------------------#

class RegisterForm(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	profession = SelectField('Profession',choices=[('Software Engineer','Software Engineer'),('Artist','Artist'),('Player','Player'),('Cook','Cook'),('Musician','Musician')])
	affiliation = StringField('Affiliation')
	email = StringField('Email',validators=[InputRequired(), Email()])
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
			register_data = Register(name,profession,affiliation,email)
			db.session.add(register_data)
			db.session.commit()
			return render_template('data.html',register = register_data.query.all()) #-- querying all to display the output.
		return render_template('index.html',form=form) #-- proper form for input using wtf

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

			# ------------ here is the logic for counting number of lines in a file.---------
			#--------------problem ----> how to access the save file and count lines...bit confused.
			# ---------- Also tried os.path module and other things.
			'''
			num_lines = 0
			with open('ACCESS_FILE_NAME','r') as f: #--------------how to access i.e how to provide path of file.
				for line in f:
					num_lines = num_lines + 1
			print(num_lines)
			'''
			flash('File uploaded to folder')
			return render_template('upload.html',filename=filename)

#--------------------App.run------------------------#
if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)



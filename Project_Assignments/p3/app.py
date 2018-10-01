'''
#Task 3
Extend the above program to insert the form entries into an SQLite database. Conditions below should be met.
The process of creating SQLite tables should be done without leaving Python (you cannot use SQL commands or some GUI tool to create the database).
There should not be a single SQL command used for inserting the data into a database. You must achieve this using ORM.
Hints: Use Flask-SQLAlchemy to achieve this. There is a create_all() command that can help you overcome the first challenge. A certain chapter of Miguel’s book is lovely for understanding this.
'''

from flask import Flask,render_template,redirect,request,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import InputRequired ,Email,Required
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/register.db'
app.config['SECRET_KEY'] = "Thisissecret"


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


#--------------------App.run------------------------#
if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)



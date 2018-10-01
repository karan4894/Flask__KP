'''
Task 2
Convert above form from plain HTML to Flask-WTForms form and add server side validation. Following validations should be added.
Name cannot be empty
Profession must become a dropdown with single option selectable.
Affiliation is optional.
E-mail must be a valid e-mail.
Output should remain the same.

'''


from flask import Flask,render_template,redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import InputRequired ,Email,Required
app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisissecret"


#------------------- Flask Class -------------------#


class RegisterForm(FlaskForm):
	mychoices = ['karan','rahul']
	name = StringField('Name', validators=[InputRequired()])
	profession = SelectField('Profession',choices=[('1','Software Developer'),('2','Artist'),('3','Player'),('4','Cook'),('5','Musician')])
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
			# goal 1
			print("Following are the things being printed")
			print(name)
			print(profession)
			print(affiliation)
			print(email)
			# goal 2
			return render_template('data.html',name=name,profession=profession,affiliation=affiliation,email=email)
		return render_template('index.html',form=form)

#--------------------App.run------------------------#
if __name__ == '__main__':
	app.run(debug=True)


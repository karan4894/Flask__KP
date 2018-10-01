'''
Task 1
Create a web page from scratch in HTML containing a form. Let this form have the following fields.
Name
Profession
Affiliation
E-mail
A ‘Submit’ button.
Now, serve this page from Flask using the URL: 127.0.0.1:5000/register. At the backend, retrieve the entries entered by the user in this form. As a first step, print out the form entries in the console. As a second step, throw a new page to the user (as a response to their clicking the Submit button), a page where these four fields are displayed as a list:
Name: <whatever user entered>
Profession: <whatever user entered>
Note: The form should be plain HTML. The form should be sent via POST. 


'''


from flask import Flask,render_template,redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)


@app.route('/register',methods=['GET','POST'])
def register():
		if request.method == 'POST':
			Name = request.form['name']                 #-- Taking data from Normal Form
			Affiliation = request.form['affiliation']
			Profession = request.form['profession']
			Email = request.form['email']
			print(Name)									#-- Printing data on console
			print(Affiliation)
			print(Profession)
			print(Email)
			return render_template('data.html',name=Name,affiliation=Affiliation,profession=Profession,email=Email) #-- printing on data.html final view
		return render_template('Index.html')

if __name__ == '__main__':
	app.run(debug=True)


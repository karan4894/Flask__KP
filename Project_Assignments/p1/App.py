from flask import Flask,render_template,redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)


@app.route('/register',methods=['GET','POST'])
def register():
		if request.method == 'POST':
			Name = request.form['name']
			Affiliation = request.form['affiliation']
			Profession = request.form['profession']
			Email = request.form['email']
			print(Name)
			print(Affiliation)
			print(Profession)
			print(Email)
			return render_template('data.html',name=Name,affiliation=Affiliation,profession=Profession,email=Email)
		return render_template('Index.html')

if __name__ == '__main__':
	app.run(debug=True)


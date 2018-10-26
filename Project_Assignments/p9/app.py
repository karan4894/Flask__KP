from flask import Flask,render_template,request,flash,redirect,url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite' #students database
app.config['SECRET_KEY'] = 'random_key'
db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id',db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    affiliation = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    goals = db.Column(db.String(100))

    def __init__(self,username,email,affiliation,hobby,goals):
        self.username = username
        self.email = email
        self.affiliation = affiliation
        self.hobby = hobby
        self.goals = goals



class UserForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    affiliation = StringField('Affiliation', [validators.Length(min=6, max=35)])
    hobby = StringField('Hobby', [validators.Length(min=6, max=35)])
    goals = StringField('Goals', [validators.Length(min=6, max=35)])


@app.route('/')
def show_all():
    return render_template('show_all.html',students=students.query.all())



@app.route('/new', methods=['GET', 'POST'])
def new():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        affiliation = form.affiliation.data
        hobby = form.hobby.data
        goals = form.goals.data
        student = students(username,email,affiliation,hobby,goals) # using this you are adding all in database i.e students database
        db.session.add(student)
        db.session.commit()
        flash('Records are successfully added')
        return redirect(url_for('show_all'))
    return render_template('new.html', form=form)


if __name__ == '__main__':
   db.create_all() # create table and database of student
   app.run(debug = True)
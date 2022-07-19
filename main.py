from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, AnswerForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from trivia import TriviaQuestion

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '288c97cf1b11a5726d571d84ccc1f5f5'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #Trivia
    t = TriviaQuestion()
    t.get_data()
    string = t.list_of_answers

    #Set Question
    return render_template('home.html', question=t.question, a1=t.list_of_answers[0], a2=t.list_of_answers[1], a3=t.list_of_answers[2], a4=t.list_of_answers[3], correct_answer=t.correct_answer)

@app.route("/correct")
def correct():
    return render_template('result.html', result="CORRECT", color="green")

@app.route("/incorrect")
def incorrect():
    return render_template('result.html', result="INCORRECT", color="red")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mitsuruki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False) 
    date = db.Column(db.DateTime, default=datetime.utcnow) 
    
    def __repr__(self):
        return 'Article %r' % self.id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Login = db.Column(db.String(100), nullable=False) 
    Pasword = db.Column(db.String(300), nullable=False)
    Name = db.Column(db.String(300), default="Anonim")
    Surname = db.Column(db.String(300), default=str(random.randint(100000,999999)))
    Status = db.Column(db.String(100), default="User")
    date = db.Column(db.DateTime, default=datetime.utcnow) 
    
    def __repr__(self):
        return 'User %r' % self.id    

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        file = open('log.txt','a')
        login = request.form["login"]
        file.write(f'Login="{login}"\n')
        file.close()
        password = request.form["password"]
        file = open('log.txt','a')
        file.write(f'Password="{password}"\n')
        file.close()
        user = Users(Login=login, Pasword=password)      
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(f'/user-{user.id}')
        except:
            return "При додаванні юзера сталася якась бебра"           
    else:
        return render_template("sign_in.html")
      
@app.route('/user-<int:id>', methods=["POST", "GET"])    
def user(id):
    user = Users.query.get(id)
    answer = f'Ласкаво просимо {user.Name}#{user.Surname} у твій кабінет'
    return answer

    
if __name__ == "__main__":
    app.run(debug=True)

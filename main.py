from flask import Flask, render_template,request,flash,redirect,url_for
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


# step 1
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdata.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    gender = db.Column(db.String(20))
    contact = db.Column(db.String(15))

@app.route("/",methods=['POST','GET'])
def main():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or user.password!= password:
            flash("Error! Incorrect details.")
            return redirect(url_for('login'))
        else:
            return render_template("profile.html")
    return render_template('login.html')
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/signup")
# def signup():
#     return render_template("signup.html")

# step 3
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        contact = request.form.get('contact')
        gender = request.form.get('gender')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
        else:
            new_user = User(email=email, name=name, username=username, password=password,
                            gender=gender, contact=contact)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
    return render_template('signup.html')

if __name__ == "__main__":
    # step 4
    with app.app_context():
        db.create_all()
    app.run(debug=True)

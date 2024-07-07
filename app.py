from flask import Flask,render_template,request,flash,redirect,session,url_for,make_response
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key="12345"

client = PyMongo(app,uri=("mongodb://localhost:27017/aaliyar_dam"))
db = client.db

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        n = request.form.get('uname')
        e = request.form.get('email')
        p = request.form.get('phone')
        pwd = request.form.get('password')
        cpwd = request.form.get('cpassword')

        db.user_info.insert_many([{
            'name':n,
            'email':e,
            "phone":p,
            "password":pwd,
            "confirm Password":cpwd
        }])

        # flash('Register successfull','success')
        return redirect("/")
    return render_template("register.html")


class User:
    def login(self,email,password):
        self.email = email
        self.password = password
        user = db.user_info.find_one({'email': self.email})

        if user is None:
            flash("Invalid User!","warning")
            return redirect("/login")
        elif self.email != user['email']:
             flash("Email doesn't match","danger")
             return redirect("/login")
        elif self.password != user['password']:
             flash("Password doesn't match","danger")
             return redirect("/login")
        elif self.email == user['email'] and self.password == user['password']:
             session['logged_in'] = True
             session['name'] = user['name']
             session['email'] = user['email']
             session['phone'] = user['phone']

             res = make_response(render_template("homeLogin.html"))
             res.set_cookie('email',self.email)
             return res

@app.route('/login',methods = ["GET","POST"])
def user_login():
     if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        return User().login(email,password)
     return render_template("login.html")

@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('home')))
    res.set_cookie('email', '',expires=0)
    session.clear()
    return res

@app.route('/userdetails')
def userDetails():
    user = db.user_info.find({'name' : session['name']})
    return render_template("userdetails.html",user=user)

if __name__ == '__main__':
    app.run(debug=True)
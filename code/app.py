from flask import Flask,render_template,redirect,url_for,request,abort
from flask_sqlalchemy import SQLAlchemy

from model import db,User,Admin,Professional,Service,Service_requests

app=Flask(__name__)

#database path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project_MAD 1.sqlite3"


db.init_app(app)

app.app_context().push()

#main home page
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":
        users=User.query.all()
        for i in users:
            if request.form["username"]==i.username and request.form["password"]==i.password:
                return render_template("admin_dashboard.html")
            abort(404)
    return render_template("index.html")
@app.route('/register_cus',methods=['GET','POST'])
def register_cus():
    if request.method == "POST":
        return render_template("index.html")
    return render_template("register.html")

@app.route('/register_pro',methods=['GET','POST'])
def register_pro():
    if request.method == "POST":
        return render_template("register_professionals.html")
    return render_template("register_professionals.html")
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
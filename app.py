from flask import Flask,render_template,redirect,url_for,request,abort

from datetime import datetime

from sqlalchemy import or_

from model import db,User,Admin,Professional,Service,Service_requests

app=Flask(__name__)


#database path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project_MAD 1.sqlite3"


db.init_app(app)

with app.app_context():
    db.create_all()

#main home page
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":
        admins=Admin.query.all()
        for i in admins:
            if request.form["email"]==i.user_name and request.form["password"]==i.password:
                return redirect(url_for('admin_dash'))
        customer=User.query.all()
        for i in customer:
            if request.form["email"]==i.user_name and request.form["password"]==i.password and i.status!='blocked':
                return redirect(url_for('customer_dash',user_id=i.user_id))
        professional=Professional.query.all()
        for i in professional:
            if request.form["email"]==i.pr_user_name and request.form["password"]==i.pr_password and i.pr_status=="approved":
                return redirect(url_for('professional_dash', pr_id=i.pr_id))
                
        return render_template("index.html")
    return render_template("index.html")

#dash_board for all roles
@app.route('/admin_dashboard')
def admin_dash():
    service=Service.query.all()
    service_requests=Service_requests.query.all()
    prof=Professional.query.filter(Professional.pr_status!="blocked").all()
    users=User.query.filter(User.status!="blocked").all()
    return render_template("admin_dashboard.html",service=service, service_requests=service_requests,professionals=prof,user=users)


@app.route('/professional_dashboard/<pr_id>')
def professional_dash(pr_id):
    today = datetime.now().date()  
    professional=Professional.query.get(pr_id)
    today_services=Service_requests.query.filter(Service_requests.professional_id == pr_id,Service_requests.date_of_request == today).all()
    accepted_services=Service_requests.query.filter(Service_requests.professional_id == pr_id,Service_requests.service_status=='accepted').all()
    closed_services=Service_requests.query.filter(Service_requests.professional_id == pr_id,Service_requests.service_status=='closed').all()
    return render_template("professional_dashboard.html",today_service=today_services,closed_service=closed_services,professional=professional,accepted_service=accepted_services)


@app.route('/customer/dashboard/<user_id>')
def customer_dash(user_id):
    service=Service.query.all()
    service_request=Service_requests.query.filter(Service_requests.customer_id==user_id).all()
    service_requests=sorted(service_request, key=lambda x: x.service_status)
    return render_template("customer_dashboard.html",service=service,service_requests=service_requests,user_id=user_id)


@app.route('/register_cus',methods=['GET','POST'])
def register_cus():
    if request.method == "POST":
        customer=User.query.all()
        for i in customer:
            if i.user_name==request.form["email"]:
                return render_template("register.html")
        user=User(user_name=request.form["email"],password=request.form["password"],fullname=request.form["fullname"],contact_no=request.form["phone"],address=request.form["address"],pincode=request.form["pincode"],status='available')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
       
    return render_template("register.html")


@app.route('/register_professional',methods=['GET','POST'])
def register_pro():
    if request.method == "POST":
        professionals=Professional.query.all()
        for i in professionals:
            if i.pr_user_name==request.form["username"]:
                return render_template("register_professionals.html")
        prof=Professional(pr_user_name=request.form["username"],pr_password=request.form["password"],pr_fullname=request.form["fullname"],pr_service_name=request.form.get("service"),pr_experience=request.form["experience"],pr_contact_no=request.form["phone"],pr_address=request.form["address"],pr_pincode=request.form["pincode"],pr_status="null")
        db.session.add(prof)
        db.session.commit()
        return redirect(url_for('home'))
    services=Service.query.all()
    return render_template("register_professionals.html",services=services)
    


@app.route('/service/create',methods=['GET','POST'])
def add_service():
    if request.method=="GET":
        return render_template("add_service.html")
    elif request.method=="POST":
        service=Service.query.all()
        for i in service:
            if i.service_name==request.form["s_name"]:
                return render_template("add_service.html")
        service=Service(service_name=request.form["s_name"],service_price=request.form["b_price"],service_time_required=request.form["s_time"],service_description=request.form["s_desc"])
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    

@app.route('/service/<service_id>/edit',methods=['GET','POST'])
def edit_service(service_id):
    if request.method == "GET":
        service = Service.query.get(service_id)
        return render_template('edit_service.html',service=service)

    elif request.method == "POST":
        service = Service.query.filter_by(service_id=service_id).first()
        desc = request.form['s_desc']
        time = request.form['s_time']
        baseprice = request.form['b_price']
        Service.query.filter(Service.service_id==service_id).update({'service_description':desc, 'service_time_required':time,'service_price':baseprice})
        db.session.commit()
        return redirect(url_for('admin_dash'))
    
@app.route('/service/<service_id>/delete',methods=["GET"])
def delete_service(service_id):
	if request.method == "GET":
		Service.query.filter_by(service_id=service_id).delete()
		db.session.commit()
		return redirect(url_for('admin_dash'))
	
@app.route('/professional/<pr_id>/approve',methods=["GET"])
def prof_approve(pr_id):
    if request.method=="GET":
        Professional.query.filter(Professional.pr_id==pr_id).update({'pr_status':'approved'})
        db.session.commit()
        return redirect(url_for('admin_dash'))
    

@app.route('/<pr_id>/professional_profile', methods=['GET', 'POST'])
def professional_profile(pr_id):
    professional=Professional.query.get(pr_id)
    if request.method == 'POST':
        if request.form['password']:
            professional.pr_password = request.form['password']
        professional.pr_address = request.form['address']
        db.session.commit()
        return redirect(url_for('professional_dash', pr_id=pr_id))
    return render_template("professional_profile.html",professional=professional)
    
@app.route('/professional/<pr_id>/reject',methods=["GET"])
def prof_reject(pr_id):
    if request.method=="GET":
        Professional.query.filter(Professional.pr_id==pr_id).update({'pr_status':'rejected'})
        db.session.commit()
        return redirect(url_for('admin_dash'))


@app.route('/professional/<pr_id>/block',methods=["GET"])
def prof_block(pr_id):
    if request.method=="GET":
        Professional.query.filter(Professional.pr_id==pr_id).update({'pr_status':'blocked'})
        db.session.commit()
        return redirect(url_for('admin_dash'))
    
@app.route('/user/<user_id>/block')
def customer_block(user_id):
    if request.method=="GET":
        User.query.filter(User.user_id==user_id).update({'status':'blocked'})
        db.session.commit()
        return redirect(url_for('admin_dash'))
    

@app.route('/professional/service/<user_id>/<pr_id>/accept',methods=["GET"])
def servicerequests_accept(user_id,pr_id):
    if request.method=="GET":
        Service_requests.query.filter(Service_requests.professional_id==pr_id,Service_requests.customer_id==user_id).update({'service_status':'accepted'})
        db.session.commit()
        return redirect(url_for('professional_dash', pr_id=pr_id))

@app.route('/professional/service/<user_id>/<pr_id>/reject',methods=["GET"])
def servicerequests_reject(user_id,pr_id):
    if request.method=="GET":
        Service_requests.query.filter(Service_requests.professional_id==pr_id,Service_requests.customer_id==user_id).delete()
        db.session.commit()
        return redirect(url_for('professional_dash', pr_id=pr_id))
    
@app.route('/<user_id>/customer_profile', methods=['GET', 'POST'])
def customer_profile(user_id):
    customer=User.query.get(user_id)
    if request.method == 'POST':
        if request.form['password']:
            User.password = request.form['password']
        User.address = request.form['address']
        db.session.commit()
        return redirect(url_for('customer_dash', user_id=user_id))
    return render_template("customer_profile.html",customer=customer)

@app.route('/service/<service_id>/<user_id>')
def service_prof(service_id,user_id):
    service=Service.query.get(service_id)
    best_services=Professional.query.filter(Professional.pr_service_name==service.service_name,Professional.pr_status=='approved').all()
    service_requests=Service_requests.query.filter(Service_requests.customer_id==user_id).all()
    return render_template("customer_professional.html",service=service,best_services=best_services,service_requests=service_requests,user_id=user_id)


@app.route('/best_services/book/<pr_id>/<service_id>/<user_id>')
def book_services(pr_id,service_id,user_id):
    service_request = Service_requests(professional_id=pr_id,customer_id=user_id,service_id=service_id,date_of_request=datetime.now().date(),service_status='requested')
    db.session.add(service_request)
    db.session.commit()
    return redirect(url_for('customer_dash',user_id=user_id))

@app.route('/service_requests/<user_id>/<pr_id>/close',methods=["GET"])
def customer_close(user_id,pr_id):
    if request.method=="GET":
        Service_requests.query.filter(Service_requests.professional_id==pr_id,Service_requests.customer_id==user_id).update({'service_status':'closed','date_of_completion':datetime.now().date()})
        db.session.commit()
        return redirect(url_for('customer_dash',user_id=user_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
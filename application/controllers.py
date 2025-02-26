from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from .models import *
from sqlalchemy import or_
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory

def formatting(text):
    text = (text.replace(" ", "").replace(",","")).lower()
    return text


@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')




############################################################



@app.route("/login_admin", methods=['GET', 'POST'])
def loginadmin():
    if request.method=='POST':
        emailid=request.form.get('emailid')
        pswd=request.form.get('pswd')
        if emailid=='admin@gohappy.com':
            if pswd=='admin123':
                return redirect('/dashb_admin')
            else:
                return "Invalid Password"
        else:
            return "Invalid email"
    return render_template('login_admin.html')

@app.route("/login_customer", methods=['GET', 'POST'])
def logincust():
    if request.method=='POST':
        emailid=request.form.get('emailid')
        pswd=request.form.get('pswd')
        customer=Customers.query.filter_by(emailid=emailid).first()
        if customer:
            userid = customer.userid
            if customer.pswd==pswd:
                return redirect(f'/dashb_customer/{userid}')
            else:
                return "Invalid Password"
        else:
            return "Invalid email"
    return render_template('login_customer.html')

@app.route("/login_professional", methods=['GET', 'POST'])
def loginprofes():
    if request.method=='POST':
        emailid=request.form.get('emailid')
        pswd=request.form.get('pswd')
        professional=Professionals.query.filter_by(emailid=emailid).first()
        if professional:
            userid = professional.userid
            if professional.pswd==pswd:
                if professional.active == "True":
                    return redirect(f'/dashb_professional/{userid}')
                elif professional.active == "None":
                    return "Wait till your documents are verified"
                else:
                    return "You are blocked or rejected"
            else:
                return "Invalid Password"
        else:
            return "Invalid email"
    return render_template('login_professional.html')





################################################################################




@app.route("/signup_customer", methods=['GET', 'POST'])
def signupcust():
    if request.method=='POST':
        fullname=request.form.get('fullname')
        contactno=request.form.get('contactno')
        emailid=request.form.get('emailid')
        pswd=request.form.get('pswd')
        address=request.form.get('address')
        searchaddress= formatting(address)
        pincode=request.form.get('pincode')
        customer=Customers.query.filter_by(emailid=emailid).first()
        if customer:
            return "User already exists, please login"
        else:
            new_cust=Customers(fullname=fullname, contactno=contactno, emailid=emailid, pswd=pswd, address=address, searchaddress=searchaddress, pincode=pincode)
            db.session.add(new_cust)
            db.session.commit()
            return redirect("/login_customer")
    return render_template('signup_customer.html')

@app.route("/signup_professional", methods=['GET', 'POST'])
def signupprofes():
    services=Services.query.all()
    if request.method=='POST':
       fullname=request.form.get('fullname')
       contactno=request.form.get('contactno')
       emailid=request.form.get('emailid')
       pswd=request.form.get('pswd')
       service=request.form.get('service')
       exp=request.form.get('exp')        
       address=request.form.get('address')
       searchaddress= formatting(address)
       pincode=request.form.get('pincode')
       uploaded_file=request.files.get('upload_file')
       professional=Professionals.query.filter_by(emailid=emailid).first()
       if professional:
           return "User already exists, please login"
       else:
           new_profes=Professionals(fullname=fullname, contactno=contactno, emailid=emailid, pswd=pswd, service=service, experience=exp, address=address, searchaddress=searchaddress, pincode=pincode, active="None", rating_sum = 0, ratings_count = 0)
           db.session.add(new_profes)
           db.session.commit()
           if uploaded_file and uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path)
                new_profes.docs=filename
                db.session.commit()
           return redirect("/login_professional")
    return render_template('signup_professional.html', services=services)




####################################################################################3




@app.route("/dashb_admin", methods=['GET', 'POST'])
def dashba():
    services=Services.query.all()
    professionals = Professionals.query.all()
    servicereqs = db.session.query(Servicerequest, Customers.fullname.label('customer_name'), Professionals.fullname.label('professional_name')).join(Customers, Servicerequest.custid == Customers.userid).join(Professionals, Servicerequest.profesid == Professionals.userid).all()
    if request.method=='POST':
        name=request.form.get('name')
        descr=request.form.get('descr')
        searchdescr = formatting(descr)
        baseprice=request.form.get('baseprice')
        service=Services.query.filter_by(name=name).first()
        if service:
            return "Service already exists"
        else:
            new_service=Services(name=name,descr=descr, searchdescr=searchdescr, baseprice=baseprice)
            db.session.add(new_service)
            db.session.commit()
            return redirect("/dashb_admin")
    return render_template('dashb_admin.html', services=services, professionals=professionals, servicereqs=servicereqs)


@app.route('/deleteservice/<id>', methods=['GET', 'POST'])
def delete(id):
    service=Services.query.get(id)
    db.session.delete(service)
    db.session.commit()
    return redirect('/dashb_admin')


@app.route('/editservice/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method=='POST':
        service=Services.query.get(id)
        service.name=request.form.get("name")
        service.descr=request.form.get("descr")
        service.baseprice=request.form.get("baseprice")
        db.session.commit()
    return redirect('/dashb_admin')
    

@app.route("/search_admin", methods=['GET', 'POST'])
def searcha():
    if request.method=='POST':
        searchby=request.form.get('search_by')
        searchfor=request.form.get('search_for')
        searchfor='%'+searchfor+'%'
        if searchby=='2':
            results=Servicerequest.query.join(Professionals).join(Customers).filter(Customers.fullname.like(searchfor)).all()
        elif searchby=='3':
            results=Servicerequest.query.join(Professionals).join(Customers).filter(Professionals.fullname.like(searchfor)).all()
        else:
            results=Servicerequest.query.join(Professionals).join(Customers).filter(Servicerequest.status.like(searchfor)).all()
       
        if results:
            return render_template('search_admin.html', results= results, noresults = False)
        else:
            return render_template('search_admin.html', noresults = True)
    return render_template('search_admin.html')



@app.route("/summary_admin", methods=['GET', 'POST'])
def summarya():
    services=Servicerequest.query.all()
    servicereqsum=[]
    for i in services:
        servicereqsum.append(i.status)
    plt.clf()
    plt.figure(figsize=(5,4))
    plt.hist(servicereqsum)
    plt.title("Service Request by Status", fontsize=14, color='blue')
    plt.savefig(f'static/statusbycount.png')

    ratingsgraph=[]
    for i in services:
        if i.status=='Completed':
            ratingsgraph.append(i.ratings)
    print(ratingsgraph)
    print(type(ratingsgraph))
    ratingsdic={}
    for i in ratingsgraph:
        if i in ratingsdic:
            ratingsdic[i]+=1
        else:
            ratingsdic[i]=1
    labelsofpie=list(ratingsdic.keys())
    sizes=[]
    for i in ratingsdic.values():
        size=i/len(ratingsgraph)
        size=size*100
        sizes.append(size)
    plt.clf()
    plt.figure(figsize=(5,4))
    plt.pie(sizes, labels=labelsofpie, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Ratings Distribution", fontsize=14, color='blue')
    plt.savefig(f'static/ratingspie.png')

    return render_template('summary_admin.html')


@app.route('/approve/<id>')
def approve(id):
    professional = Professionals.query.get(id)
    professional.active = "True"
    db.session.commit()
    return redirect(request.referrer)

@app.route('/block/<id>')
def block(id):
    professional = Professionals.query.get(id)
    professional.active = "False"
    db.session.commit()
    return redirect(request.referrer)





######################################################################################



@app.route('/dashb_customer/<int:userid>', methods=['GET', 'POST'])
def dashbc(userid):
    services=Services.query.all()
    pendingreqs=db.session.query(Servicerequest.bookingid, Professionals.service, Professionals.fullname, Professionals.contactno, Servicerequest.datecreated, Servicerequest.status).join(Servicerequest).filter(Servicerequest.custid==userid, Servicerequest.status.in_(['Pending', 'Accepted']))
    servicehist=db.session.query(Servicerequest.bookingid, Professionals.service, Professionals.fullname, Professionals.contactno, Servicerequest.datecompleted, Servicerequest.ratings, Servicerequest.status).join(Servicerequest).filter(Servicerequest.custid==userid, Servicerequest.status.in_(['Completed', 'Rejected']))
    userdetails=Customers.query.get(userid)
    return render_template('dashb_customer.html', id=userid, services=services, pendingreqs=pendingreqs, servicehist=servicehist, userdetails=userdetails)
    

@app.route('/dashb_customer/completed/<bookingid>', methods=['GET', 'POST'])
def completed(bookingid):
    if request.method=='POST':
        print('sexy suhani')
        print(bookingid)
        sreq=Servicerequest.query.get(bookingid)
        sreq.ratings=request.form.get('rating')
        sreq.remarks=request.form.get('remarks')
        sreq.datecompleted=request.form.get('date')
        sreq.status='Completed'
        proid=sreq.profesid
        pro=Professionals.query.get(proid)
        pro.rating_sum=pro.rating_sum+int(sreq.ratings)
        pro.ratings_count=pro.ratings_count+1
        pro.avg_rating=pro.rating_sum/pro.ratings_count
        db.session.commit()
    return redirect(request.referrer)

@app.route('/dashb_customer/<int:userid>/<servicename>', methods=['GET', 'POST'])
def dashbcservice(userid, servicename):
    listofprofessionals=Professionals.query.filter_by(service=servicename)
    return render_template('services.html', list=listofprofessionals, id=userid, service=servicename)

@app.route('/book/<id>', methods=['GET', 'POST'])
def book(id):
    if request.method=='POST':
        datecreated=request.form.get("date")
        profesid=request.form.get("profesid")
        new_servicereq=Servicerequest(custid=id, profesid=profesid, datecreated=datecreated, status="Pending")
        db.session.add(new_servicereq)
        db.session.commit()
        return redirect(f'/dashb_customer/{id}')
    


@app.route('/search_customer/<int:userid>', methods=['GET', 'POST'])
def searchc(userid):
    if request.method=='POST':
        searchby=request.form.get('search_by')
        searchfor=request.form.get('search_for')
        searchfor='%'+searchfor+'%'
        if searchby=='1':
            services = db.session.query(Services).filter(Services.searchdescr.like(searchfor)).first()
            service = services.name
            if not services:
                return render_template('search_cust.html', noresults = True, id=userid)
            results = db.session.query(Professionals, Services).join(Services, Professionals.service == Services.name).filter(Professionals.service==service).all()
        if searchby=='2':
            results = db.session.query(Professionals, Services).join(Services, Professionals.service == Services.name).filter(Professionals.searchaddress.like(searchfor)).all()
        if searchby=='3':
            results = db.session.query(Professionals, Services).join(Services, Professionals.service == Services.name).filter(Professionals.pincode.like(searchfor)).all()
        if searchby=='4':
            results = db.session.query(Professionals, Services).join(Services, Professionals.service == Services.name).filter(Professionals.fullname.like(searchfor)).all()
        
        if results:
            return render_template('search_cust.html', results= results, noresults = False, id=userid)
        else:
            return render_template('search_cust.html', noresults = True, id=userid)
    return render_template('search_cust.html', id = userid)


@app.route('/summary_customer/<int:userid>', methods=['GET', 'POST'])
def summaryc(userid):
    services=Servicerequest.query.filter_by(custid=userid)
    servicebystatus=[]
    for i in services:
        servicebystatus.append(i.status)
    plt.clf()
    plt.figure(figsize=(5,4))
    plt.hist(servicebystatus)
    plt.savefig(f'static/statusbycount{userid}.png')
    return render_template('summary_cust.html', id=userid)



@app.route('/profilecust/<userid>', methods=['GET','POST'])
def profilecust(userid):
    if request.method=='POST':
        user = Customers.query.get(userid)
        user.fullname = request.form.get('fullname')
        user.emailid = request.form.get('emailid')
        user.pswd = request.form.get('pswd')
        user.address = request.form.get('address')
        user.searchaddress=formatting(user.address)
        user.pincode = request.form.get('pincode')
        user.contactno = request.form.get('contactno')
        db.session.commit()
        return redirect(request.referrer)


##########################################################################################3



@app.route('/dashb_professional/<int:userid>', methods=['GET', 'POST'])
def dashbp(userid):
    servicerequests=db.session.query(Customers.fullname, Customers.contactno, Customers.pincode, Servicerequest.datecreated, Servicerequest.bookingid).join(Servicerequest, Servicerequest.custid==Customers.userid).filter(Servicerequest.profesid==userid, Servicerequest.status=="Pending")
    servicehist=db.session.query(Servicerequest.bookingid, Customers.fullname, Customers.contactno, Servicerequest.datecompleted, Servicerequest.ratings, Servicerequest.remarks).join(Servicerequest, Servicerequest.custid==Customers.userid).filter(Servicerequest.profesid==userid, Servicerequest.status=="Completed")
    userdetails=Professionals.query.get(userid)
    return render_template('dashb_professional.html', id=userid, servicerequests=servicerequests, servicehist=servicehist, userdetails=userdetails)
    
@app.route('/accept_profes/<bookingid>', methods=['GET', 'POST'])
def accept(bookingid):
    serreq=Servicerequest.query.get(bookingid)
    if serreq.status=='Pending':
        serreq.status='Accepted'
        db.session.commit()
    return redirect(request.referrer)

@app.route('/reject_profes/<bookingid>', methods=['GET', 'POST'])
def reject(bookingid):
    serreq=Servicerequest.query.get(bookingid)
    if serreq.status=='Pending':
        serreq.status='Rejected'
        db.session.commit()
    return redirect(request.referrer)

@app.route('/search_professional/<int:userid>', methods=['GET', 'POST'])
def searchp(userid):
    if request.method=='POST':
        searchby=request.form.get('search_by')
        searchfor=request.form.get('search_for')
        searchfor='%'+searchfor+'%'
        results=Servicerequest.query.filter_by(profesid = userid)
        if searchby =='3':
            results=results.join(Customers).filter(Servicerequest.status.like(searchfor))
            #return render_template('search_profes.html', id=userid, results=results)
        else:
            results=results.join(Customers).filter(or_(Servicerequest.datecompleted.like(searchfor),Servicerequest.datecreated.like(searchfor))).all()
            #return render_template('search_profes.html', id=userid, results=results)
        if results:
            return render_template('search_profes.html', id=userid, results=results)
        else:
            return render_template('search_profes.html', id=userid, noresults=True)
    return render_template('search_profes.html', id=userid)


@app.route('/summary_professional/<int:userid>', methods=['GET', 'POST'])
def summaryp(userid):
    services=Servicerequest.query.filter_by(profesid=userid)
    servicebystatus=[]
    for i in services:
        servicebystatus.append(i.status)
    plt.clf()
    plt.figure(figsize=(5,4))
    plt.hist(servicebystatus)
    plt.title("Your Service Request by Status", fontsize=14, color='blue')
    plt.savefig(f'static/statusbycount{userid}.png')
    ratingsgraph=[]
    for i in services:
        if i.status=='Completed':
            ratingsgraph.append(i.ratings)
    print(ratingsgraph)
    print(type(ratingsgraph))
    ratingsdic={}
    for i in ratingsgraph:
        if i in ratingsdic:
            ratingsdic[i]+=1
        else:
            ratingsdic[i]=1
    labelsofpie=list(ratingsdic.keys())
    sizes=[]
    for i in ratingsdic.values():
        size=i/len(ratingsgraph)
        size=size*100
        sizes.append(size)
    plt.clf()
    plt.figure(figsize=(5,4))
    plt.pie(sizes, labels=labelsofpie, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Your Ratings Distribution", fontsize=14, color='blue')
    plt.savefig(f'static/ratingspie{userid}.png')
    return render_template('summary_profes.html', id=userid)



@app.route('/profileprofes/<userid>', methods=['GET','POST'])
def profileprofes(userid):
    if request.method=='POST':
        user = Professionals.query.get(userid)
        user.fullname = request.form.get('fullname')
        user.emailid = request.form.get('emailid')
        user.pswd = request.form.get('pswd')
        user.address = request.form.get('address')
        user.searchaddress=formatting(user.address)
        user.pincode = request.form.get('pincode')
        user.contactno = request.form.get('contactno')
        user.experience = request.form.get('experience')
        db.session.commit()
        return redirect(request.referrer)


@app.route('/view_file/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)



from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import ibm_db
import re
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key ='a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=Certificate.crt;UID=jqy91109;PWD=jKfOzK88qIqZnQQK",'','')
print(conn)
@app.route('/register',methods=['GET', 'POST'])
def register():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        email_id = request.form['email_id']
        phone_no = request.form['phone_no']
        password = request.form['password']
        blood_group = request.form['blood_group']
        age = request.form['age']
        query = "SELECT * FROM USER1 WHERE username=?"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account =ibm_db.fetch_assoc(stmt)
        if (account):
            msg = "Account already exists!"
            return render_template('login.html', msg=msg)
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
        #     msg = "Invalid email addres"
        # elif not re.match(r'[A-Za-z0-9+', username):
        #     msg = "Name must contain only characters and numbers"
        else:
            insert_sql= "INSERT INTO USER1 values(?,?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, email_id)
            ibm_db.bind_param(stmt, 3, phone_no)
            ibm_db.bind_param(stmt, 4, password)
            ibm_db.bind_param(stmt, 5, blood_group)
            ibm_db.bind_param(stmt, 6, age)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            msg = 'You have successfully Logged In!!'
            return render_template('login.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register.html', msg=msg)

@app.route('/login',methods=['GET', 'POST'])
def login():
    global usermail,userpass,userid
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usermail = username
        userpass = password 
        query = "SELECT * FROM USER1 WHERE username=? and password=?"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account =ibm_db.fetch_assoc(stmt)
        if (account):
            session['loggedin'] = True
            session['id']= account['USERNAME']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            msg = "Login Successfully ! "
            return render_template('welcome.html', msg=msg)
        else:
            return render_template('login.html')
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('login.html', msg=msg)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template("welcome.html")
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    #sendemail('.com','s')
    return render_template('reset.html')
    
@app.route('/req', methods = ['GET', 'POST'])
def req():
  msg=' '
  if request.method == 'POST':  
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    phone = request.form['phone']
    blood = request.form['blood']
    locality = request.form['locality']
    postalcode =request.form['postalcode'] 
    address = request.form['address']
    print('age')
    insert_sql = "INSERT INTO REQ1 VALUES('name','age','email','phone','blood','locality','postalcode','address')"

    stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, age)
    ibm_db.bind_param(stmt, 3, email)
    ibm_db.bind_param(stmt, 4, phone)
    ibm_db.bind_param(stmt, 5, blood)
    ibm_db.bind_param(stmt, 6, locality)
    ibm_db.bind_param(stmt, 7, postalcode)
    ibm_db.bind_param(stmt, 8, address)
    print('age')
    ibm_db.execute(stmt)
    #sendmail('Plasma donor App plasma request', email ,'Your request for plasma is received.')
    msg='success'
    return render_template('success.html', msg=msg)
  else:
    return render_template('req.html', msg=msg)
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")
@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template("success.html")
@app.route('/logout',methods=['GET', 'POST'])
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')




# query = "SELECT username FROM USER1 WHERE username=?"
# stmt = ibm_db.prepare(connection, query)
# ibm_db.bind_param(stmt, 1, username)
# ibm_db.execute(stmt)
# username = ibm_db.fetch_assoc(stmt)
# print(username)

#dsn = (
#    "DATABASE ={0};"
#    "HOSTNAME ={1};"
#    "PORT ={2};"
#    "UID ={3};"
#    "SECURITY=SSL;"
 #   "PROTOCOL={4};"
#    "PWD ={5};"
#).format(db_name, hostname, port, uid, protocol, pwd)
#connection = ibm_db.connect(dsn, "", "")




#sendgrid mail api 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




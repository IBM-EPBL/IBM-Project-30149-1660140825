from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
app.secret_key ='a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=Certificate.crt;UID=jqy91109;PWD=jKfOzK88qIqZnQQK",'','')

@app.route('/register',methods=['GET', 'POST'])
def register():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        email_id = request.form['email_id']
        phone_no = request.form['phone_no']
        password = request.form['password']
        query = "SELECT * FROM USER1 WHERE username=?;"
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
            insert_sql= "INSERT INTO USER1 values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email_id)
            ibm_db.bind_param(prep_stmt, 3, phone_no)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            account = ibm_db.fetch_assoc(stmt)
            msg = 'You have successfully Logged In!!'
            return render_template('login.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register.html', msg=msg)

@app.route('/login',methods=['GET', 'POST'])
def login():
    global userid
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM USER1 WHERE username=? and password=?;"
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
            return render_template('register.html')
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('welcome.html', msg=msg)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        return render_template('welcome.html', username=username)
    else:
        return render_template('welcome.html', username=username)
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    return render_template('reset.html')


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









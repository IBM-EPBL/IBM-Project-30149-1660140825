from flask import Flask,request,render_template,redirect, url_for
app = Flask(_name_)
@app.route("/login",methods=["POST","GET"])
def log():
    if request.method == "POST":
        user = request.form["Name"]
        email = request.form["Email"]
        number = request.form["phone"]
        return redirect(url_for("user",usr=user,e=email,n=number))
    else:
        return render_template("login.html")
@app.route("/<usr>/<e>/<n>")
def user(usr,e,n):
    return '{} {} {}'.format(usr ,e ,n )
if _name_ =='_main_':
    app.run(debug=True)

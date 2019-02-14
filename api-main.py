from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage
from datetime import date
from credentials import cred


app = Flask(__name__)
client = MongoClient("localhost", 27017)

db = client["elec-vote"]
citizens = db["citizens"]


#list where you can specifically add the places of election
ECIplaces = ["mumbai",  "sikar", "lucknow"]

def emailGen(to, password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(cred.emailId, cred.emailPass)
    msg = EmailMessage()
    message = "Your login password is : " + password
    msg.set_content(message)
    msg['Subject'] = 'Online Voting'
    msg['From'] = "test.proje.niks@gmail.com"
    msg['To'] = to
    s.send_message(msg)
    s.quit()

def password():
    key = "!@#$&*1234567890qwertyuiopasd12345QWERTYUIOPASDFGHJKLZXCVBNM67890fghjklzxcvbnm1234567890!@#$&*"
    key = list(key)
    random.shuffle(key)
    password = key[0:8]
    password = "".join(password)
    return password

def age(dbDate):
    dbDate = dbDate.split("-")
    dbDate = [int(x) for x in dbDate]
    today = str(date.today()).split("-")
    today = [int(x) for x in today]
    age = date(today[0], today[1], today[2]) - date(dbDate[0], dbDate[1], dbDate[2])
    age = age.days // 365
    return age

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/blank")
def blank():
    error = "You cannot leave input fields empty"
    return render_template("main.html", error=error)


@app.route("/ECILogin")
def ECILogin():
    username = (request.form["username"]).lower()
    password = request.form["password"]
    if ( username == cred.username and password == cred.password):
        global otp = password()
        emailGen(cred.ECIEmail,otp)
        return render_template("ECIOtp.html")
    else:
        error = "Username and password provided by you is not correct"
        return render_template("ECILogin.html", error=error)

@app.route("/otpVerify")
def otpVerify():
    otpInput = request.form["otp"]
    if (otp == )


@app.route("/generate", methods=["GET", "POST"])
def generate():
    name = (request.form["name"]).lower()
    uid = request.form["uid"]
    dob = request.form["dob"]
    place = (request.form["place"]).lower()
    print(name, uid , dob, place )
    print(type(name), type(uid), type(dob), type(place))
    error = "Thank you for using Online Voting, your login have been mailed to your registered email id!"
    if (len(name) == 0 or len(str(uid)) == 0 or len(dob) == 0 or len(place) == 0):
        error = "You cannot leave input fields blank"
        return redirect(url_for('blank'))
    else:
        uid = int(request.form["uid"])
        if( db.citizens.find_one({"name": name, "vid": uid, "dob" : dob, "pob" : place}) ):
            #accessing the particular persons data
            reqData = db.citizens.find_one({"name": name,"vid": uid, "dob" : dob, "pob" : place})
            # checking persons age
            dbDate = reqData["dob"]
            ageNow = age(dbDate)
            if (ageNow >= 18 ):
                electPlace = reqData["pob"]
                if electPlace in ECIplaces:
                    #sending email procedure
                    to = reqData["email"]
                    print(to)
                    passwordGen = password()
                    emailGen(to, passwordGen)
                    return render_template("main.html", error=error)
                else:
                    error = "Elections are not happening at your place!"
                    return render_template("main.html", error=error)
            else:
                error = "You are not eligible to vote, you should be atleast of 18 years in order to vote."
                return render_template("main.html", error=error)

        else:
            error = "The details given by you do not match our database"
            return render_template("main.html", error=error)
    # return render_template("success.html")


app.run(debug=True)



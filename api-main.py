from flask import Flask, render_template, request
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
client = MongoClient("localhost", 27017)

db = client["elec-vote"]
citizens = db["citizens"]

def emailGen(to, password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("test.proje.niks@gmail.com", "@imnikhil7")
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


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    name = (request.form["name"]).lower()
    uid = int(request.form["uid"])
    dob = request.form["dob"]
    mobile = int(request.form["mobile"])
    email = request.form["email"]
    place = request.form["place"]
    print(name, uid , dob , mobile, email)
    print(type(name), type(uid), type(dob), type(mobile), type(email))
    error = "Thank you for using Online Voting, your login have been mailed to your registered email id!"
    if( db.citizens.find_one({"name": name, "uid": uid, "dob" : dob, "mobile" : mobile, "email" : email, "place" : place}) ):
        #accessing the particular persons data
        if ()
        reqData = db.citizens.find_one({"name": name,"uid": uid, "dob" : dob, "mobile" : mobile, "email" : email, "place" : place})
        #sending email procedure
        to = reqData["email"]
        passwordGen = password()
        emailGen(to, passwordGen)
        return render_template("main.html", error=error)
    else:
        error = "The details given by you do not match our database"
        return render_template("main.html", error=error)
    # return render_template("success.html")


app.run(debug=True)



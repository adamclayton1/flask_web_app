from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import MAIL, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" #Specifies that we are using an SQLite database.
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

db = SQLAlchemy(app)

mail = MAIL(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(100))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start_date = request.form['date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        occupation = request.form['occupation']

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, start_date=start_date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        db.session.close()

        message_body = f"Thank you for your submission, {first_name}"
        message = Message(subject = "New Form Submission",
                          sender = app.config['MAIL_USERNAME'],
                          recipients = [email],
                          body = message_body)
        #mail.send(message) used to send the message.

        flash(f" {first_name}, your form was submitted successfully", "success")

    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)

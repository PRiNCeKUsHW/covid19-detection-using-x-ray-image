from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Email, Length
from PIL import Image
from pas import own_email,own_password
import smtplib
from smtplib import SMTPException
from socket import timeout
import os
import cv2
from tensorflow.keras.models import load_model

app = Flask('__main__')
app.secret_key = "Sdh4$%Fhf589k@$@5Ghnisl00r6"
Bootstrap5(app)

model_path = 'covid.h5'
model = load_model(model_path)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class CovidForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired()])
    Gender = SelectField('Gender', choices=["Male", "Female"], validators=[DataRequired()])
    Moblie= StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10, message="Mobile number must be 10 digits")])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Address = StringField("Address", validators=[DataRequired()])
    Photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg'], 'Only JPEG files allowed')])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/checking", methods=["GET", "POST"])
def checking():
    form = CovidForm()
    result = None
    if form.validate_on_submit():
        image = form.Photo.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)  # Save the uploaded image to the specified folder

        # Load the saved image and preprocess it
        image = Image.open(image_path)
        image = cv2.imread('uploads/'+filename)
        image = cv2.resize(image, (224, 224))
        image = image.reshape(1, 224, 224, 3)  # Resize the image to match model's input size
        image = image/255.0

        # Make a prediction
        prediction = model.predict(image)

        # Interpret the prediction
        is_positive = prediction < 0.5
        result = True if is_positive else False
        name = form.Name.data
        age = form.Age.data
        gender = form.Gender.data
        number = form.Moblie.data
        email = form.Email.data
        address = form.Address.data
        if result:
            send_email(name,age,gender,number,email,address)
            
        return render_template("result.html",result=result)

    return render_template("test.html", form=form, result=result)


def send_email(name,age,gender,number,email,address):
    email_message = f"Subject:Covid Patient Detail\n\nThis person is positive\nName: {name}\nAge: {age}\nGender: {gender}\nPhone: {number}\nEmail: {email}\nAddress: {address} "
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection:
            connection.starttls()
            connection.login(own_email, own_password)
            connection.sendmail(own_email, own_email, email_message)
    except (timeout, SMTPException) as e:
        print(f"An error occurred: {e}")
        
if __name__ == '__main__':
    app.run(debug=True)
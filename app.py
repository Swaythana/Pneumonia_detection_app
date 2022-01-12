from flask import Flask,flash, sessions
from flask_sqlalchemy import SQLAlchemy


from flask import Flask, render_template
# from __future__ import division, print_function

import sys
import os
import glob
import re
import numpy as np
import cv2

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# User Login module
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    jobrole = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    age = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    username = db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Model saved with Keras model.save()
MODEL_PATH = 'models/trained_model4.h5'

#Load your trained model
model = load_model(MODEL_PATH)
print('Model loaded. Start serving...')

def model_predict(img_path, model):
    img = image.load_img(img_path,target_size=(64,64)) 
    # Preprocessing the image
    img=np.array(img)
    img = cv2.resize(img, (64, 64)) 
    img = img.reshape(1, 64, 64, 3)
    # img = image.img_to_array(img)
    # img = np.expand_dims(img, axis=1)
    preds = model.predict(img)
    return preds

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html') 

@app.route("/signup")
def signup():
    return render_template('signup.html') 

@app.route("/login1", methods=['GET', 'POST'])
def login1():

    name=request.form['name']
    jobrole=request.form['jobrole']
    gender=request.form['gender']
    age=request.form['age']
    email=request.form['email']
    phone=request.form['phoneno']
    username=request.form['username']
    password=request.form['password']
    print(name,jobrole,gender,age,email,phone,username,password)

    user=User(name=name,jobrole=jobrole,gender=gender,age=age,email=email,phone=phone,username=username,password=password)
    print(user)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login')) 

@app.route('/upload', methods=['POST'])
def index():
    # Main page
    global username
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    if user!=None and password==user.password:
        return render_template('index.html',uname=username)
    return render_template('invalidlogin.html')

@app.route('/pd',methods=['GET'])
def pd():
    return render_template('index.html',uname=username)

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds)
        preds=(int(preds[0][0]))
        os.remove(file_path)#removes file from the server after prediction has been returned

        # Arrange the correct return according to the model. 
		# In this model 1 is Pneumonia and 0 is Normal.
        str1 = 'Pneumonia'
        str2 = 'Normal'
        if preds == 1:
            return str1
        else:
            return str2
    return None

@app.route("/logout")
def logout():
    return render_template('logout.html')   

if __name__=='__main__':
    app.run(debug=True)
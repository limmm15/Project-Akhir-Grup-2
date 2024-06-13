import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# MONGODB_URI = os.environ.get("MONGODB_URI")
# DB_NAME =  os.environ.get("DB_NAME")

# client = MongoClient(MONGODB_URI)
# db = client[DB_NAME]

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/nan',methods=['GET','POST'])
def nan():
    return render_template('nan.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/admission',methods=['GET','POST'])
def admissions():
    return render_template('admissions.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/course',methods=['GET','POST'])
def course():
    return render_template('course.html')

@app.route('/courses',methods=['GET','POST'])
def courses():
    return render_template('courses.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/news',methods=['GET','POST'])
def news():
    return render_template('news.html')


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
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

@app.route('/profile',methods=['GET','POST'])
def Profile():
    return render_template('profile.html')

@app.route('/SarPras',methods=['GET','POST'])
def SarPras():
    return render_template('sarpras.html')

@app.route('/galeri',methods=['GET','POST'])
def galeri():
    return render_template('galeri.html')

@app.route('/prestasi',methods=['GET','POST'])
def prestasi():
    return render_template('prestasi.html')

@app.route('/pengumuman',methods=['GET','POST'])
def pengumuman():
    return render_template('pengumuman.html')

@app.route('/daftar',methods=['GET','POST'])
def daftar():
    return render_template('daftar.html')

@app.route('/loginA',methods=['GET','POST'])
def loginA():
    return render_template('loginA.html')

@app.route('/loginP',methods=['GET','POST'])
def loginP():
    return render_template('loginP.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
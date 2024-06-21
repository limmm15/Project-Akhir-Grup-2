from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
import jwt
import hashlib
import datetime
from datetime import datetime, timedelta
import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)

SECRET_KEY = 'KELOMPOK1'
TOKEN_KEY = 'mytoken'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/photos'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16 MB max upload size

#app.config['UPLOAD_FOLDER'] = 'uploads'
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/profile',methods=['GET','POST'])
def Profile():
    guru_contents = db.guru.find()
    return render_template('profile.html', contents=guru_contents)

@app.route('/SarPras',methods=['GET','POST'])
def SarPras():
    return render_template('sarpras.html')

@app.route('/galeri',methods=['GET','POST'])
def galeri():
    return render_template('galeri.html')

@app.route('/prestasi',methods=['GET','POST'])
def prestasi():
    prestasi_contents = db.prestasi.find()
    return render_template('prestasi.html', contents=prestasi_contents)

@app.route('/pengumuman',methods=['GET','POST'])
def pengumuman():
    pengumuman_contents = db.pengumuman.find()
    return render_template('pengumuman.html', contents=pengumuman_contents)

@app.route('/daftar',methods=['GET','POST'])
def daftar():
    return render_template('daftar.html')

#Daftar
@app.route('/submit', methods=['POST'])
def submit():
   nama = request.form['nama']
   nama_orang_tua = request.form['nama_orang_tua']
   alamat = request.form['alamat']

   kartu_keluarga = request.files['kartu_keluarga']
   akte_kelahiran = request.files['akte_kelahiran']
   ijazah_tk = request.files['ijazah_tk']

   filenames = {}
   
   if kartu_keluarga:
       filename = os.path.join(app.config['UPLOAD_FOLDER'], kartu_keluarga.filename)
       kartu_keluarga.save(filename)
       filenames['kartu_keluarga'] = filename
   
   if akte_kelahiran:
       filename = os.path.join(app.config['UPLOAD_FOLDER'], akte_kelahiran.filename)
       akte_kelahiran.save(filename)
       filenames['akte_kelahiran'] = filename
   
   if ijazah_tk:
       filename = os.path.join(app.config['UPLOAD_FOLDER'], ijazah_tk.filename)
       ijazah_tk.save(filename)
       filenames['ijazah_tk'] = filename

   db.daftar.insert_one({
       "nama": nama,
       "nama_orang_tua": nama_orang_tua,
       "alamat": alamat,
       "files": filenames
   })

   return redirect(url_for('form', success=True))

@app.route('/loginA',methods=['GET','POST'])
def loginA():
    return render_template('loginA.html')

@app.route('/loginP',methods=['GET','POST'])
def loginP():
    return render_template('loginP.html')

# Login Admin
@app.route("/sign_in_adm", methods=["POST"])
def sign_in_adm():
   username_receive = request.form["username_give"]
   password_receive = request.form["password_give"]
   pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
   result = db.admin.find_one(
       {
           "username": username_receive,
           "password": pw_hash,
       }
   )
   if result:
       payload = {
           "id": username_receive,
           "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
       }
       token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

       return jsonify(
           {
               "result": "success",
               "token": token,
           }
       )
   else:
       return jsonify(
           {
               "result": "fail",
               "msg": "We could not find a user with that id/password combination",
           }
       )


# Login Pengunjung
@app.route("/sign_in", methods=["POST"])
def sign_in():
   username_receive = request.form["username_give"]
   password_receive = request.form["password_give"]
   pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
   result = db.users.find_one(
       {
           "username": username_receive,
           "password": pw_hash,
       }
   )
   if result:
       payload = {
           "id": username_receive,
           "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
       }
       token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

       return jsonify(
           {
               "result": "success",
               "token": token,
           }
       )
   else:
       return jsonify(
           {
               "result": "fail",
               "msg": "We could not find a user with that id/password combination",
           }
       )

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
   username_receive = request.form['username_give']
   password_receive = request.form['password_give']
   password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
   doc = {
       "username": username_receive,                               
       "password": password_hash,                                  
       "profile_name": username_receive,                           
       "profile_pic": "",                                          
       "profile_pic_real": "profile_pics/profile_placeholder.png", 
       "profile_info": ""                                          
   }
   db.users.insert_one(doc)
   return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
   username_receive = request.form.get('username_give')
   exists = bool(db.users.find_one({'username': username_receive}))
   return jsonify({'result': 'success', 'exists': exists})

# Admin
@app.route('/uploads/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class SarprasForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    judul = StringField('Judul', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PengumumanForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    judul = StringField('Judul', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GuruForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    judul = StringField('Judul', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GaleriForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    judul = StringField('Judul', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PrestasiForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    judul = StringField('Judul', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/dashboard')
def dashboard():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        return render_template("dashboard.html", user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/sarprasA')
def sarprasA():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        sarpras_contents = db.sarpras.find()
        return render_template("sarprasA.html", contents=sarpras_contents, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/add_sarpras', methods=['GET', 'POST'])
def add_sarpras():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form = SarprasForm()
        if form.validate_on_submit():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.sarpras.insert_one({'foto': filename, 'judul': judul, 'keterangan': keterangan})
                return redirect(url_for('sarprasA'))
            else:
                flash('Foto is required')
        return render_template('add_sarpras.html', form=form, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/edit_sarpras/<id>', methods=['GET', 'POST'])
def edit_sarpras(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        content = db.sarpras.find_one({'_id': ObjectId(id)})
        form = SarprasForm(obj=content)
        if request.method == 'POST' and form.validate():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.sarpras.update_one({'_id': ObjectId(id)}, {"$set": {'foto': filename, 'judul': judul, 'keterangan': keterangan}})
            else:
                db.sarpras.update_one({'_id': ObjectId(id)}, {"$set": {'judul': judul, 'keterangan': keterangan}})
                return redirect(url_for('sarprasA'))
        return render_template('edit_sarpras.html', form=form, content=content, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/delete_sarpras/<id>', methods=['POST'])
def delete_sarpras(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.sarpras.delete_one({'_id': ObjectId(id)})
        return render_template('sarprasA.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))


@app.route('/pengumumanA')
def pengumumanA():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        pengumuman_contents = db.pengumuman.find()
        return render_template('pengumumanA.html', contents=pengumuman_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/add_pengumuman', methods=['GET', 'POST'])
def add_pengumuman():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form = PengumumanForm()
        if form.validate_on_submit():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.pengumuman.insert_one({'foto': filename, 'judul': judul, 'keterangan': keterangan})
                return redirect(url_for('pengumumanA'))
            else:
                flash('Foto is required')
        return render_template('add_pengumuman.html', form=form, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/edit_pengumuman/<id>', methods=['GET', 'POST'])
def edit_pengumuman(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        content = db.pengumuman.find_one({'_id': ObjectId(id)})
        form = PengumumanForm(obj=content)
        if request.method == 'POST' and form.validate():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.pengumuman.update_one({'_id': ObjectId(id)}, {"$set": {'foto': filename, 'judul': judul, 'keterangan': keterangan}})
            else:
                db.pengumuman.update_one({'_id': ObjectId(id)}, {"$set": {'judul': judul, 'keterangan': keterangan}})
            return redirect(url_for('pengumumanA'))
        return render_template('edit_pengumuman.html', form=form, content=content, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/delete_pengumuman/<id>', methods=['POST'])
def delete_pengumuman(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.pengumuman.delete_one({'_id': ObjectId(id)})
        return render_template('pengumumanA.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/guruA')
def guruA():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        guru_contents = db.guru.find()
        return render_template('guru.html', contents=guru_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/add_guru', methods=['GET', 'POST'])
def add_guru():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form = GuruForm()
        if form.validate_on_submit():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.guru.insert_one({'foto': filename, 'judul': judul, 'keterangan': keterangan})
                return redirect(url_for('guruA'))
            else:
                flash('Foto is required')
        return render_template('add_guru.html', form=form, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/edit_guru/<id>', methods=['GET', 'POST'])
def edit_guru(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        content = db.guru.find_one({'_id': ObjectId(id)})
        form = GuruForm(obj=content)
        if request.method == 'POST' and form.validate():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.guru.update_one({'_id': ObjectId(id)}, {"$set": {'foto': filename, 'judul': judul, 'keterangan': keterangan}})
            else:
                db.guru.update_one({'_id': ObjectId(id)}, {"$set": {'judul': judul, 'keterangan': keterangan}})
            return redirect(url_for('guruA'))
        return render_template('edit_guru.html', form=form, content=content, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/delete_guru/<id>', methods=['POST'])
def delete_guru(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.guru.delete_one({'_id': ObjectId(id)})
        return render_template('guru.html',user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))


@app.route('/galeriA')
def galeriA():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        galeri_contents = db.galeri.find()
        return render_template('galeriA.html', contents=galeri_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/add_galeri', methods=['GET', 'POST'])
def add_galeri():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form = GaleriForm()
        if form.validate_on_submit():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.galeri.insert_one({'foto': filename, 'judul': judul, 'keterangan': keterangan})
                return redirect(url_for('galeriA'))
            else:
                flash('Foto is required')
        return render_template('add_galeri.html', form=form, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/edit_galeri/<id>', methods=['GET', 'POST'])
def edit_galeri(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        content = db.galeri.find_one({'_id': ObjectId(id)})
        form = GaleriForm(obj=content)
        if request.method == 'POST' and form.validate():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.galeri.update_one({'_id': ObjectId(id)}, {"$set": {'foto': filename, 'judul': judul, 'keterangan': keterangan}})
            else:
                db.galeri.update_one({'_id': ObjectId(id)}, {"$set": {'judul': judul, 'keterangan': keterangan}})
            return redirect(url_for('galeriA'))
        return render_template('edit_galeri.html', form=form, content=content, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/delete_galeri/<id>', methods=['POST'])
def delete_galeri(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.galeri.delete_one({'_id': ObjectId(id)})
        return render_template('galeri.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/prestasiA')
def prestasiA():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        prestasi_contents = db.prestasi.find()
        return render_template('prestasiA.html', contents=prestasi_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/add_prestasi', methods=['GET', 'POST'])
def add_prestasi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form = PrestasiForm()
        if form.validate_on_submit():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.prestasi.insert_one({'foto': filename, 'judul': judul, 'keterangan': keterangan})
                return redirect(url_for('prestasiA'))
            else:
                flash('Foto is required')
        return render_template('add_prestasi.html', form=form, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/edit_prestasi/<id>', methods=['GET', 'POST'])
def edit_prestasi(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        content = db.prestasi.find_one({'_id': ObjectId(id)})
        form = PrestasiForm(obj=content)
        if request.method == 'POST' and form.validate():
            judul = form.judul.data
            keterangan = form.keterangan.data
            foto = form.foto.data
            if foto:
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.prestasi.update_one({'_id': ObjectId(id)}, {"$set": {'foto': filename, 'judul': judul, 'keterangan': keterangan}})
            else:
                db.prestasi.update_one({'_id': ObjectId(id)}, {"$set": {'judul': judul, 'keterangan': keterangan}})
            return redirect(url_for('prestasiA'))
        return render_template('edit_prestasi.html', form=form, content=content, user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/delete_prestasi/<id>', methods=['POST'])
def delete_prestasi(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.prestasi.delete_one({'_id': ObjectId(id)})
        return render_template('prestasiA.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))

@app.route('/form_pendaftaran')
def form_pendaftaran():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        form_pendaftaran_contents = db.form_pendaftaran.find()
        return render_template('form_pendaftaran.html', contents=form_pendaftaran_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))
    
@app.route('/user')
def user():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        user_contents = db.user.find()
        return render_template('user.html', users=user_contents, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginA", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginA", msg="There was problem logging you in"))

@app.route('/delete_user/<id>', methods=['POST'])
def delete_user(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.admin.find_one({"username": payload["id"]})
        db.user.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('user'))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("loginA"))


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)

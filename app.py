from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename

client = MongoClient('')
db = client.

app = Flask(__name__)

SECRET_KEY = 'KELOMPOK1'
TOKEN_KEY = 'mytoken'

# Konfigurasi database MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_puspamukti'

mysql = MySQL(app)

@app.route('/loginP')
def loginP():
    return render_template('loginP.html')

@app.route('/user/<username>', methods=['GET'])
def user(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = username == payload.get('id')
        user_info = db.users.find_one(
            {'username': username},
            {'_id': False}
        )
        return render_template(
            'user.html',
            user_info=user_info,
            status=status
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

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
    hashed_username = hashlib.sha256(username_receive.encode('utf-8')).hexdigest()
    exists = bool(db.users.find_one({'username': hashed_username}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sarpras')
def sarpras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sarpras")
    rv = cur.fetchall()

    sarpras_list = []
    for row in rv:
        sarpras_item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'img_url': row[3],
            'action_link': row[4]
        }
        sarpras_list.append(sarpras_item)

    cur.execute("SELECT * FROM ekstrakulikuler")
    rv = cur.fetchall()

    ekstrakulikuler_list = []
    for row in rv:
        ekstrakulikuler_item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'img_url': row[3],
            'action_link': row[4]
        }
        ekstrakulikuler_list.append(ekstrakulikuler_item)
    
    cur.close()

    return render_template('views/sarpras.html', sarpras=sarpras_list, ekstrakulikuler=ekstrakulikuler_list)

@app.route('/galeri')
def galeri():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM galeri")
    rv = cur.fetchall()
    cur.close()
    galeri_list = []
    for row in rv:
        galeri_item = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'img_url': row[3],
            'action_link': row[4]
        }
        galeri_list.append(galeri_item)
    return render_template('views/galeri.html', galeri=galeri_list)


if __name__ == '__main__':
    app.run(debug=True)

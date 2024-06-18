from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Konfigurasi database MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_puspamukti'

mysql = MySQL(app)

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
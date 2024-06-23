from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Konfigurasi database MongoDB
client = MongoClient('localhost', 27017)
db = client['db_puspamukti']

@app.route('/sarpras')
def sarpras():
    sarpras_collection = db['sarpras']
    sarpras_data = sarpras_collection.find()

    sarpras_list = []
    for row in sarpras_data:
        sarpras_item = {
            'id': str(row['_id']),
            'title': row['title'],
            'description': row['description'],
            'img_url': row['img_url'],
            'action_link': row['action_link']
        }
        sarpras_list.append(sarpras_item)

    ekstrakulikuler_collection = db['ekstrakulikuler']
    ekstrakulikuler_data = ekstrakulikuler_collection.find()

    ekstrakulikuler_list = []
    for row in ekstrakulikuler_data:
        ekstrakulikuler_item = {
            'id': str(row['_id']),
            'title': row['title'],
            'description': row['description'],
            'img_url': row['img_url'],
            'action_link': row['action_link']
        }
        ekstrakulikuler_list.append(ekstrakulikuler_item)

    return render_template('views/sarpras.html', sarpras=sarpras_list, ekstrakulikuler=ekstrakulikuler_list)

@app.route('/galeri')
def galeri():
    galeri_collection = db['galeri']
    galeri_data = galeri_collection.find()
    
    galeri_list = []
    for row in galeri_data:
        galeri_item = {
            'id': str(row['_id']),
            'title': row['title'],
            'description': row['description'],
            'img_url': row['img_url'],
            'action_link': row['action_link']
        }
        galeri_list.append(galeri_item)

    return render_template('views/galeri.html', galeri=galeri_list)

def get_version():
    return jsonify({'version': '1.0.0'})


if __name__ == '__main__':
    app.run(debug=True)

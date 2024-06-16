from flask import Flask, render_template

app = Flask(__name__)

@app.route('/sarpras')
def sarpras():
    return render_template('views/sarpras.html')

@app.route('/galeri')
def galeri():
    return render_template('views/galeri.html')


if __name__ == '__main__':
    app.run(debug=True)
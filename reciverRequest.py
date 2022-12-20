from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'Gu1d0M4qu1n0l4'
db = SQLAlchemy(app)

class Embalaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(20), unique=True, nullable=False)
    metros = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# set up post for embalaje
@app.route('/', methods=['POST'])
def embalaje():
    mac = request.form['mac']
    metros = request.form['metros']
    embalaje = Embalaje(mac=mac, metros=metros)
    try:
        db.session.add(embalaje)
        db.session.commit()
        return jsonify({'message': 'New packaging created!'})
    except:
        return jsonify({'message': 'There was an issue creating your packaging'})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
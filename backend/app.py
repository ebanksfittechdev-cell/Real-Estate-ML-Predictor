from flask import Flask
from models import db
from predict import predict_bp
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)
app.register_blueprint(predict_bp)

with app.app_context():
    db.create_all()   # creates app.db and the table on first run, if not already there

if __name__ == '__main__':
    app.run(debug=True)
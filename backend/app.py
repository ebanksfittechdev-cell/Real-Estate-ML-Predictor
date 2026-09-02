import os
from flask import Flask
from models import db
from predict import predict_bp
from flask_cors import CORS

app = Flask(__name__)


if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)
app.register_blueprint(predict_bp)

with app.app_context():
    db.create_all()


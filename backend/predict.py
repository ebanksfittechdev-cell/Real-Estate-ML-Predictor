from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
import os

from models import db, PredictionRecord

predict_bp = Blueprint('predict', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))

FEATURES = [
    'Overall Qual', 'Gr Liv Area', 'Garage Cars', 'Total Bsmt SF',
    'Year Built', 'Full Bath', 'Year Remod/Add', 'Garage Yr Blt',
    'Mas Vnr Area', 'Has Garage'
]

# min/max bounds based on realistic values for this dataset
VALIDATION_RULES = {
    'Overall Qual':    {'min': 1,    'max': 10},
    'Gr Liv Area':     {'min': 100,  'max': 6000},
    'Garage Cars':     {'min': 0,    'max': 5},
    'Total Bsmt SF':   {'min': 0,    'max': 4000},
    'Year Built':      {'min': 1800, 'max': 2026},
    'Full Bath':       {'min': 0,    'max': 5},
    'Year Remod/Add':  {'min': 1800, 'max': 2026},
    'Garage Yr Blt':   {'min': 1800, 'max': 2026},
    'Mas Vnr Area':    {'min': 0,    'max': 2000},
    'Has Garage':      {'min': 0,    'max': 1},
}

def validate_input(data):
    errors = []

    for feature in FEATURES:
        if feature not in data:
            errors.append(f"Missing field: {feature}")
            continue

        value = data[feature]

        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{feature} must be a number")
            continue

        rules = VALIDATION_RULES[feature]
        if value < rules['min'] or value > rules['max']:
            errors.append(f"{feature} must be between {rules['min']} and {rules['max']}")

    return errors


@predict_bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON body provided'}), 400

    errors = validate_input(data)
    if errors:
        return jsonify({'errors': errors}), 400

    input_df = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = float(model.predict(input_df)[0])

    record = PredictionRecord(
        overall_qual=data['Overall Qual'],
        gr_liv_area=data['Gr Liv Area'],
        garage_cars=data['Garage Cars'],
        total_bsmt_sf=data['Total Bsmt SF'],
        year_built=data['Year Built'],
        full_bath=data['Full Bath'],
        year_remod_add=data['Year Remod/Add'],
        garage_yr_blt=data['Garage Yr Blt'],
        mas_vnr_area=data['Mas Vnr Area'],
        has_garage=data['Has Garage'],
        predicted_price=round(prediction, 2)
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'predicted_price': round(prediction, 2), 'record_id': record.id})
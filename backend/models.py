from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PredictionRecord(db.Model):
    __tablename__ = 'prediction_records'

    id = db.Column(db.Integer, primary_key=True)

    # Input features
    overall_qual = db.Column(db.Integer, nullable=False)
    gr_liv_area = db.Column(db.Float, nullable=False)
    garage_cars = db.Column(db.Float, nullable=False)
    total_bsmt_sf = db.Column(db.Float, nullable=False)
    year_built = db.Column(db.Integer, nullable=False)
    full_bath = db.Column(db.Integer, nullable=False)
    year_remod_add = db.Column(db.Integer, nullable=False)
    garage_yr_blt = db.Column(db.Float, nullable=False)
    mas_vnr_area = db.Column(db.Float, nullable=False)
    has_garage = db.Column(db.Integer, nullable=False)

    # Output
    predicted_price = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'overall_qual': self.overall_qual,
            'gr_liv_area': self.gr_liv_area,
            'garage_cars': self.garage_cars,
            'total_bsmt_sf': self.total_bsmt_sf,
            'year_built': self.year_built,
            'full_bath': self.full_bath,
            'year_remod_add': self.year_remod_add,
            'garage_yr_blt': self.garage_yr_blt,
            'mas_vnr_area': self.mas_vnr_area,
            'has_garage': self.has_garage,
            'predicted_price': self.predicted_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
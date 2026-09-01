import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const FIELDS = [
  { key: 'Overall Qual',   label: 'Overall Quality (1-10)', min: 1,    max: 10 },
  { key: 'Gr Liv Area',    label: 'Living Area (sq ft)',     min: 100,  max: 6000 },
  { key: 'Garage Cars',    label: 'Garage Capacity (cars)',  min: 0,    max: 5 },
  { key: 'Total Bsmt SF',  label: 'Basement Area (sq ft)',   min: 0,    max: 4000 },
  { key: 'Year Built',     label: 'Year Built',              min: 1800, max: 2026 },
  { key: 'Full Bath',      label: 'Full Bathrooms',          min: 0,    max: 5 },
  { key: 'Year Remod/Add', label: 'Year Remodeled',          min: 1800, max: 2026 },
  { key: 'Garage Yr Blt',  label: 'Garage Year Built',       min: 1800, max: 2026 },
  { key: 'Mas Vnr Area',   label: 'Masonry Veneer (sq ft)',  min: 0,    max: 2000 },
];

function PredictionForm() {
  const [form, setForm] = useState(FIELDS.reduce((acc, f) => ({ ...acc, [f.key]: '' }), {}));
  const [hasGarage, setHasGarage] = useState(true);
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (key, value) => setForm(prev => ({ ...prev, [key]: value }));

  const getPayload = () => {
    const payload = {};
    FIELDS.forEach(({ key }) => {
      payload[key] = Number(form[key]);
    });
    payload['Has Garage'] = hasGarage ? 1 : 0;
    return payload;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setErrors({});
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(getPayload()),
      });

      const data = await res.json();

      if (!res.ok) {
        setErrors({ submit: data.errors ? data.errors.join(', ') : (data.error || 'Prediction failed') });
        return;
      }

      setResult(data.predicted_price);
    } catch (err) {
      setErrors({ submit: 'Could not reach the server. Is the backend running?' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      {FIELDS.map(({ key, label }) => (
        <div className="field" key={key}>
          <label htmlFor={key}>{label}</label>
          <input
            id={key}
            type="number"
            value={form[key]}
            onChange={(e) => handleChange(key, e.target.value)}
          />
          {errors[key] && <span className="error">{errors[key]}</span>}
        </div>
      ))}

      <div className="field checkbox-field">
        <label htmlFor="hasGarage">Has Garage</label>
        <input
          id="hasGarage"
          type="checkbox"
          checked={hasGarage}
          onChange={(e) => setHasGarage(e.target.checked)}
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Predicting...' : 'Predict Price'}
      </button>

      {errors.submit && <p className="submit-error">{errors.submit}</p>}

      {result !== null && (
        <div className="result">
          <span className="result-label">Predicted Price</span>
          <span className="result-value">
            ${result.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
        </div>
      )}
    </form>
  );
}

export default PredictionForm;
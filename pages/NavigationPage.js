// src/pages/NavigationPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function NavigationPage() {
  const [locations, setLocations] = useState([]);
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/locations')
      .then(res => {
        setLocations(res.data.locations);
      })
      .catch(err => {
        console.error("Failed to fetch locations:", err);
      });
  }, []);

  const handleSubmit = () => {
    if (!start || !end) return;
    axios.post('http://localhost:5000/find_path', { start: parseInt(start), end: parseInt(end) })
      .then(res => {
        setResult(res.data);
        setError(null);
      })
      .catch(err => {
        setError("Path not found or backend error.");
        setResult(null);
      });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Campus Navigation</h2>

      <div>
        <label>From:</label>
        <select value={start} onChange={e => setStart(e.target.value)}>
          <option value=''>-- Select Start --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>{loc.name}</option>
          ))}
        </select>

        <label style={{ marginLeft: '20px' }}>To:</label>
        <select value={end} onChange={e => setEnd(e.target.value)}>
          <option value=''>-- Select End --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>{loc.name}</option>
          ))}
        </select>

        <button onClick={handleSubmit} style={{ marginLeft: '20px' }}>Find Path</button>
      </div>

      <div style={{ marginTop: '30px' }}>
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {result && (
          <div>
            <h4>Path:</h4>
            <ul>
              {result.path.map((loc, idx) => (
                <li key={idx}>{loc}</li>
              ))}
            </ul>

            <h4>Step-by-Step Instructions:</h4>
            <ul>
              {result.steps.map((step, idx) => (
                <li key={idx}>{step.instruction} - {step.distance} meters</li>
              ))}
            </ul>

            <p><strong>Total Distance:</strong> {result.total_distance} meters</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default NavigationPage;

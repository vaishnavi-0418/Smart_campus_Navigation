// src/pages/NavigationPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function NavigationPage() {
  const [locations, setLocations] = useState([]);
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [paths, setPaths] = useState([]);
  const [selectedPath, setSelectedPath] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/locations')
      .then(res => {
        setLocations(res.data.locations);
      })
      .catch(err => {
        console.error('Error fetching locations:', err);
      });
  }, []);

  const handleFindPath = () => {
    if (!start || !end) return;

    axios.post('http://localhost:5000/find_path', { start: parseInt(start), end: parseInt(end) })
      .then(res => {
        const { shortest_path, other_paths } = res.data;
        setPaths([shortest_path, ...other_paths]);
        setSelectedPath(shortest_path);  // default select shortest
        setError(null);
      })
      .catch(err => {
        console.error('Error finding path:', err);
        setPaths([]);
        setSelectedPath(null);
        setError("Path not found");
      });
  };

  const handleSelectPath = (index) => {
    setSelectedPath(paths[index]);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>Smart Campus Navigation</h2>

      <div>
        <label>From: </label>
        <select value={start} onChange={e => setStart(e.target.value)}>
          <option value=''>-- Select Start --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>{loc.name}</option>
          ))}
        </select>

        <label style={{ marginLeft: '20px' }}>To: </label>
        <select value={end} onChange={e => setEnd(e.target.value)}>
          <option value=''>-- Select End --</option>
          {locations.map(loc => (
            <option key={loc.id} value={loc.id}>{loc.name}</option>
          ))}
        </select>

        <button onClick={handleFindPath} style={{ marginLeft: '20px' }}>Find Path</button>
      </div>

      <div style={{ marginTop: '30px' }}>
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {/* Show path options */}
        {paths.length > 0 && (
          <div style={{ marginBottom: '20px' }}>
            <h4>Available Paths:</h4>
            {paths.map((p, idx) => (
              <button key={idx} onClick={() => handleSelectPath(idx)} style={{ marginRight: '10px' }}>
                {idx === 0 ? 'Shortest Path' : `Path ${idx}`}
              </button>
            ))}
          </div>
        )}

        {/* Show selected path details */}
        {selectedPath && (
          <div>
            <h4>Selected Path:</h4>
            <ul>
              {selectedPath.path.map((loc, idx) => (
                <li key={idx}>{loc}</li>
              ))}
            </ul>

            <h4>Instructions:</h4>
            <ul>
              {selectedPath.steps.map((step, idx) => (
                <li key={idx}>
                  {step.instruction} - {step.distance} meters
                </li>
              ))}
            </ul>

            <p><strong>Total Distance:</strong> {selectedPath.total_distance} meters</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default NavigationPage;

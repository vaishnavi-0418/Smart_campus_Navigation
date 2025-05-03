import React, { useEffect, useState } from 'react';
import { getLocations } from '../api';

const LocationSelector = ({ onStartChange, onEndChange }) => {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    async function fetchLocations() {
      try {
        const res = await getLocations();
        setLocations(res.data.locations);
        console.log(res.data.locations); // 
      } catch (err) {
        console.error('Error fetching locations:', err);
      }
    }

    fetchLocations();
  }, []);

  return (
    <div>
      <h3>Select Start and End Locations</h3>

      <label>Start:</label>
      <select onChange={(e) => onStartChange(parseInt(e.target.value))}>
        <option value="">-- Select Start --</option>
        {locations.map((loc) => (
          <option key={loc.id} value={loc.id}>{loc.name}</option>
        ))}
      </select>

      <br /><br />

      <label>End:</label>
      <select onChange={(e) => onEndChange(parseInt(e.target.value))}>
        <option value="">-- Select End --</option>
        {locations.map((loc) => (
          <option key={loc.id} value={loc.id}>{loc.name}</option>
        ))}
      </select>
    </div>
  );
};

export default LocationSelector;

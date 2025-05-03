import React, { useState } from 'react';
import { Outlet, Link } from 'react-router-dom';
import './MainApp.css';

function MainApp() {
  const [collapsed, setCollapsed] = useState(false);

  const handleToggle = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div className="main-container">
      <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
        <button className="toggle-button" onClick={handleToggle}>
          {collapsed ? '→' : '←'}
        </button>
        <h3>SmartNav</h3>
        <ul>
          <li><Link to="/navigation" style={{ color: 'white', textDecoration: 'none' }}>Navigation</Link></li>
          <li><Link to="/nearby" style={{ color: 'white', textDecoration: 'none' }}>Nearby</Link></li>
          <li><Link to="/parking" style={{ color: 'white', textDecoration: 'none' }}>Parking</Link></li>
          <li><Link to="/events" style={{ color: 'white', textDecoration: 'none' }}>Events</Link></li>
          <li><Link to="/admin" style={{ color: 'white', textDecoration: 'none' }}>Admin Panel</Link></li>
        </ul>
      </div>

      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
}

export default MainApp;

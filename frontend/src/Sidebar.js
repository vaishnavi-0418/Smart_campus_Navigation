// src/Sidebar.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css'; // We'll also update this

function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <button onClick={toggleSidebar} className="toggle-btn">
        ☰
      </button>

      {!isCollapsed && <h3>Dashboard</h3>}
      <ul>
        <li><Link to="/navigation">{isCollapsed ? 'Nv' : 'Navigation'}</Link></li>
        <li><Link to="/nearby">{isCollapsed ? 'nbL' : 'Nearby Locations'}</Link></li>
        <li><Link to="/parking">{isCollapsed ? 'Prk' : 'Parking Info'}</Link></li>
        <li><Link to="/events">{isCollapsed ? 'Ev' : 'Events'}</Link></li>
        <li><Link to="/admin">{isCollapsed ? 'Ac' : 'Admin Panel'}</Link></li>
      </ul>
    </div>
  );
}

export default Sidebar;

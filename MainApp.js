// src/MainApp.js
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';  // Assuming you have a Sidebar.js

import './MainApp.css'; // Your CSS styling

function MainApp() {
  return (
    <div className="main-app">
      <Sidebar />
      <div className="content">
        <Outlet /> 
      </div>
    </div>
  );
}

export default MainApp;

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainApp from './MainApp';
import NavigationPage from './pages/NavigationPage';
import Nearby from './pages/Nearby';
import Parking from './pages/Parking';
import Events from './pages/Events';
import AdminPanel from './pages/AdminPanel';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainApp />}>
          <Route path="navigation" element={<NavigationPage />} />
          <Route path="nearby" element={<Nearby />} />
          <Route path="parking" element={<Parking />} />
          <Route path="events" element={<Events />} />
          <Route path="admin" element={<AdminPanel />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom/client';
import AuthPage from './AuthPage';
import '../../css/input.css'; // Tailwind styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthPage />
  </React.StrictMode>
);

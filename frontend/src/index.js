import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root')); // Encontra a <div id="root"> no index.html
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();

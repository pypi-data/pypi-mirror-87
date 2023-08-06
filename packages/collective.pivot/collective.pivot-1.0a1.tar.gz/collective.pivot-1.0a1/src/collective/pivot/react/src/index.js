import React from 'react';
import ReactDOM from 'react-dom';
import "core-js/stable"; // TODO delete. https://stackoverflow.com/questions/53558916/babel-7-referenceerror-regeneratorruntime-is-not-defined
import "regenerator-runtime/runtime"; // TODO delete. https://stackoverflow.com/questions/53558916/babel-7-referenceerror-regeneratorruntime-is-not-defined
// import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';
import 'leaflet/dist/images/marker-icon.png';
import './index.css';


import App from './App';

const url = document.getElementById('root').getAttribute('data-pivot-view-url');
const details = document.getElementById('root').getAttribute('data-pivot-details-url');

ReactDOM.render(
  <React.StrictMode>
    <App pivot_url={url} details_url={details}  />
  </React.StrictMode>,
  document.getElementById('root')
);

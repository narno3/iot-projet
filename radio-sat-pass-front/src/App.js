import React, { useState, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './App.css';

import Header from './components/Header';
import LeftSidebar from './components/LeftSidebar';
import RightSidebar from './components/RightSidebar';
import MapComponent from './components/MapComponent';

// Fix for default marker icon issue in React-Leaflet
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import { Satellites } from './components/Satellites';

let DefaultIcon = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;


function App() {
  // State to manage the map's center and the visibility of input fields
  const [map, setMap] = useState(null);
  const [userPosition, setUserPos] = useState({
    longitude: 2.35,
    latitude: 48.85
  }); // Default center
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const new_long = parseFloat(formData.get('longitude'));
    const new_lat = parseFloat(formData.get('latitude'));
    setUserPos({
      longitude: new_long,
      latitude: new_lat,
    });
  };

  return (
    <body className="App">
      <Header />
      <div class="container">
        <LeftSidebar />
        <MapComponent setmap = {setMap} userPosition={userPosition} />
        <RightSidebar map = {map} pos={userPosition} setPos= {setUserPos} />
      </div>
    </body>
  );
}

export default App;

import React, { useState, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './App.css';

// Fix for default marker icon issue in React-Leaflet
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

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

const UpdateView = ({ center, zoom }) => {
  const map = useMap(); // Get the map instance

  useEffect(() => {
    map.setView(center, map.getZoom()); // Dynamically update the view whenever center or zoom changes
  }, [center, zoom, map]);

  return null; // No need to render anything, just updating the view
};

function App() {
  // State to manage the map's center and the visibility of input fields
  const [map, setMap] = useState(null);
  const mapRef = useRef(null);
  const [userPosition, setUserPos] = useState({
    longitude: 51.505,
    latitude: 0.09
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

  const fillBlueOptions = { fillColor: 'blue' }

  return (
    <div className="App">
      <h1>Leaflet Map in React</h1>

      {/* Button to toggle input fields */}
      <form onSubmit={handleSubmit}>
        <input
            id="longitude"
            className="form-field"
            type="text"
            placeholder="Longitude"
            name="longitude"
            // value={userPosition.longitude}
            // onChange={handleLongitudeChange}
        />
        <input
            id="latitude"
            className="form-field"
            type="text"
            placeholder="Latitude"
            name="latitude"
            // value={userPosition.latitude}
            // onChange={handleLatitudeChange}
        />
        <button type="submit">Update Position</button>
      </form>

      {/* Leaflet Map */}
      <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '500px', width: '100%', marginTop: '20px' }} >
      <UpdateView center={[userPosition.latitude, userPosition.longitude]} zoom={10} />
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <Marker position={[userPosition.latitude, userPosition.longitude]}>
          <Popup>Current position: {userPosition.latitude}, {userPosition.longitude}</Popup>
        </Marker>
        <Circle center={[userPosition.latitude, userPosition.longitude]} pathOptions={fillBlueOptions} radius={4600} />
      </MapContainer>
    </div>
  );
}

export default App;

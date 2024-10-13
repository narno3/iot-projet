
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle } from 'react-leaflet';
import React, { useState, useRef, useEffect } from 'react';
import { Satellites } from './Satellites';
import { Trajectory } from './Trajectory';

import L from 'leaflet';

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

export default function MapComponent( {setmap, userPosition, satInfos} ) {
    const fillBlueOptions = { fillColor: 'blue' }

    return (
        <main class="map-area">
            {/* Leaflet Map */}
            <MapContainer center={[51.505, -0.09]} zoom={5} style={{ height: '100%', width: '100%'}} ref={setmap} >
                <UpdateView center={[userPosition.latitude, userPosition.longitude]} zoom={5} />
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                <Marker position={[userPosition.latitude, userPosition.longitude]}>
                    <Popup>Current position: {userPosition.latitude}, {userPosition.longitude}</Popup>
                </Marker>
                <Circle center={[userPosition.latitude, userPosition.longitude]} pathOptions={fillBlueOptions} radius={4600} />
                <Satellites satInfos={satInfos} />
            </MapContainer>
        </main>
    )
}

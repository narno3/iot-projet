
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import React from 'react';
import { Satellites } from './Satellites';

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


export default function MapComponent( {setmap, userPosition, satInfos, setSelected, trajPoints, setTrajPoints, selected} ) {
    const fillBlueOptions = { fillColor: 'blue' }

    return (
        <main class="map-area">
            {/* Leaflet Map */}
            <MapContainer center={[51.505, -0.09]} zoom={4} style={{ height: '100%', width: '100%'}} ref={setmap} >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                <Marker position={[userPosition.latitude, userPosition.longitude]}>
                    <Popup>Current position: {userPosition.latitude}, {userPosition.longitude}</Popup>
                </Marker>
                <Circle center={[userPosition.latitude, userPosition.longitude]} pathOptions={fillBlueOptions} radius={4600} />
                <Satellites satInfos={satInfos} setSelected={setSelected} trajPoints={trajPoints} setTrajPoints={setTrajPoints} selected={selected}/>
            </MapContainer>
        </main>
    )
}

import React, { useEffect, useState } from 'react';
import 'leaflet/dist/leaflet.css';
import './App.css';

import Header from './components/Header';
import LeftSidebar from './components/LeftSidebar';
import RightSidebar from './components/RightSidebar';
import MapComponent from './components/MapComponent';

function App() {
  // State to manage the map's center and the visibility of input fields
  const [map, setMap] = useState(null);
  const [satInfos, setSatInfos] = useState([[0],[0]]); // sat infos
  const [selected, setSelected] = useState(0);
  const [trajPoints, setTrajPoints] = useState([[0, 0, 0]]);
  const [userPosition, setUserPos] = useState({
    longitude: 2.35,
    latitude: 48.85
  }); // Default center

  function getSatInfos(){
    fetch("http://127.0.0.1:8000/sat_infos")
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        setSatInfos(data);
    });
  }
  useEffect(() => { getSatInfos() }, []);

  return (
    <body className="App">
      <Header />
      <div class="container">
        <LeftSidebar satInfos={satInfos} selected={selected} />
        <MapComponent 
          setmap = {setMap}
          userPosition={userPosition}
          satInfos = {satInfos}
          setSelected={setSelected} selected={selected}
          trajPoints={trajPoints} setTrajPoints={setTrajPoints}
        />
        <RightSidebar map = {map} pos={userPosition} setPos= {setUserPos} setTrajPoints={setTrajPoints} setSelected={setSelected}/>
      </div>
    </body>
  );
}

export default App;

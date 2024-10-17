import React, { useState, useRef, useEffect } from 'react';
import { Marker, Popup } from "react-leaflet";
import L from 'leaflet';
import { Trajectory } from './Trajectory';

var saticon = L.icon({
    iconUrl: 'sat-icon.png',
    iconSize: [30, 30]
})

export const Satellite = ( {position, onClick, idx, info, selected} ) => {
    const markerRef = useRef(null);
    useEffect(() => {
        // open popup when satellite is selected
        if (markerRef.current) {
            const marker = markerRef.current;
            if (selected === idx) {
                marker.openPopup();
            } else {
                marker.closePopup();
            }
        }
    }, [selected]);
    const marker = <Marker position={position} icon={saticon} ref={markerRef} eventHandlers={{click: () => onClick(idx)}} >
        {info && <Popup offset={[0, -10]} keepInView={false} autoPan={false}>{info[0]}</Popup>}
    </Marker>;
    return marker;
}

export const Satellites = ( {satInfos, setSelected, trajPoints, setTrajPoints, selected} ) => {
    const [satPositions, setPositions] = useState([[0, 0]]);
    const ws = useRef(null);

    // function that updates "trajPoints" with the trajectory for 'sat'
    function updateSatTraj(sat){
        setSelected(sat);
        fetch("http://127.0.0.1:8000/get_trajectory?sat=" + sat)
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            setTrajPoints(data['points']);
        });
    }

    // read sat positions from websocket endpoint
    function get_positions_ws() {
        ws.current = new WebSocket("ws://localhost:8000/positions");
        ws.current.onopen = () => console.log("ws opened");
        ws.current.onclose = () => console.log("ws closed");
        ws.current.onmessage = (event) => {
            const json = JSON.parse(event.data);
            if (event.data){
                setPositions(json);
            }
        };
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }
    useEffect(() => { get_positions_ws() }, []);

    const sats = satPositions.map((pos, index) => <Satellite position={pos} key={index} info={satInfos[index+1]} onClick={updateSatTraj} idx={index} selected={selected} />);
    return (
        <>
            <Trajectory points={trajPoints}/>
            {sats}
        </>
    )
}
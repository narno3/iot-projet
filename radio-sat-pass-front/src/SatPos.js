import React, { useState, useRef, useEffect } from 'react';
import { Marker } from 'react-leaflet';
import L from 'leaflet';

var saticon = L.icon({
    iconUrl: 'sat-icon.png',
    iconSize: [30, 30]
})

export const SatPos = () => {
    const [positions, setPositions] = useState([[0, 0]]);

    // Event listener for incoming messages
    
    const ws = useRef(null);
    useEffect(() => {
        ws.current = new WebSocket("ws://localhost:8000/ws");
        ws.current.onopen = () => console.log("ws opened");
        ws.current.onclose = () => console.log("ws closed");
        ws.current.onmessage = (event) => {
            console.log("hi" + JSON.stringify(event.data));
            const json = JSON.parse(event.data);
            if (event.data){
                setPositions(json);
                console.log("la data" + JSON.stringify(json.data));
            }
        };
        
        const wsCurrent = ws.current;
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);
        
    const markers = positions.map(position => <Marker position={position} icon={saticon} />)
    return (
        <> {markers} </>
    )
}

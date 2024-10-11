import { Polyline, CircleMarker } from 'react-leaflet';
import { useState, useEffect } from 'react';
const limeOptions = { color: 'lime' }

export function Trajectory() {
    const [myPoints, setPoints] = useState([]);
    // fetch our back-end data
    function getSatTraj(){
        fetch("http://127.0.0.1:8000/get_trajectory")
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            // console.log(data);
            setPoints(data['points']);
        });
    }
    useEffect(() => { getSatTraj(); }, []);

    // here, we are decomposing the trajectory into continuous lines, (if we don't do this, there might lines across the map from lat 0 to 180)
    function makePolylines(){
        const lines = [];
        let prevPoint = myPoints[0];
        let line = [];
        for (let i = 0; i < myPoints.length; i++) {
            if (Math.abs(prevPoint[2] - myPoints[i][2]) > 100) {
                lines.push(line);
                line = [];
            }
            line.push([myPoints[i][1], myPoints[i][2]]);
            prevPoint = myPoints[i];
        }
        lines.push(line);
        return lines.map( line => <Polyline pathOptions={limeOptions} positions={line}/>)
    }
    // equivalent of the whole thing with just points (circles)
    function makeCircles(){
        return myPoints.map(
            point => <CircleMarker center = {[point[1], point[2]]} radius = {2} />
        )
    }
    return <>{makePolylines()}</>
    //return <>{circleMarkers}</>

}
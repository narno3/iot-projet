import { Polyline, CircleMarker } from 'react-leaflet';
const trajColor = { color: 'red' }

export function Trajectory( {points} ) {
    // here, we are decomposing the trajectory into continuous lines, (if we don't do this, there might lines across the map from lat 0 to 180)
    function makePolylines(){
        const lines = [];
        let prevPoint = points[0];
        let line = [];
        for (let i = 0; i < points.length; i++) {
            if (Math.abs(prevPoint[2] - points[i][2]) > 100) {
                lines.push(line);
                line = [];
            }
            line.push([points[i][1], points[i][2]]);
            prevPoint = points[i];
        }
        lines.push(line);
        return lines.map( line => <Polyline pathOptions={trajColor} positions={line}/>)
    }
    // equivalent of the whole thing with just points (circles)
    function makeCircles(){
        return points.map(
            point => <CircleMarker center = {[point[1], point[2]]} color='red' radius = {2} />
        )
    }
    return <>
        {makePolylines()}
        {/* {makeCircles()} */}
    </>

}
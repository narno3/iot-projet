import React from 'react';

export default function RightSidebar( {map, pos, setPos} ) {
    const handleLocate = () => {
        if (!map){
            return;
        }
        map.locate({ setView: true, maxZoom: 12 });

        const onLocationFound = (e) => {
            setPos({ longitude: e.latlng.lng, latitude: e.latlng.lat });
        };
        map.on('locationfound', onLocationFound);
        map.once('locationfound', () => {
            map.off('locationfound', onLocationFound);
        });
    };
    const handleLatChange = (e) => {
        if(isNaN(parseFloat(e.target.value))){
            return;
        }
        setPos({latitude: e.target.value, longitude: pos.longitude});
        map.setView([e.target.value, pos.longitude], map.getZoom());
    };
    const handleLongChange = (e) => {
        if(isNaN(parseFloat(e.target.value))){
            return;
        }
        setPos({longitude: e.target.value, latitude: pos.latitude});
        map.setView([pos.latitude, e.target.value], map.getZoom());
    };

    return (
        <aside class="right-sidebar">
            <div class="location card">
                <h2>My location</h2>
                <div class="coords">
                    <input type="text" placeholder={"Long: " + pos.latitude } onChange={handleLatChange} />
                    <input type="text" placeholder={"Lat: " + pos.longitude } onChange={handleLongChange}/>
                </div>
                <button onClick={() => {handleLocate(setPos)}}>Locate Me!</button>
            </div>
            <div class="next-passes card">
                <h2>Next Passes</h2>
                <ul>
                    <li>pass</li>
                    <li>pass</li>
                    <li>pass</li>
                    <li>pass</li>
                    <li>pass</li>
                </ul>
            </div>
        </aside>
    )
}

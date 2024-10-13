import React from 'react';

function SatData ( {fieldName, fieldValue} ) {
    return <div class="sat-data-line"><b>{fieldName}:</b> <p>{fieldValue}</p></div>
}

export default function LeftSidebar( {satInfos, selected} ) {
    const infos = satInfos[selected+1].map((field, index) => <SatData fieldName={satInfos[0][index]} fieldValue={satInfos[selected+1][index]}/>)
    return (
        <aside class="left-sidebar">
        <div class="satellites card">
            <h2>Satellites</h2>
            {/* <input type="text" placeholder="Search satellites"> */}
            {/* <ul class="satellites-list">
                <li>sat</li>
                <li>sat</li>
                <li>sat</li>
                <li>sat</li>
                <li>sat</li>
                </ul> */}
        </div>
        <div class="satellite-info card">
            <h2>Satellite Info</h2>
            <div class="sat-infos">{infos}</div>
        </div>
    </aside>
    )
}

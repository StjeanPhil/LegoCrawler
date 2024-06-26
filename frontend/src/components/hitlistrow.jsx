import { useState } from 'react'
import { useEffect } from 'react'

import React from 'react';
function Hitlistrow({item,index,showSelected}){
    useEffect(() => {
    console.log("Item updated:", item);
    }, [item]);

    return<>
        <tr key={index} style={listItemStyle} >
            <td style={tdStyle}>{item["name"]}</td>   
            <td style={tdStyle}>{ item["price"]}</td>
            <td style={tdStyle}>{ item["store"]}</td>
            <td style={tdStyle}><a href={item["href"]}>Link</a></td>
        </tr>
        
    </>
}

// Inline styles for list items
const listItemStyle = {
    
    padding: '10px', // Add padding for better spacing
    
    width: '90%',
};
const tdStyle = {
    borderBottom: '1px solid #ccc', // Add border between list items
}
export default Hitlistrow
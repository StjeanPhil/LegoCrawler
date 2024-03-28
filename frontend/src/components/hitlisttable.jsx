
import { useState } from 'react'
import { useEffect } from 'react'

import React from 'react';
import Hitlistrow from './hitlistrow';

function Hitlisttable( {items,getHitList} ) {

    
            
  return (
    <div style={tableContainer}>
        <div style={headerstyle}>
            <h2>Hitlist</h2>
            <button onClick={()=>getHitList()}>
                Get Hitlist
            </button>

        </div>



        <table style={tableStyle}>
          <thead>
              <tr>
                <th>Name</th>
                <th>Price</th>
                <th>Store</th>
                <th>Link</th>
              </tr>
          </thead>
          <tbody>
              {items.map((item, index) => (
                  <Hitlistrow key={index} item={item} />
              ))}
          </tbody>

        </table>
    </div>
  );
}
const headerstyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px',
    borderBottom: '1px solid #ccc',
  };
// Inline styles for the scrollable list container
const tableContainer = {
  overflowY: 'auto', // Enable vertical scrolling
  maxHeight: '500px', // Set maximum height to make it scrollable

};

// Inline styles for the list
const tableStyle = {
  listStyleType: 'none', // Remove default list styles
  padding: 0, // Remove default padding
  width: '100%',

};
export default Hitlisttable;
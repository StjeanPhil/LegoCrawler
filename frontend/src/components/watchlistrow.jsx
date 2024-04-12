import { useState } from "react";
import { useEffect } from "react";

import React from "react";
function Watchlistrow({ item, index, showSelected }) {
  useEffect(() => {
    console.log("Item updated:", item);
  }, [item]);
  //item=[idx,set_num,price]
  return (
    <>
      <tr
        key={index}
        style={listItemStyle}
        onClick={() => showSelected(item, index)}
      >
        <td style={tdStyle}>{item[1]}</td>
        <td style={tdStyle}>{item[2]}</td>
      </tr>
    </>
  );
}

// Inline styles for list items
const listItemStyle = {
  padding: "10px", // Add padding for better spacing

  width: "90%",
};
const tdStyle = {
  borderBottom: "1px solid #ccc", // Add border between list items
};
export default Watchlistrow;

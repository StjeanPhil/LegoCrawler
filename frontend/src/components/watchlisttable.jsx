import { useState } from "react";
import { useEffect } from "react";

import React from "react";
import Watchlistrow from "./watchlistrow";

function Watchlisttable({ items, getWatchList, handleWatchlist }) {
  useEffect(() => {
    console.log("Items updated:", items);
  }, [items]);

  const showSelected = (item, index) => {
    document.getElementById("nameInput").value = item[1];
    document.getElementById("priceInput").value = item[2];
  };
  const saveNewItem = () => {
    console.log("saveNewItem");
    var name = document.getElementById("nameInput").value;
    var price = document.getElementById("priceInput").value;
    //if(name.match('\b\d{5}\b') > 0 && price.length > 0){
    handleWatchlist(name, price, "save");
  };
  const deleteItem = () => {
    console.log("deleteItem");
    var name = document.getElementById("nameInput").value;
    var price = document.getElementById("priceInput").value;

    handleWatchlist(name, price, "delete");
  };

  return (
    <div style={tableContainer}>
      <div style={headerstyle}>
        <h2>Watchlist</h2>
        <button onClick={() => getWatchList()}>Get Watchlist</button>
      </div>

      <input id="nameInput" type="text" placeholder="Item Name" />
      <input id="priceInput" type="text" placeholder="Item Price" />
      <button onClick={saveNewItem}>Add</button>
      <button onClick={deleteItem}>Delete</button>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, index) => (
            <Watchlistrow key={index} item={item} showSelected={showSelected} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
const headerstyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "10px",
  borderBottom: "1px solid #ccc",
};
// Inline styles for the scrollable list container
const tableContainer = {
  overflowY: "auto", // Enable vertical scrolling
  maxHeight: "500px", // Set maximum height to make it scrollable
};

// Inline styles for the list
const tableStyle = {
  listStyleType: "none", // Remove default list styles
  padding: 0, // Remove default padding
  width: "100%",
};

export default Watchlisttable;

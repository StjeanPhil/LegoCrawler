import { useEffect, useState } from "react";

import "./App.css";
import brickboy from "./assets/brickboy.svg";
import Watchlisttable from "./components/watchlisttable";
import Hitlisttable from "./components/hitlisttable";

function App() {
  const [count, setCount] = useState(0);
  const [watchlist, setWatchlist] = useState([]);
  const [hitlist, setHitlist] = useState([]);

  var watchlistLoaded = false;
  useEffect(() => {
    console.log("Watchlist updated:", watchlist);
    watchlistLoaded = true;
  }, [watchlist]);

  const sendHello = () => {
    console.log("trying to send request to /test");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/test", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      console.log(xhr);
      if (xhr.readyState == 4 && xhr.status === 200) {
        // Handle response if needed
        console.log("Script executed successfully:", xhr.responseText);
      }
    };
    xhr.send(JSON.stringify({}));
    setCount(count + 1);
  };
  const getHitList = () => {
    console.log("Retrieving hitlist");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/gethitlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status === 200) {
        console.log("Script executed successfully:", xhr.responseText);
        const hitlistData = JSON.parse(xhr.responseText);
        setHitlist(hitlistData);
      }
    };
    xhr.send(JSON.stringify({}));
  };

  const getWatchList = () => {
    console.log("Retrieving watchlist");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/getwatchlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status === 200) {
        //console.log('Script executed successfully:', xhr.responseText);
        const watchlistData = JSON.parse(xhr.responseText);
        setWatchlist(watchlistData);
      }
    };
    xhr.send(JSON.stringify({}));
  };

  const updateItemWatchlist = (set_num, price) => {
    console.log("Updating item in watchlist");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/updatewatchlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status === 200) {
        console.log("Script executed successfully:", xhr.responseText);
      }
    };
    xhr.send(JSON.stringify({ set_num: set_num, price: price }));
  };
  const insertItemWatchlist = (set_num, price) => {
    console.log("Inserting item in watchlist");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/insertwatchlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status === 200) {
        console.log("Script executed successfully:", xhr.responseText);
      }
    };
    xhr.send(JSON.stringify({ set_num: set_num, price: price }));
  };
  const deleteItemWatchlist = (set_num) => {
    console.log("Deleting item in watchlist");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/deletewatchlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status === 200) {
        console.log("Script executed successfully:", xhr.responseText);
      }
    };
    xhr.send(JSON.stringify({ set_num: set_num }));
  };
  const handleWatchlist = (set_num, price, action) => {
    //watchlistItem=[idx,set_num,price]
    if (!watchlistLoaded) {
      return;
    }
    console.log("Handling watchlist action");
    console.log(set_num);
    var actionCompleted = false;
    for (var i = 0; i < watchlist.length; ++i) {
      if (watchlist[i][1] == set_num) {
        if (action == "delete") {
          console.log("Action: Delete item");
          setWatchlist((prevWatchlist) => {
            var newWatchlist = [...prevWatchlist];
            for (i = 0; i < newWatchlist.length; i++) {
              if (newWatchlist[i][1] == set_num) {
                newWatchlist.splice(i, 1);
              }
            }
            return newWatchlist;
          });
          console.log("Deleting from DB");
          deleteItemWatchlist(set_num);
          actionCompleted = true;
          console.log("Deleted item");
          break;
        } else if (action == "save") {
          actionCompleted = true;

          setWatchlist((prevWatchlist) => {
            var newWatchlist = [...prevWatchlist];
            for (i = 0; i < newWatchlist.length; i++) {
              if (newWatchlist[i][1] == set_num) {
                newWatchlist[i][2] = price;
              }
            }
            return newWatchlist;
          });
          updateItemWatchlist(set_num, price);
          console.log(watchlist);
          break;
        }
      }
    }
    if (!actionCompleted && action == "save") {
      setWatchlist((prevWatchlist) => {
        const newWatchlist = [...prevWatchlist];
        newWatchlist.push([newWatchlist.length, set_num, price]);
        return newWatchlist;
      });
      insertItemWatchlist(set_num, price);
      console.log("Added item");
    }
    //getWatchList();
    return;
  };
  const unleashTheBots = () => {
    console.log("Unleashing the bots");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/crawl", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      console.log(xhr);
      if (xhr.readyState == 4 && xhr.status === 200) {
        // Handle response if needed
        console.log("Script executed successfully:", xhr.responseText);
        const newHitlist = JSON.parse(xhr.responseText);
        setHitlist(newHitlist);
      } else {
        console.log(xhr.responseText);
      }
    };
    xhr.send(JSON.stringify({}));
  };

  return (
    <>
      <div id="title">
        <h1>LegoCrawler</h1>
        <div style={menu}>
          <img src={brickboy} className="logo" alt="Brick Boyyy" />
          <button style={redbtn} onClick={() => unleashTheBots()}>
            Crawl
          </button>
        </div>
      </div>

      <Watchlisttable
        items={watchlist}
        getWatchList={getWatchList}
        handleWatchlist={handleWatchlist}
      />
      <Hitlisttable items={hitlist} getHitList={getHitList} />
    </>
  );
}
const menu = {
  display: "flex",
  "justify-content": "center",
  "align-items": "center",
};
const redbtn = {
  "background-color": "red",
  color: "white",
  padding: "10px 40px",
  "font-size": "30px",
  border: "none",
  "border-radius": "8px",
  "max-height": "60px",
};

export default App;

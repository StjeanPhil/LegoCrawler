import { useEffect, useState } from 'react'

import './App.css'
import brickboy from './assets/brickboy.svg'
import Watchlisttable from './components/watchlisttable'
import Hitlisttable from './components/hitlisttable'

function App() {
  const [count, setCount] = useState(0)
  const [watchlist, setWatchlist] = useState([])
  const [hitlist, setHitlist] = useState([])
  var watchlistLoaded = false
    useEffect(() => {
    console.log("Watchlist updated:", watchlist);
    watchlistLoaded = true;
  }, [watchlist]);

  const sendHello = () => {
    console.log("trying to send request to /test")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/test", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      console.log(xhr)
        if (xhr.readyState==4  && xhr.status === 200) {
            // Handle response if needed
            console.log('Script executed successfully:', xhr.responseText);
        }
    };
    xhr.send(JSON.stringify({}));
    setCount(count + 1)
  }
  const getHitList = () => {
    console.log("Retrieving hitlist")
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/gethitlist", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState==4  && xhr.status === 200) {
        console.log('Script executed successfully:', xhr.responseText);
        const hitlistData = JSON.parse(xhr.responseText);
        setHitlist(hitlistData)
      }
    };
    xhr.send(JSON.stringify({}));
  }




  const getWatchList = () => {
    
    console.log("Retrieving watchlist")
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/getwatchlist", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState==4  && xhr.status === 200) {
        console.log('Script executed successfully:', xhr.responseText);
        
        const watchlistData = JSON.parse(xhr.responseText);
        setWatchlist(watchlistData)
        
      }
    };
    xhr.send(JSON.stringify({}));
  }
  const postWatchList = () => {
    console.log("Posting watchlist")
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/postwatchlist", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState==4  && xhr.status === 200) {
        console.log('Script executed successfully:', xhr.responseText);
      }
    };
    xhr.send(JSON.stringify(watchlist));
  }

  const handleWatchlist = (name, price,action) => {
    
    if (!watchlistLoaded){ return}
    console.log("Handling watchlist action")
    
    var actionCompleted=false;
    for (var i = 0; i < watchlist.length; ++i) {
      console.log("I is at :"+i)
      if (watchlist[i]["name"] == name) {
        
        if (action == "delete") {
          setWatchlist(prevWatchlist => {
            var newWatchlist = prevWatchlist;
            newWatchlist=newWatchlist.filter((item) => item.name !== name)
            console.log(newWatchlist)
            return newWatchlist;
          });
          actionCompleted=true;
          console.log("Deleted item")
          break;
        }else if (action == "save" ) {
          actionCompleted=true;
        
          setWatchlist(prevWatchlist => {
            var newWatchlist = prevWatchlist;
            newWatchlist=newWatchlist.filter((item) => item.name !== name)
            newWatchlist.push( {"name":name,"price":price});

            return newWatchlist;
          });
          break;


          
          console.log("Saved item")
        }
      }
    }
    if (!actionCompleted && action == "save") {
        setWatchlist(prevWatchlist => {
          const newWatchlist = [...prevWatchlist];
          newWatchlist.push( {"name":name,"price":price});
          return newWatchlist;
        });

      console.log("Added item")
    }
    return
  }

  return (
    <>
      <div id='title'>
        <h1>LegoCrawler</h1>
        <div style={menu}>
          <img src={brickboy}  className="logo" alt="Brick Boyyy" />
          <button style={redbtn} onClick={sendHello}>Crawl</button>
        </div>
        
        
      </div>
      
      <Watchlisttable items={watchlist}  getWatchList={getWatchList} postWatchList={postWatchList} handleWatchlist={handleWatchlist} />
      <Hitlisttable items={hitlist} getHitList={getHitList}/>
      
    </>
  )
}
const menu = {
  "display":"flex",
  "justify-content":"center",
  "align-items": 'center'
}
const redbtn = {
    "background-color": 'red',
    "color": 'white',
    "padding": '10px 40px',
    "font-size": '30px',
    "border": 'none',
    "border-radius": '8px',
    "max-height": '60px',
    
}


export default App

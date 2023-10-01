import React from 'react';
import TopSignal from './TopSignal';
import LeftSignal from './LeftSignal';
import BottomSignal from './BottomSignal';
import RightSignal from './RightSignal';

const TrafficSignalSystem = () => {
  function fetchDataAndUpdateLocalStorage() {
    fetch('http://127.0.0.1:8000/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(response => {
      // Handle the response here
      return response.json()
    }).then((e) => {
      localStorage.setItem('max_count', e[0]);
    })
    .catch(error => {
      // Handle any errors here
      console.log(error);
    });
  }
  
  // Call the function immediately to fetch and set the initial value
  fetchDataAndUpdateLocalStorage();
  
  // Set up an interval to fetch and update the value every 40 seconds
  const fetchInterval = setInterval(fetchDataAndUpdateLocalStorage, 4000);
  return (
    <div className="traffic-signal-system">
      <div className="top-signal">
        <TopSignal fetchInterval={fetchInterval} />
      </div>
      <div className="left-signal">
        <LeftSignal fetchInterval={fetchInterval} />
      </div>
      <div className="bottom-signal">
        <BottomSignal fetchInterval={fetchInterval} />
      </div>
      <div className="right-signal">
        <RightSignal fetchInterval={fetchInterval} />
      </div>
    </div>
  );
};

export default TrafficSignalSystem;

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle, faArrowUp } from '@fortawesome/free-solid-svg-icons';

const BottomSignal = ({ fetchInterval }) => {
  const [leftColor, setLeftColor] = useState('white');
  const [rightColor, setRightColor] = useState('white');
  const [showLeftArrow, setShowLeftArrow] = useState(false);
  const [showRightArrow, setShowRightArrow] = useState(false);
  const [leftBlinking, setLeftBlinking] = useState(false);
  const [rightBlinking, setRightBlinking] = useState(false);
  const [showArrow, setShowArrow] = useState(false);
  const max_count_up = localStorage.getItem('max_count');
  // const changeColor = (newColor) => {
  //   if (newColor === 'red') {
  //     setLeftColor('red');
  //     setRightColor('white');
  //     setShowLeftArrow(false);
  //     setShowRightArrow(false);
  //     setLeftBlinking(false);
  //     setRightBlinking(false);
  //   } else if (newColor === 'green') {
  //     setLeftColor('green');
  //     setRightColor('green');
  //     setShowLeftArrow(true); // Set to true for green signal
  //     setShowRightArrow(true); // Set to true for green signal
  //   }
  // };

  useEffect(() => {
    console.log("changeing?")
    const max_count_up = localStorage.getItem('max_count');
    console.log('max_count_up:', max_count_up); // Add this line
    // Set initial colors and arrow visibility based on max_count_up
    if (max_count_up === 'A') {
      setLeftColor('green');
      setRightColor('green');
      setShowArrow(true);
    } else {
      setLeftColor('red');
      setRightColor('white');
      setShowArrow(false);
    }
  }, [max_count_up])
  useEffect(() => {
    let leftInterval, rightInterval;

    if (leftBlinking) {
      leftInterval = setInterval(() => {
        setLeftColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setShowLeftArrow((prev) => !prev);
      }, 500);
    }

    if (rightBlinking) {
      rightInterval = setInterval(() => {
        setRightColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setShowRightArrow((prev) => !prev);
      }, 500);
    }

    return () => {
      clearInterval(leftInterval);
      clearInterval(rightInterval);
      clearInterval(fetchInterval);
    };
  }, [leftBlinking, rightBlinking, fetchInterval]);

  const circleStyle = {
    width: '50px',
    height: '50px',
    borderRadius: '50%',
    border: '2px solid black',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    
  };

  return (
    <div className="signal">
      <div className="signal-illustration">
        <div className="circle-container">
          <div className="circle" style={{ ...circleStyle, backgroundColor: leftColor }}>
            {showLeftArrow &&leftBlinking && (
              <>
                <FontAwesomeIcon icon={faArrowUp} size="2x" style={{ color: 'black', position: 'absolute', top: '27%', left: '48%', transform: 'rotate(180deg)', zIndex:'10' }} />
              </>
              
            )}
          </div>
          <div className="circle" style={{ ...circleStyle, backgroundColor: rightColor }}>
            {showRightArrow && rightBlinking && (
              <>
                <FontAwesomeIcon icon={faArrowUp} size="2x" style={{ color: 'black', position: 'absolute', top: '47%', left: '48%', transform: 'rotate(90deg)',zIndex:'10'}} />
              </>
            )}
          </div>
        </div>
      </div>
      <div className="button-container">
        <button onClick={() => changeColor('red')}>Red</button>
        <button onClick={() => changeColor('green')}>Green</button>
        <button onClick={() => setLeftBlinking(!leftBlinking)}>1</button>
        <button onClick={() => setRightBlinking(!rightBlinking)}>2</button>
      </div>
    </div>
  );
};

export default BottomSignal;

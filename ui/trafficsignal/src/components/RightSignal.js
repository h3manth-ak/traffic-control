import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle, faArrowUp } from '@fortawesome/free-solid-svg-icons';

const BottomSignal = (fetchInterval) => {
  const max_count_right=localStorage.getItem('max_count')
  // console.log(max_count_right);
  const [leftColor, setLeftColor] = useState('white');
  const [rightColor, setRightColor] = useState('white');
  const [showArrow, setShowArrow] = useState(false);
  const [blinking, setBlinking] = useState(false);

  // const changeColor = (newColor) => {
  //   if (newColor === 'red') {
  //     setLeftColor('red');
  //     setRightColor('white');
  //     setShowArrow(false);
  //   } else if (newColor === 'green') {
  //     setLeftColor('green');
  //     setRightColor('green');
  //     setShowArrow(true);
  //   }
  // };

  useEffect(() => {
    const max_count_right = localStorage.getItem('max_count');
    console.log('max_count_right:', max_count_right); // Add this line
    // Set initial colors and arrow visibility based on max_count_right
    if (max_count_right === 'D') {
      setLeftColor('green');
      setRightColor('green');
      setShowArrow(true);
    } else {
      setLeftColor('red');
      setRightColor('white');
      setShowArrow(false);
    }
  }, [max_count_right])

  useEffect(() => {
    let interval;

    if (blinking) {
      interval = setInterval(() => {
        setLeftColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setRightColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setShowArrow((prevShowArrow) => !prevShowArrow); // Toggle arrow visibility
      }, 500);
    } else {
      clearInterval(interval);
    }

    return () => {
      clearInterval(interval);
      clearInterval(fetchInterval);
    };
  }, [blinking, fetchInterval]);

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
            {showArrow && (
              <>
                <FontAwesomeIcon icon={faArrowUp} size="2x" style={{ color: 'black', position: 'absolute', top: '27%', left: '48%', transform: 'rotate(180deg)' }} />
              </>
            )}
          </div>
          <div className="circle" style={{ ...circleStyle, backgroundColor: rightColor }}>
            {showArrow && (
              <>
                <FontAwesomeIcon icon={faArrowUp} size="2x" style={{ color: 'black', position: 'absolute', top: '47%', left: '48%', transform: 'rotate(90deg)' }} />
              </>
            )}
          </div>
        </div>
      </div>
      <div className="button-container">
        <button onClick={() => changeColor('red')}>Red</button>
        <button onClick={() => changeColor('green')}>Green</button>
        <button onClick={() => setBlinking(!blinking)}>Blink Green</button>
      </div>
    </div>
  );
};

export default BottomSignal;

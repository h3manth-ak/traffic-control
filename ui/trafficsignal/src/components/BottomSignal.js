import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUp } from '@fortawesome/free-solid-svg-icons';

const BottomSignal = () => {
  const max_count_bottom = localStorage.getItem('max_count');
  const [leftColor, setLeftColor] = useState('white');
  const [rightColor, setRightColor] = useState('white');
  const [showArrow, setShowArrow] = useState(false);
  const [blinking, setBlinking] = useState(false);

  useEffect(() => {
    const max_count_bottom = localStorage.getItem('max_count');
    console.log('max_count_bottom:', max_count_bottom); // Add this line
    // Set initial colors and arrow visibility based on max_count_bottom
    if (max_count_bottom === 'C') {
      setLeftColor('green');
      setRightColor('green');
      setShowArrow(true);
    } else {
      setLeftColor('red');
      setRightColor('white');
      setShowArrow(false);
    }
  }, [max_count_bottom]);

  useEffect(() => {
    let interval;

    if (blinking) {
      interval = setInterval(() => {
        setLeftColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setRightColor((prevColor) => (prevColor === 'green' ? 'white' : 'green'));
        setShowArrow((prevShowArrow) => !prevShowArrow);
      }, 500);
    } else {
      clearInterval(interval);
    }

    return () => clearInterval(interval);
  }, [blinking]);

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
                <FontAwesomeIcon icon={faArrowUp} size="2x" style={{ color: 'black', position: 'absolute', top: '47%', left: '48%', transform: 'rotate(-90deg)' }} />
              </>
            )}
          </div>
        </div>
      </div>
      <div className="button-container">
        {/* You can remove the changeColor function and control color via state */}
        <button onClick={() => setLeftColor('red')}>Red</button>
        <button onClick={() => setLeftColor('green')}>Green</button>
        <button onClick={() => setBlinking(!blinking)}>Blink Green</button>
      </div>
    </div>
  );
};

export default BottomSignal;

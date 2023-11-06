import React, { useState, useEffect } from 'react';
import loading from './assets/loading.gif';

const EmbeddedGoogleCalendar = ({ calendarId = '' }) => {
  const calendarUrl = `https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23B39DDB&ctz=America%2/Sao_Paulo&mode=WEEK&hl=pt_BR&showCalendars=0&showPrint=0&src=${calendarId}&color=%23AD1457`;

  const [iframeLoaded, setIframeLoaded] = useState(false);

  useEffect(() => {
    const iframe = document.getElementById('google-calendar-iframe');
    iframe.addEventListener('load', handleIframeLoad);
  }, []);

  const handleIframeLoad = () => {
    setIframeLoaded(true);
  };

  return (
    <div style={{
      width: '95%',
      height: '480px',
      borderRadius: '15px',
      overflow: 'hidden',
      boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.75)',
      position: 'relative',
    }}>
      {iframeLoaded ? null : (
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'rgba(255, 255, 255, 0.8)',
            zIndex: 1,
          }}
        >
          <img src={loading} alt="Loading" />
        </div>
      )}
      <iframe
        id="google-calendar-iframe"
        src={calendarUrl}
        style={{
          border: 0,
          width: '100%',
          height: '100%',
          display: iframeLoaded ? 'block' : 'none',
        }}
        title="Google Calendar"
      />
    </div>
  );
};

export default EmbeddedGoogleCalendar;

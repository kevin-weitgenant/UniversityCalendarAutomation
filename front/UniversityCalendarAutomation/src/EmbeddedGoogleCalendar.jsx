import React, { useState, useEffect } from 'react';
import Loading from './Loading';

const EmbeddedGoogleCalendar = ({ calendarId = '' }) => {
  const calendarUrl = `https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23B39DDB&ctz=America/Sao_Paulo&mode=WEEK&hl=pt_BR&showCalendars=0&showPrint=0&src=${calendarId}&color=%23AD1457`;

  const [iframeLoaded, setIframeLoaded] = useState(false);

  useEffect(() => {
    const iframe = document.getElementById('google-calendar-iframe');
    iframe.addEventListener('load', handleIframeLoad);
  }, []);

  const handleIframeLoad = () => {
    setIframeLoaded(true);
  };

  const iframeStyle = {
    border: 0,
    width: '100%',
    minHeight: '480px',
    display: iframeLoaded ? 'block' : 'none',
  };

  return (
    <div style={{ width: '100%', height: '100%', minHeight: '480px', margin: '30px', borderRadius: '20px', overflow: 'hidden', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.5)' }}>
      {!iframeLoaded && <Loading/>} {/* Exibe o componente Loading enquanto o iframe não estiver carregado */}
      <iframe
        id="google-calendar-iframe"
        src={calendarUrl}
        style={iframeStyle}
        title="Google Calendar"
      />
    </div>
  );
};

export default EmbeddedGoogleCalendar;

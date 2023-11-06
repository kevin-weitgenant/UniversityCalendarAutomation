const EmbeddedGoogleCalendar = ({ calendarId = ''}) => {
  const calendarUrl = `https://calendar.google.com/calendar/embed?height=600&wkst=2&bgcolor=%23B39DDB&ctz=America%2FSao_Paulo&mode=WEEK&hl=pt_BR&showCalendars=0&showPrint=0&src=${calendarId}&color=%23AD1457`

  const iframeStyle = {
    border: 0,
    width: '100%',
    height: '100%',
  };

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <iframe
        src={calendarUrl}
        style={iframeStyle}
        title="Google Calendar"
      />
    </div>
  );
};



export default EmbeddedGoogleCalendar;

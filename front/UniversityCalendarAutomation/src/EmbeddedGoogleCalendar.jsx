import PropTypes from 'prop-types';

const EmbeddedGoogleCalendar = ({ calendarId }) => {
  const calendarUrl = `https://calendar.google.com/calendar/embed?src=${calendarId}`;

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

EmbeddedGoogleCalendar.propTypes = {
  calendarId: PropTypes.string.isRequired,
};

export default EmbeddedGoogleCalendar;

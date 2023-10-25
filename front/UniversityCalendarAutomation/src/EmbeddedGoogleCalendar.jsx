import React from 'react';
import PropTypes from 'prop-types';

const EmbeddedGoogleCalendar = ({ calendarId}) => {
  const calendarUrl = `https://calendar.google.com/calendar/embed?src=${calendarId}`;

  return (
    <iframe
      src={calendarUrl}
      style={{ border: 0 }}
      width="800"
      height="600"
      frameBorder="0"
      scrolling="no"
    />
  );
};

EmbeddedGoogleCalendar.propTypes = {
  calendarId: PropTypes.string.isRequired,
};

export default EmbeddedGoogleCalendar;
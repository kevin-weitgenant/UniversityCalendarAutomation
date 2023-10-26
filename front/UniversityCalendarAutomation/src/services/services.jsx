import axios from 'axios';
import FileDownload from 'js-file-download';

let apiUrl

if (process.env.NODE_ENV === 'production') {
  apiUrl = process.env.REACT_APP_PROD_API_URL;
} else {
  // Use the localhost URL for local development
  apiUrl = 'http://localhost:5000';
}

export const getIcal = async () => {
  try {
    const response = await axios.get(`${apiUrl}/getIcal`);
    return response.data;
  } catch (error) {
    console.error('Error fetching iCal:', error);
    throw error;
  }
};

export const handleDownload = async (scheduleText) => {
  try {
    const response = await axios.get(`${apiUrl}/api/download_ical`, {
      params: { scheduleText },
      responseType: 'blob',  // Important: indicate that we are expecting a stream
    });
    FileDownload(response.data, 'calendar.ics');
  } catch (error) {
    console.error('An error occurred while downloading the file.', error);
  }
};


export const getEmbeddedCalendarID = async (email = 'kcweitgenant@inf.ufpel.edu.br') => {
    try {
      const response = await axios.get(`${apiUrl}/getEmbeddedCalendarID`, { params: { email,scheduleText} });
      
      return response.data.calendarID;
    } catch (error) {
      console.error('Error fetching Embedded Calendar ID:', error);
      throw error;
    }
  };
  
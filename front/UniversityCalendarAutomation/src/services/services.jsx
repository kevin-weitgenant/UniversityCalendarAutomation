import axios from 'axios';
import FileDownload from 'js-file-download';

let apiUrl

if (process.env.NODE_ENV === 'production') {
  apiUrl = process.env.REACT_APP_PROD_API_URL || 'http://localhost:5000';
} else {
  // Use the localhost URL for local development
  apiUrl = 'http://localhost:5000';
}

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


export const getEmbeddedCalendarID = async (email = 'kcweitgenant@inf.ufpel.edu.br',scheduleText) => {
    try {
      const response = await axios.get(`${apiUrl}/api/getEmbeddedCalendarID`, { params: { email,scheduleText} });
      
      return response.data.calendarID;
    } catch (error) {
      console.error('Error fetching Embedded Calendar ID:', error);
      throw error;
    }
  };

  export const getCount = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/get_count`);
      console.log("The count is: ", response.data.count);
      return response.data.count;
    } catch (error) {
      console.error('An error occurred while getting the count.', error);
      return null;
    }
  };
  
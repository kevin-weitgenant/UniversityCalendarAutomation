import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from './App.jsx'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CalendarRoute from './CalendarRoute.jsx';



const router = createBrowserRouter([
  {
    path : "/",
    element: <App/>,
  },
  
  {
    path: '/calendar',
    element: <CalendarRoute/>
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router = {router}/>
    <ToastContainer />
  </React.StrictMode>,
)

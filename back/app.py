from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from parseCalendarText import parse_schedule_text
from generateIcal import createCalendar, writeCalendar
from googleCalendar.generateGoogleCalendar import generate_Google_Calendar

import os
from database.counter import Base, engine, increment_count

app = FastAPI()

# Add cors middleware
origins = [
    "http://localhost:5173",  # React app
    "http://localhost:5000",  # FastAPI server
    "http://your-react-app-url.com",  # Substitute this with your React app's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build files
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "dist"), html=True), name="calendarFront")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from parseCalendarText import parse_schedule_text
from generateIcal import createCalendar, writeCalendar
from googleCalendar.generateGoogleCalendar import generate_Google_Calendar

import os
from database.counter import Base, engine, increment_count, get_count

app = FastAPI()

# Add cors middleware
origins = [
    "http://localhost:5173",  # React app
    "http://localhost:5000",  # FastAPI server
    "http://your-react-app-url.com",  # Substitute this with your React app's URL
    "http://127.0.0.1:5000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)



@app.get("/api/download_ical")
def download_ical(scheduleText: str):
    scheduleDict = parse_schedule_text(scheduleText)
    
    filepath = writeCalendar(createCalendar(scheduleDict))
    increment_count()
    return FileResponse(filepath, media_type='text/calendar', filename=os.path.basename(filepath))

@app.get("/api/getEmbeddedCalendarID")
async def get_embedded_calendar_id(email: str, scheduleText: str):     

    if not email or not scheduleText:
        raise HTTPException(status_code=400, detail="Email and scheduleText must be provided")
    
    try:
        scheduleDict = parse_schedule_text(scheduleText)
        calendarID = generate_Google_Calendar(scheduleDict, email)

        print(f'scheduleText = {scheduleText}')
        print(f'calendarID ={calendarID}')
        
        if not calendarID:
            raise HTTPException(status_code=500, detail="Calendar generation failed.")
        
        increment_count()
        return JSONResponse(content={"calendarID": calendarID})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during calendar generation: {str(e)}")
    
# Serve React build files


@app.get("/api/get_count")
def get_counter():
    count = get_count()
    if count is not None:
        return {"count": count}
    else:
        return {"error": "An error occurred while fetching the count."}
    
app.mount("/", StaticFiles(directory="dist", html=True), name="calendarFront")   
    
    
    
    



# poetry run uvicorn app:app --port 5000 --reload
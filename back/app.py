from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from parseCalendarText import parse_schedule_text
from googleCalendar.generateGoogleCalendar import generate_Google_Calendar
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

# # Serve React build files
# app.mount("/", StaticFiles(directory="react-app/build"), name="react-app")

@app.get("/api/getIcal")
async def get_ical():
    # Your implementation here
    return JSONResponse(content={"message": "getIcal called!"})

@app.get("/getEmbeddedCalendarID")
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
        
        return JSONResponse(content={"calendarID": calendarID})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during calendar generation: {str(e)}")
    
   
    
    
    
    



# poetry run uvicorn app:app --port 5000 --reload
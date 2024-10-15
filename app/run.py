import uvicorn
from fastapi import FastAPI # need python-multipart
import app.views as my_app_views
from app.models import Base  # Import your Base to create tables
from app.database import engine
from app.load_csv_data import run as load_csv_data  # Import the CSV loader script's `run` method

app = FastAPI(title="AdviNow Interview Challenge", version="1.6")

# Use app.views.router instead of just views.router
app.include_router(my_app_views.router)

# Function to initialize the database and load data
def initialize_database():

    # Drop all existing tables
    Base.metadata.drop_all(bind=engine)
    
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)
    
    # Load CSV data by calling the function from the external script
    load_csv_data()

# Ensure that the data is loaded when the app starts (for development)
@app.on_event("startup")
async def startup_event():
    initialize_database()
    print("data loaded")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)

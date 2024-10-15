from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business, Symptom
import io
import csv

router = APIRouter()


@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
    
@router.get('/symptoms')
async def get_symptoms(business_id: int = None, diagnostic: str = None, db: Session = Depends(get_db)):
    query = db.query(Business.id, Business.name, Symptom.code, Symptom.name, Symptom.diagnostic).join(Symptom)

    if business_id:
        query = query.filter(Business.id == business_id)  # Filter by provided Business ID

    if diagnostic:
        query = query.filter(Symptom.diagnostic.ilike(diagnostic))  # Case-insensitive matching for diagnostic

    result = query.all()

    return [{"business_id": r[0], "business_name": r[1], "symptom_code": r[2], "symptom_name": r[3], "symptom_diagnostic": r[4]} for r in result]

@router.post("/import-csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check if the file is a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    # Read and decode the file contents
    content = await file.read()
    # Process CSV content and insert it into the database
    csv_data = io.StringIO(content.decode("utf-8-sig"))

    # Use csv.DictReader to read the file content as a CSV
    reader = csv.DictReader(csv_data)

    for row in reader:
        # Ensure that the required fields are present in each row
        if not all(key in row for key in ['Business ID', 'Business Name', 'Symptom Code', 'Symptom Name', 'Symptom Diagnostic']):
            raise HTTPException(status_code=400, detail="Missing required fields in CSV data.")

        # Check if the business already exists in the database
        business = db.query(Business).filter_by(id=row['Business ID']).first()

        if not business:
            # Create a new business if it doesn't exist
            business = Business(id=int(row['Business ID']), name=row['Business Name'])
            db.add(business)
            db.commit()
            db.refresh(business)  # Get the business ID from the database

        # Insert or update the symptom associated with the business
        symptom = Symptom(
            code=row['Symptom Code'],
            name=row['Symptom Name'],
            diagnostic=row['Symptom Diagnostic'].strip().lower(),  # Normalize diagnostic values
            business_id=business.id  # Associate with the correct business
        )
        db.add(symptom)
    
    # Commit the changes after processing all rows
    db.commit()
    
    # Assume you have logic to parse CSV and load data into Business and Symptom tables
    return {"status": "CSV imported successfully"}
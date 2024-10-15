import csv
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business, Symptom
from pathlib import Path

# Define the path to your CSV file
csv_file_path = Path(__file__).parent / "data/business_symptom_data.csv"

def run():
    db: Session = next(get_db())  # Initialize database session

    # Open the CSV file and load its content
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Check if the business already exists in the database
            business = db.query(Business).filter_by(name=row['Business Name']).first()

            if not business:
                # Create a new business if it doesn't exist
                business = Business(id=int(row['Business ID']), name=row['Business Name'])
                db.add(business)
                db.commit()
                db.refresh(business)  # Refresh to get the business id

            # Create a new symptom associated with the business
            symptom = Symptom(
                code=row['Symptom Code'],
                name=row['Symptom Name'],
                diagnostic=row['Symptom Diagnostic'],
                business_id=business.id
            )
            db.add(symptom)

        # Commit all changes
        db.commit()

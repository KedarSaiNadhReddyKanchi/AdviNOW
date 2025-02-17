# AdviNOW
Coding Challenge Invitation

# AdviNow Interview Challenge
This repository will be used as a test case for interview candidates. The application structure is predefined using FastAPI and uvicorn in the "app" directory in the "run.py" module. 
FastAPI creates API docs automatically, and these can be found at "http://127.0.0.1:8013/docs" when the app is running.

Please follow the instructions below to define data modules, generate a database through migration files, and create an API to return symptom data based on business logic.

Below are all the tasks/expectations required to complete this challenge. These tasks are not listed in any defined order, and you may go about these tasks in any order you see best:

**Please organize these tasks and update the ReadMe based on the order you complete them!**

- Create data models - example with sqlalchemy in "app\models.py"
- Create an endpoint that returns business and symptom data
  - Endpoint should take two optional parameters - business_id & diagnostic
  - Endpoint should return Business ID, Business Name, Symptom Code, Symptom Name, and Symptom Diagnostic values based on filter
- Generate migration script and run migration to create database tables - alembic files provided
  - To create a migration file: "alembic revision --autogenerate -m some_comment"
  - To update database with migration file: "alembic upgrade head"
- Design a database mock up based on the provided data - "app\data\business_symptom_data.csv"
- Create an endpoint for importing a CSV file into the database
  - The only requirement is the endpoint requires a CSV file. If needed, other parameters can be used.
- Create a virtual environment and install the requirements - "requirements\requirements.txt"

As a note, FastAPI, uvicorn, sqlalchemy, and alembic are not required to be used and may be changed if desired. 
Any of the existing files or variables can be and may need to be changed or updated, please be prepared to explain changes on the follow-up call.
The final end result should be a filled database, two working APIs, and an accessible API docs page.

# Setup Instructions

1. **Clone the Repository**:
  ```bash
  git clone https://github.com/KedarSaiNadhReddyKanchi/AdviNOW.git
  ```
2. **Navigate into the code base**:
  ```bash
  cd AdviNow
  ```
3. **Create a Virtual Environment (Optional)**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

4. **Install the Dependencies: Install the required Python packages**:
  ```bash
  pip install -r requirements/requirements.txt
  ```

5. **Setup Environment Variables (Optional)**: Create a .env file in the root of your project with your PostgreSQL database credentials:
  ```bash
  DB_HOST=localhost
  DB_NAME=your_database_name
  DB_USER=your_database_user
  DB_PWD=your_database_password
  ```

# Running the App
To start the FastAPI application locally, run the following command:
  ```bash
  uvicorn app.run:app --reload --port 8013
  ```

The app will be accessible at http://127.0.0.1:8013.

# Database Migrations
Alembic is used for managing database migrations. Before running the application, you need to apply the database schema:

1. **Generate a Migration (Optional)**: If you modify the models in the app/models.py, generate a migration using:
  ```bash
  alembic revision --autogenerate -m "Your migration message"
  ```

2. **Apply the Migrations**: Run the following command to apply migrations and set up the database tables:
  ```bash
  alembic upgrade head
  ```

# Endpoints

**Symptom Query Endpoint**

1. ***URL***: /symptoms
2. ***Method***: GET
3. ***Description***: Retrieve business and symptom data filtered by business_id or symptom diagnostic values.
4. ***Parameters***:
   - business_id (optional): Integer (e.g., 1004)
   - diagnostic (optional): String (e.g., TRUE)
5. Example
  ```bash
  curl http://127.0.0.1:8013/symptoms?business_id=1004&diagnostic=TRUE
  ```
6. Response
  ```bash
  [
    {
      "business_id": 1004,
      "business_name": "SportHealth",
      "symptom_code": "SYMPT0001",
      "symptom_name": "Patient Age",
      "symptom_diagnostic": "true"
    },
  ...
]
  ```

**CSV Import Endpoint**

1. ***URL***: /import-csv
2. ***Method***: POST
3. ***Description***: Upload a CSV file to bulk import Business and Symptom data.
4. ***CSV Requirement***: The CSV must have the following headers:
   - Business ID,
   - Business Name
   - Symptom Code
   - Symptom Name
   - Symptom Diagnostic
5. ***Used the CSV file*** - business_symptom_data present in the app/data directory for initial data load.
6. ***For thge CSV Import Endpoint***, I have created a new CSV file called - new_checking_data.csv which is also present in the app/data directory.
     - The data in this file is also similar to the data in the business_symptom_data.csv file.
     - The reason for creating this new file was to implement the flow where this data gets appended to the already present data in the database which was initially loaded from the business_symptom_data.csv file. 
5. Example CSV Data:
  ```bash
  Business ID,Business Name,Symptom Code,Symptom Name,Symptom Diagnostic
  1004,SportHealth,SYMPT0001,Patient Age,TRUE
  1104,MedStop,SYMPT0002,Fatigue,TRUE
  ```

# Database Reset
If you want to reset the database by dropping and recreating all tables before each run, the initialize_database function in run.py already handles this by calling:
  ```bash
  Base.metadata.drop_all(bind=engine)  # Drops all existing tables
Base.metadata.create_all(bind=engine)  # Recreates all tables
  ```

When the app starts, it will drop the existing tables and load new data from the CSV if the initialize_database() is triggered at startup.





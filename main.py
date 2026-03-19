from fastapi import FastAPI, Path , HTTPException, Query # Path enhance readability of path parameters
import json
from pydantic_model import Patient
from fastapi.responses import JSONResponse
from patient_update_pydantic import PatientUpdate

app=FastAPI() # object 

def load_data():
    with open('patients.json','r') as f: #The with statement in Python is used to handle resources safely by automatically managing setup and cleanup operations, such as opening and closing files.
        data=json.load(f)
    return data

def save_data(data):  
    with open('patients.json','w') as f:
        json.dump(data, f)
    

@app.get("/") # <-- (define route) means if my website is abc.com then abc.com/ will hit     this endpoint
def hello():
    return{'message':'Patient management system api'}

@app.get("/about")
def about():
    return {'message':'To  manage patient records'}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description='ID of the patient in DB', example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    #return {'error':'patient not found'}
    raise HTTPException(status_code=404, detail='patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on basis of  height, weight or BMI'), order : str = Query('asc', description='sort in asc or dsc order')):
    valid_fields=['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='invalid order select between asc and desc')
    data=load_data()

    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
# here ... means requred so sort_by field is required and order is optional with default value asc

@app.post('/create')
def create_patient(patient : Patient): # ahiya manually data pydentic object ma nakhi ne validate karvani jarur nathi FastAPI automatically handle kari lese
    # load existing data
    data=load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # new patient added to database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into jason file
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})

#Meaning of This Line
# def create_patient(patient: Patient):

# patient → parameter name

# : Patient → type annotation using a Pydantic model

# This means the function expects request body data that matches the Patient Pydantic model.

# What FastAPI Does Automatically

# When a request comes like:

# {
#  "id": 1,
#  "name": "Jenish",
#  "age": 22,
#  "weight": 75
# }

# FastAPI automatically:

# Reads the JSON request body

# Converts it into a Python dictionary

# Validates it using the Pydantic Patient model

# Creates a Patient object

# Passes it to the function as patient

# So inside the function:

# patient

# is already a validated Pydantic object.

# Why This is an Advantage of Pydantic

# Without Pydantic you would need to manually:

# Read JSON

# Validate fields

# Check data types

# Handle missing fields

# With Pydantic + FastAPI this happens automatically.

# Example

# Instead of writing:

# data = request.json()
# name = data["name"]
# age = int(data["age"])

# FastAPI directly gives:

# patient.name
# patient.age
# Short Note (for your notes)

# Advantage of Pydantic in FastAPI

# When a parameter is typed with a Pydantic model (e.g., patient: Patient), FastAPI automatically converts the incoming JSON request body into a validated Pydantic object. This removes the need for manual data parsing and validation.


@app.put('/edit/{patient_id}')
def upadet_patient(patient_id: str, patient: PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patientInfo=data[patient_id]
    updated_patient_info= patient.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patientInfo[key]=value

# now we need to calculate updated bmi and verdict so we will create new pydantic object based on existing_patientInfo it will automaticaly do  bmi and verdict calculation , data and type validation   after that we will again convert it into dictionary and will update database

#existing_patientInfo <- this has not id attribute so first we have to add it before converting it into pydantic object

    existing_patientInfo['id']=patient_id

    # dict -> pydantic object
    patient_pydantic_object=Patient(**existing_patientInfo)

    # pydantic_obj -> dict
    existing_patientInfo=patient_pydantic_object.model_dump(exclude='id');

    data[patient_id]=existing_patientInfo 

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not exists")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':"patient deleted successfully"})
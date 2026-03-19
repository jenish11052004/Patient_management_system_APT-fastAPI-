from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name:Annotated[str, Field(..., description="Not more than 50 caharacters")]
    city:Annotated[str, Field(..., description="City where the patient is living")]
    age:Annotated[int, Field(..., gt=0, le=120, description="Age of patient")]
    gender:Annotated[Literal['male', 'female', 'other'], Field(..., description="Patient's gender")]
    height:Annotated[float, Field(..., gt=0, description="Hight of the patient in meters")]
    weight:Annotated[float, Field(..., gt=0, description="Wight of the patient kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        calculate_bmi=round(self.weight / (self.height**2), 2)
        return calculate_bmi
    
    @computed_field
    @property
    def verdict(self) -> str :
        if self.bmi < 18.5:
            return 'underWeight'
        elif self.bmi < 30:
            return 'Normal'
        return 'Obese'
        
    

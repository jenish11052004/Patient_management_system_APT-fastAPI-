from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class PatientUpdate(BaseModel):

    name:Annotated[Optional[str], Field(default=None)]
    city:Annotated[Optional[str], Field(default=None)]
    age:Annotated[Optional[int], Field(default=None, gt=0, le=120)]
    gender:Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height:Annotated[Optional[float], Field(default=None, gt=0)]
    weight:Annotated[Optional[float], Field(default=None, gt=0)]

        
    

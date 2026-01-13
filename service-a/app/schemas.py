from pydantic import BaseModel, IPvAnyAddress

class IPValidation(BaseModel):
     ip: IPvAnyAddress
from pydantic import BaseModel, Field

# Define schema for tool input
class CreateContactInput(BaseModel):
    email: str = Field(..., description="Email address of the contact")
    firstName: str = Field(..., description="First name of the contact")
    lastName: str = Field(..., description="Last name of the contact")

    
# Define schema for tool input
class RegisterForEventInput(BaseModel):
    contactId: int = Field(..., description="contactId of the contact.")
    eventName: str = Field(..., description="name of the event.")
    regType: str = Field(..., description="Type of registration.")

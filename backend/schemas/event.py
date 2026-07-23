from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    title: str
    city: str
    category: str
    date: str
    venue: str
    description: str



class EventUpdate(BaseModel):
    title: str | None = None
    city: str | None = None
    category: str | None = None
    date: str | None = None
    venue: str | None = None
    description: str | None = None


    

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    city: str
    category: str
    date: str
    venue: str
    description: str
from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    title: str
    city: str
    category: str
    date: str
    venue: str
    description: str


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    city: str
    category: str
    date: str
    venue: str
    description: str
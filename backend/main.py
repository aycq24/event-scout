from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers.events import router as events_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello Event Scout!"}




app.include_router(events_router)
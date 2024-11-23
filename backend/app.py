from fastapi import FastAPI
from routers import documents, queries  # Import your API routes
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routers import auth  # Import the auth router


# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key (or any other keys)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Ensure it's set in the .env file.")

app = FastAPI()

# Middleware for CORS (to allow frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth")  
app.include_router(documents.router)
app.include_router(queries.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Question-Answering API!"}

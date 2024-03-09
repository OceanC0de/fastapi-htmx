from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_htmx import htmx_init
from pydantic import BaseModel
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from random import sample
from pathlib import Path
from app.config import templates, ioc_collection

htmx_init(templates)
# Load environment variables

# FastAPI app initialization
app = FastAPI()

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

from app.routers.routers import router
app.include_router(router)  # Include the router in your main app

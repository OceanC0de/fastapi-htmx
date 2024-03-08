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

htmx_init(templates=Jinja2Templates(directory=Path("my_app") / "templates"))
# Load environment variables
load_dotenv()

# MongoDB connection string
connection_string = os.getenv('COSMOS_CONNECTION_STRING')

# MongoDB client initialization
client = MongoClient(connection_string)
db = client['iocs']  # Database name
ioc_collection = db['ioccollection']  # Collection name

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

@app.get("/")
async def read_root(request: Request):
    # Fetch random IOCs (or you can limit the number of documents to fetch if the collection is large)
    iocs_cursor = ioc_collection.find({}).limit(3)  # Adjust the limit as needed
    iocs = list(iocs_cursor)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "random_iocs": iocs
    })

@app.get("/ioc/")
async def get_ioc(ioc: str = Query(None)):
    if ioc:
        ioc_data = ioc_collection.find_one({"ioc": ioc})
        if ioc_data:
            ioc_data.pop('_id', None)
            return ioc_data
    raise HTTPException(status_code=404, detail="IOC not found")

@app.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}

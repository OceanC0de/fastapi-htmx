# app/config.py
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from environment variable
connection_string = os.getenv('COSMOS_CONNECTION_STRING')

# Establish connection to MongoDB (Cosmos DB)
client = MongoClient(connection_string)
db = client['iocs']  # Use your new database name here
ioc_collection = db['ioccollection']  # Use your new collection name here

TEMPLATES_DIRECTORY = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

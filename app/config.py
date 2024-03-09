# app/config.py
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pathlib import Path
import os

# Load environment variables, assuming dotenv is already loaded elsewhere or you're setting environment variables through another method
connection_string = os.getenv('COSMOS_CONNECTION_STRING')

client = MongoClient(connection_string)
db = client['iocs']  # 'iocs' is your database name
ioc_collection = db['ioccollection']  # 'ioccollection' is your collection name

TEMPLATES_DIRECTORY = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

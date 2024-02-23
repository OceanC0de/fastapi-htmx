from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# MongoDB connection string
connection_string = os.getenv('COSMOS_CONNECTION_STRING')

# MongoDB client initialization
client = MongoClient(connection_string)
db = client['pokemon2']  # Database name
pokemon_collection = db['collection2']  # Collection name

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

# Model definition
class Pokemon(BaseModel):
    name: str
    type: str
    description: str

# Route Handlers
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}

@app.post("/pokemon")
async def add_pokemon(pokemon: Pokemon):
    pokemon_dict = pokemon.dict()
    existing_pokemon = pokemon_collection.find_one({"name": pokemon.name})
    if existing_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already exists")
    pokemon_collection.insert_one(pokemon_dict)
    return {"message": f"{pokemon.name} added to the database!"}

@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    pokemon = pokemon_collection.find_one({"name": name})
    if pokemon:
        # Excluding the MongoDB generated ID in the response
        pokemon.pop('_id', None)
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

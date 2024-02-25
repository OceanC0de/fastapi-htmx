from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from random import sample
from fastapi_htmx import htmx_init
from pathlib import Path

htmx_init(templates=Jinja2Templates(directory=Path("my_app") / "templates"))
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

# Adjust your Pydantic model for form data
class PokemonForm(BaseModel):
    name: str
    type: str
    description: str

# Route Handlers
@app.get("/")
async def read_root(request: Request):
    # Fetch all Pokémon names (or you can limit the number of documents to fetch if the collection is large)
    all_pokemon = list(pokemon_collection.find({}, {'name': 1, '_id': 0}))
    # Extract names and choose up to 3 random ones
    all_names = [p['name'] for p in all_pokemon]
    random_names = sample(all_names, min(len(all_names), 3))
    # Get the full details of these random Pokémon
    random_pokemon = [pokemon_collection.find_one({"name": name}) for name in random_names]
    # Pass them to the template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "random_pokemon": random_pokemon,
        "weekday": datetime.now().strftime("%A")  # Add this line to include the weekday in the context
    })

@app.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}

@app.post("/pokemon")
async def add_pokemon(name: str = Form(...), type: str = Form(...), description: str = Form(...)):
    pokemon_dict = {"name": name, "type": type, "description": description}
    existing_pokemon = pokemon_collection.find_one({"name": name})
    if existing_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already exists")
    pokemon_collection.insert_one(pokemon_dict)
    return {"message": f"{name} added to the database!"}

@app.get("/pokemon/")
async def get_pokemon(name: str = Query(None)):
    if name:
        pokemon = pokemon_collection.find_one({"name": name})
        if pokemon:
            pokemon.pop('_id', None)
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

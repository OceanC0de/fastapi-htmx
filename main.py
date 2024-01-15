from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the Cosmos DB connection string from environment variable
connection_string = os.getenv('COSMOS_CONNECTION_STRING')

# Initialize the Cosmos client
client = CosmosClient.from_connection_string(conn_str=connection_string)

# Database and Container configuration
database_name = 'pokemon'
container_name = 'collection1'

# Create or get the database and container
database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/name"),
    offer_throughput=400
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Model definitions
class Pokemon(BaseModel):
    name: str
    type: str
    description: str

class UserInput(BaseModel):
    username: str

class TextToMorseRequest(BaseModel):
    text: str

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', 
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': ' ', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', 
    '(': '-.--.', ')': '-.--.-'
}

def text_to_morse(text: str) -> str:
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

# FastAPI route handlers
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}

@app.post("/submit")
async def submit_data(user_input: UserInput):
    return {"message": f"Hello, {user_input.username}!"}

@app.post("/text-to-morse")
async def text_to_morse_endpoint(request: TextToMorseRequest):
    morse_code = text_to_morse(request.text)
    return {"morse_code": morse_code}

@app.post("/pokemon")
async def add_pokemon(pokemon: Pokemon):
    try:
        container.upsert_item({
            'id': pokemon.name.lower(),  # Use Pokémon name as a unique ID
            'name': pokemon.name,  # Partition key
            'type': pokemon.type,
            'description': pokemon.description
        })
        return {"message": f"{pokemon.name} added to the database!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    try:
        item_response = container.read_item(item=name.lower(), partition_key=name)
        return item_response
    except exceptions.CosmosResourceNotFoundError:
        return {"error": "Pokemon not found"}
    except Exception as e:
        return {"error": str(e)}
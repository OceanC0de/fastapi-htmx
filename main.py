from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}
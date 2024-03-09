# routers.py
from fastapi import APIRouter, Request, HTTPException, Query
from datetime import datetime
from app.config import templates, ioc_collection

router = APIRouter()

@router.get("/")
async def read_root(request: Request):
    iocs_cursor = ioc_collection.find({}).limit(1)
    iocs = list(iocs_cursor)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "random_iocs": iocs
    })

@router.get("/ioc/")
async def get_ioc(ioc: str = Query(None)):
    if ioc:
        ioc_data = ioc_collection.find_one({"ioc": ioc})
        if ioc_data:
            ioc_data.pop('_id', None)
            return ioc_data
    raise HTTPException(status_code=404, detail="IOC not found")

@router.get("/weekday")
async def get_weekday():
    weekday = datetime.now().strftime("%A")
    return {"weekday": weekday}

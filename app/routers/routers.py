# routers.py
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.config import templates, ioc_collection
from app.routers import plot_router

router = APIRouter()

@router.get("/", include_in_schema=False)
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

@router.get("/plots", include_in_schema=False)
async def plots():
    return HTMLResponse(content="""
        <div class="column">
            <div class="container">
                <h3 class="title">Raspberry Pi - CPU Temperature over Time</h3>
                <div class="plot-wrapper">
                    <div id="plot-container-temp" hx-get="/plot/cpu_temp" hx-target="#plot-container-temp" hx-swap="outerHTML" hx-trigger="load">
                        <div id="plot-temp"></div>
                    </div>
                </div>
            </div>

            <div class="container">
                <h3 class="title">Raspberry Pi - CPU Load over Time</h3>
                <div class="plot-wrapper">
                    <div id="plot-container-load" hx-get="/plot/cpu_load" hx-target="#plot-container-load" hx-swap="outerHTML" hx-trigger="load">
                        <div id="plot-load"></div>
                    </div>
                </div>
            </div>

            <div class="container">
                <h3 class="title">Raspberry Pi - Memory Used over Time</h3>
                <div class="plot-wrapper">
                    <div id="plot-container-memory" hx-get="/plot/memory_used" hx-target="#plot-container-memory" hx-swap="outerHTML" hx-trigger="load">
                        <div id="plot-memory"></div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            document.querySelectorAll('.navbar-item').forEach(function(item) {
                item.classList.remove('active');
                item.removeAttribute('hx-disable');
            });
            var activeNavItem = document.querySelector('.navbar-item[hx-get="/plots"]');
            activeNavItem.classList.add('active');
            activeNavItem.setAttribute('hx-disable', '');
        </script>
    """, status_code=200)

@router.get("/iocs", include_in_schema=False)
async def iocs(request: Request):
    iocs_cursor = ioc_collection.find({}).limit(1)
    iocs = list(iocs_cursor)
    return HTMLResponse(content="""
        <div class="container">
            <h3 class="title">Search for an IOC</h3>
            <div>
                <form
                    method="get"
                    hx-get="/ioc/"
                    hx-target="#iocResponse"
                    hx-swap="innerHTML"
                >
                    <div class="field">
                        <!--<label class="label">Search IOC by Value</label>-->
                        <div class="control">
                            <input
                                class="input"
                                type="text"
                                id="iocSearchInput"
                                name="ioc"
                                placeholder="e.g. 91.92.250.61:3232"
                                required
                            />
                        </div>
                    </div>
                    <div class="control">
                        <button type="submit" class="button is-info">
                            Get
                        </button>
                    </div>
                </form>
                <div id="iocResponse" class="json-response">
                    <!-- The server should respond with a table or table row(s) here -->
                    <!-- JSON response will be styled here -->
                </div>
            </div>
            <h3 class="title">Example IOC</h3>
            <table class="is-striped is-fullwidth table">
                <thead>
                    <tr>
                        <th>First Seen</th>
                        <th>IOC</th>
                        <th>Type</th>
                        <th>Malware</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>2024-03-08 22:00:08 UTC</td>
                        <td>91.92.250.61:3232</td>
                        <td>ip:port</td>
                        <td>AsyncRAT</td>
                        <td>75</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <script>
            document.querySelectorAll('.navbar-item').forEach(function(item) {
                item.classList.remove('active');
                item.removeAttribute('hx-disable');
            });
            var activeNavItem = document.querySelector('.navbar-item[hx-get="/iocs"]');
            activeNavItem.classList.add('active');
            activeNavItem.setAttribute('hx-disable', '');
        </script>
    """, status_code=200)

router.include_router(plot_router.router)  # Move this line here
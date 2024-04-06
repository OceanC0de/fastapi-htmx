import numpy as np
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.charts import make_chart
from app.database import fetch_data_from_cosmosdb
from app.charts import make_chart

router = APIRouter()

def smooth_data(data, window_size):
    data_array = np.array(data)
    smoothed_data = np.convolve(data_array, np.ones(window_size) / window_size, mode='valid')
    return smoothed_data.tolist()

async def plot_metric(request: Request, metric: str, y_axis_title: str):
    # Fetch data from CosmosDB
    data = fetch_data_from_cosmosdb()
    x_data = [item["timestamp"] for item in data]
    y_data = [item[metric] for item in data]

    if not y_data:
        # Handle the case when there is no data available
        return HTMLResponse(content="No data available for the last 60 minutes.")

    # Smooth the y_data using a moving average
    window_size = 5
    smoothed_y_data = smooth_data(y_data, window_size)

    chart_html = make_chart(x_data=x_data, y_data=smoothed_y_data, ticker_symbol="", x_axis_title="", y_axis_title=y_axis_title)
    return HTMLResponse(content=f'<div id="plot-{metric}">{chart_html}</div>')

@router.route("/plot/cpu_temp", methods=["GET"])
async def plot_cpu_temp(request: Request):
    return await plot_metric(request, "cpu_temp", "CPU Temperature (°C)")

@router.route("/plot/cpu_load", methods=["GET"])
async def plot_cpu_load(request: Request):
    return await plot_metric(request, "cpu_load", "CPU Load (%)")

@router.route("/plot/memory_used", methods=["GET"])
async def plot_memory_used(request: Request):
    return await plot_metric(request, "memory_used", "Memory Used (MB)")
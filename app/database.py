from pymongo import MongoClient
from datetime import datetime, timedelta
from pytz import UTC
from app.config import connection_string

client = MongoClient(connection_string)
db = client['rapi_health_monitoring']
metrics_collection = db['metrics']

def fetch_data_from_cosmosdb():
    # Get the current timestamp in UTC
    current_timestamp = datetime.now(UTC)

    # Calculate the timestamp 60 minutes ago in UTC
    one_hour_ago = current_timestamp - timedelta(minutes=60)

    # Fetch data from the 'metrics' collection in CosmosDB for the last 60 minutes
    data = list(metrics_collection.find({
        "timestamp": {"$gte": one_hour_ago.isoformat()}
    }))

    return data
from clickhouse_driver import Client
from .schemas import AnalyticsEvent

client = Client(
    host='clickhouse',
    port=9000,
    user='default',
    password='mysecret',
    database='default'
)

# Create DB and table if they don't exist
client.execute("CREATE DATABASE IF NOT EXISTS analytics")
client.execute("""
    CREATE TABLE IF NOT EXISTS analytics.page_events (
        event_type String,
        page_url String,
        user_agent String,
        timestamp DateTime
    ) ENGINE = MergeTree() ORDER BY timestamp
""")

def insert_event(event: AnalyticsEvent):
    client.execute(
        "INSERT INTO analytics.page_events (event_type, page_url, user_agent, timestamp) VALUES",
        [(event.event_type, event.page_url, event.user_agent, event.timestamp)]
    )

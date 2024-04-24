from celery import Celery

from tasks import FetchLinks, ParseXML

# Initialize Celery app
app = Celery(
    "parser",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    broker_connection_retry_on_startup=True,
)
# assign tasks
fetch_task = app.register_task(FetchLinks())
parse_xml_task = app.register_task(ParseXML())

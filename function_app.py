import azure.functions as func
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return func.HttpResponse(
        f"Hello, World! Current time: {current_time}",
        status_code=200
    ) 
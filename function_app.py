import azure.functions as func
import logging
from datetime import datetime


app = func.FunctionApp()


@app.function_name(name="HttpTrigger")
@app.route(route="hello")
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f'Python HTTP trigger function processed a request at {current_time}'
        )
        
        return func.HttpResponse(
            f"Hello, World! Current time: {current_time}",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in function execution: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        ) 
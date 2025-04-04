import azure.functions as func
import logging
from datetime import datetime


app = func.FunctionApp()


@app.function_name(name="HttpTrigger")
@app.route(route="hello", methods=["GET", "POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')
        
        # Log request details
        logging.info(f'Request method: {req.method}')
        logging.info(f'Request URL: {req.url}')
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_message = f"Hello, World! Current time: {current_time}"
        
        logging.info(f'Sending response: {response_message}')
        
        return func.HttpResponse(
            response_message,
            status_code=200,
            mimetype="text/plain"
        )
    except Exception as e:
        error_message = f"Error in function execution: {str(e)}"
        logging.error(error_message)
        return func.HttpResponse(
            error_message,
            status_code=500,
            mimetype="text/plain"
        ) 
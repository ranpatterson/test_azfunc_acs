import os
import azure.functions as func
import logging
from azure.communication.sms import SmsClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_acs", methods=["POST"])
def http_acs(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        payload = req.get_json()
        to_phone = payload.get('to')
        message = payload.get('message')
        if not to_phone or not message:
            return func.HttpResponse("Missing 'to' or 'message' in JSON payload.", status_code=400)
        connectionString = os.environ.get('ACS_CONNECTION_STRING')
        from_phone = os.environ.get('FROM_PHONE')
        if not connectionString or not from_phone:
            return func.HttpResponse("Missing ACS Connection String or from phone number in environment variables.", status_code=400)

        logging.info(f"to_phone: {to_phone}")
        logging.info(f"from_phone: {from_phone}")
        logging.info(f"message: {message}")

        #sms_client = SmsClient(endpoint, DefaultAzureCredential())
        sms_client = SmsClient.from_connection_string(connectionString)
        sms_client.send(
            from_=from_phone,
            to=[to_phone],
            message=message,
            enable_delivery_report=True
        )
        return func.HttpResponse(f"Message sent to {to_phone}", status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Failed to send message.", status_code=500)
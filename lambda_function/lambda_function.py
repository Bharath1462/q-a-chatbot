import json
import boto3
import os

sagemaker_runtime = boto3.client('sagemaker-runtime')
ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT_NAME']

def lambda_handler(event, context):
    try:
        # Parse input from API Gateway
        if 'body' not in event:
            return error_response("Missing request body", 400)
            
        request_body = json.loads(event['body'])
        
        # Validate input format (critical for LLM deployments)
        if 'inputs' not in request_body:
            return error_response("Missing 'inputs' in request body", 400)
        
        # Prepare SageMaker payload
        payload = {
            "inputs": request_body['inputs'],
            "parameters": request_body.get('parameters', {})
        }
        
        # Invoke SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        # Parse SageMaker response
        result = json.loads(response['Body'].read().decode())
        
        return success_response(result)
        
    except json.JSONDecodeError:
        return error_response("Invalid JSON format", 400)
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)

# Helper functions for standardized responses
def success_response(body):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Required for web browser
        },
        'body': json.dumps({'success': True, 'data': body})
    }
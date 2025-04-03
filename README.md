# Azure Function Hello World

This is a simple "Hello World" Azure Function implemented in Python, with a complete CI/CD pipeline using Jenkins.

## Project Structure

- `function_app.py`: Main Azure Function implementation
- `test_function.py`: Test cases for the function
- `requirements.txt`: Python dependencies
- `Jenkinsfile`: Jenkins pipeline configuration

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest test_function.py -v
```

## CI/CD Pipeline

The project includes a Jenkins pipeline with three stages:
1. Build: Sets up Python environment and installs dependencies
2. Test: Runs automated tests
3. Deploy: Deploys the function to Azure Functions

### Jenkins Setup Requirements

1. Jenkins server with the following plugins installed:
   - Pipeline
   - GitHub
   - Azure CLI

2. Azure credentials configured in Jenkins:
   - AZURE_SUBSCRIPTION_ID
   - AZURE_TENANT_ID
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET

3. Update the following variables in the Jenkinsfile:
   - RESOURCE_GROUP
   - FUNCTION_APP_NAME

## Testing

The project includes three test cases:
1. Verifies the response contains "Hello, World!"
2. Checks if the status code is 200
3. Validates the response type is correct 
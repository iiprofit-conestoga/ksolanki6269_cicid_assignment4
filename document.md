# Azure Functions Deployment Documentation

## Overview
This project demonstrates the creation and deployment of an HTTP-triggered Azure Function using Jenkins for CI/CD. The function returns a "Hello, World!" message along with the current timestamp.

## Project Structure

### 1. `function_app.py`
**Purpose**: Main Azure Function code that handles HTTP requests.
- Contains HTTP trigger function
- Handles CORS requests
- Includes error handling and logging
- Returns timestamp with response

### 2. `host.json`
**Purpose**: Configuration file for Azure Functions runtime.
- Contains logging configuration
- Python worker settings
- CORS configuration
- Extension bundle settings

### 3. `local.settings.json`
**Purpose**: Local development settings for Azure Functions.
- Specifies Python runtime
- Development storage settings

### 4. `requirements.txt`
**Purpose**: Python dependencies for the Azure Function.
- Lists all required Python packages
- Specifies exact versions for compatibility

### 5. `test_function.py`
**Purpose**: Test cases for the Azure Function.
- Tests response content
- Tests status codes
- Tests response types

### 6. `Jenkinsfile`
**Purpose**: Jenkins pipeline configuration for CI/CD.
- Defines deployment stages
- Handles Azure authentication
- Manages deployment process

## Step-by-Step Implementation Process

### 1. Initial Setup

#### Azure Resources Creation
1. **Create Resource Group**:
   - Go to Azure Portal
   - Search for "Resource groups"
   - Click "Create"
   - Name: "myfunction-rg"
   - Select region
   - Click "Review + create"

2. **Create Function App**:
   - Go to Azure Portal
   - Search for "Function App"
   - Click "Create"
   - Select resource group: "myfunction-rg"
   - Name: "myfunction-function"
   - Select "Python" as runtime
   - Select Python version 3.8
   - Select "Consumption" plan
   - Click "Review + create"

3. **Create Service Principal**:
   ```bash
   # First, ensure Azure CLI is installed
   # For macOS
   brew install azure-cli

   # For Windows
   # Download MSI installer from Microsoft website

   # Verify Azure CLI installation
   az --version

   # Login to Azure
   az login

   # Create service principal
   az ad sp create-for-rbac --name "myfunction-sp" --role contributor \
                           --scopes /subscriptions/{subscription-id}/resourceGroups/myfunction-rg \
                           --sdk-auth
   ```
   - Save the output JSON for Jenkins credentials

#### Local Development Environment Setup

1. **Install Python 3.8**:
   ```bash
   # For macOS
   brew install python@3.8

   # For Windows
   # Download Python 3.8 installer from python.org

   # Verify installation
   python3.8 --version
   ```

2. **Install Azure CLI**:
   ```bash
   # For macOS
   brew install azure-cli

   # For Windows
   # Download MSI installer from Microsoft website

   # Verify installation
   az --version
   ```

3. **Install Azure Functions Core Tools**:
   ```bash
   # For macOS
   brew tap azure/functions
   brew install azure-functions-core-tools@4

   # For Windows
   # Download installer from Microsoft website

   # Verify installation
   func --version
   ```

### 2. Function Development

1. **Create Basic Function**:
   - Create `function_app.py`
   - Implement HTTP trigger
   - Add error handling
   - Include CORS support

2. **Configure Function**:
   - Create `host.json`
   - Create `local.settings.json`
   - Update `requirements.txt`

3. **Test Locally**:
   ```bash
   func start
   ```

### 3. CI/CD Pipeline Setup

#### Jenkins Configuration
1. **Install Required Plugins**:
   - Azure CLI Plugin
   - GitHub Integration Plugin
   - Credentials Plugin

2. **Configure Azure Credentials**:
   - Go to Jenkins Dashboard
   - Click "Manage Jenkins" > "Manage Credentials"
   - Add new credentials with ID "azure-credentials"
   - Add these credentials:
     - AZURE_SUBSCRIPTION_ID
     - AZURE_TENANT_ID
     - AZURE_CLIENT_ID
     - AZURE_CLIENT_SECRET

3. **Server-side Azure CLI Installation**:
   ```bash
   # For Ubuntu/Debian
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

   # For RHEL/CentOS
   sudo dnf install 'python3-pip'
   pip3 install --user azure-cli
   ```
   - Verify installation: `az --version`

#### GitHub Integration
1. **Create GitHub Token**:
   - Go to GitHub Settings
   - Developer settings > Personal access tokens
   - Generate new token with repo access
   - Copy token for Jenkins

2. **Configure Jenkins GitHub Credentials**:
   - Add GitHub token in Jenkins credentials
   - ID: "github-credentials"

3. **Configure GitHub Webhook**:
   - Go to your GitHub repository
   - Settings > Webhooks > Add webhook
   - Payload URL: `http://your-jenkins-url/github-webhook/`
   - Content type: `application/json`
   - Secret: Generate a secure secret
   - Select events: "Just the push event"
   - Save webhook

### 4. Deployment Process

1. **Initial Deployment**:
   - Push code to GitHub
   - GitHub webhook triggers Jenkins
   - Function deploys to Azure

2. **Troubleshooting and Improvements**:
   - Fixed CORS issues
   - Updated configuration
   - Improved error handling

### 5. Testing and Verification

#### CORS Configuration
1. **Azure Portal CORS Settings**:
   - Go to Function App
   - Click "CORS"
   - Add allowed origins:
     ```
     https://portal.azure.com
     https://myfunction-function.azurewebsites.net
     http://localhost:7071
     ```
   - Enable "Access-Control-Allow-Credentials"
   - Click "Save"

#### Function URL Components
```
https://myfunction-function.azurewebsites.net/api/hello
```
- Base URL: `https://myfunction-function.azurewebsites.net`
- Function path: `/api/hello`
- Function key: You need to add your function key as a query parameter

#### Testing Methods

1. **Browser Testing**:
   - Open function URL in browser
   - Expected response: "Hello, World! Current time: [timestamp]"

2. **Postman Testing**:
   - Create new GET request
   - Enter function URL
   - Send request
   - Check response and status code

3. **Azure Portal Testing**:
   - Go to Function App
   - Click "Functions" > "HttpTrigger"
   - Click "Code + Test"
   - Configure test parameters:
     - HTTP method: GET
     - Query parameters: Add your function key
   - Click "Run"

4. **curl Testing**:
   ```bash
   # Add your function key as a query parameter
   curl "https://myfunction-function.azurewebsites.net/api/hello"
   ```

## Key Learnings
1. **Azure Functions Development**:
   - Proper configuration is crucial
   - Error handling improves reliability
   - CORS settings need careful attention

2. **CI/CD with Jenkins**:
   - Environment variables and credentials need proper configuration
   - Tool checks ensure pipeline has required dependencies
   - GitHub webhooks enable automated deployments

3. **Azure Deployment**:
   - Azure Functions Core Tools simplify deployment
   - Function keys provide secure access
   - Remote building on Azure ensures compatibility

## Conclusion
This project demonstrates the complete process of creating and deploying an Azure Function using CI/CD with Jenkins. The function returns a "Hello, World!" message with the current timestamp, and the entire process is automated through a Jenkins pipeline triggered by GitHub webhooks. 
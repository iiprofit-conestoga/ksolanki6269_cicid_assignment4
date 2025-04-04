pipeline {
    agent any
    
    environment {
        // These credentials should be configured in Jenkins Credentials Manager
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        // Update these with your actual Azure resource group and function app name
        RESOURCE_GROUP = 'ksolanki6269-rg'  // Replace with your resource group name
        FUNCTION_APP_NAME = 'ksolanki6269-function'  // Replace with your function app name
    }
    
    triggers {
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    sh '''
                        # Check for required tools
                        command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
                        command -v zip >/dev/null 2>&1 || { echo "zip is required but not installed. Aborting."; exit 1; }
                        command -v az >/dev/null 2>&1 || { echo "Azure CLI is required but not installed. Aborting."; exit 1; }
                        command -v func >/dev/null 2>&1 || { echo "Azure Functions Core Tools is required but not installed. Aborting."; exit 1; }
                        
                        # Set up Python environment
                        python3 -m venv venv
                        . venv/bin/activate
                        python3 -m pip install --upgrade pip
                        python3 -m pip install --no-cache-dir -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        . venv/bin/activate
                        python3 -m pytest test_function.py -v
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying to Azure Functions...'
                    sh '''
                        # Create deployment package
                        echo "Creating deployment package..."
                        zip -r function.zip . -x "venv/*" "tests/*" "*.pyc" "__pycache__/*" ".git/*" ".pytest_cache/*"
                        
                        # Login to Azure
                        echo "Logging into Azure..."
                        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                        
                        # Deploy using Azure Functions Core Tools
                        echo "Deploying to Azure Functions..."
                        func azure functionapp publish $FUNCTION_APP_NAME --python --build remote --build-native-deps --nozip
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
} 
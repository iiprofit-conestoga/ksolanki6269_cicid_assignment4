pipeline {
    agent any
    
    environment {
        // These credentials should be configured in Jenkins Credentials Manager
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        // Update these with your actual Azure resource group and function app name
        RESOURCE_GROUP = 'ksolanki6269-rg'
        FUNCTION_APP_NAME = 'ksolanki6269-function'
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
                        
                        # Create a temporary directory for deployment
                        mkdir -p deploy
                        
                        # Copy necessary files to the deployment directory
                        cp function_app.py deploy/
                        cp requirements.txt deploy/
                        cp host.json deploy/
                        cp local.settings.json deploy/
                        
                        # Create the deployment package
                        cd deploy
                        zip -r ../function.zip .
                        cd ..
                        
                        # Login to Azure
                        echo "Logging into Azure..."
                        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                        
                        # Deploy using Azure Functions Core Tools
                        echo "Deploying to Azure Functions..."
                        cd deploy
                        func azure functionapp publish $FUNCTION_APP_NAME --python --build remote --build-native-deps
                        cd ..
                        
                        # Clean up
                        rm -rf deploy
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
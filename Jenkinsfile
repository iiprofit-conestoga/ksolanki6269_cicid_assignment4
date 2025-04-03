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
                        python3 -m venv venv
                        . venv/bin/activate
                        python3 -m pip install --upgrade pip
                        pip3 install -r requirements.txt
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
                        . venv/bin/activate
                        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                        zip -r function.zip . -x "venv/*" "tests/*" "*.pyc" "__pycache__/*"
                        az functionapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $FUNCTION_APP_NAME --src function.zip
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
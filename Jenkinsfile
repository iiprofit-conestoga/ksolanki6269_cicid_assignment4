pipeline {
    agent any
    
    environment {
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        RESOURCE_GROUP = 'your-resource-group'
        FUNCTION_APP_NAME = 'your-function-app-name'
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '. venv/bin/activate && python -m pytest test_function.py -v'
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
    }
} 
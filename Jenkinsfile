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
                        # Install Azure Functions Core Tools
                        curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
                        sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
                        sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -rs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
                        sudo apt-get update
                        sudo apt-get install -y azure-functions-core-tools@4
                        
                        # Create deployment package
                        zip -r function.zip . -x "venv/*" "tests/*" "*.pyc" "__pycache__/*"
                        
                        # Deploy using Azure Functions Core Tools
                        func azure functionapp publish $FUNCTION_APP_NAME --python --build remote --build-native-deps
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
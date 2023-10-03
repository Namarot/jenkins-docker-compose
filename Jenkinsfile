def envDetails = [
    dev: [
        sshCredentialId: 'jenkinsDev',
        remoteName: 'vagrant',
        remoteHost: '192.168.56.11',
        remotePort: '22',
        remoteUser: 'vagrant',
        gitBranch: 'dev',
        appDir: 'jenkins_app_dev',
        appPort: '9000',
        basePath: '~',
        cloneDir: 'jenkins_app_repo_dev',
        backupDir: 'jenkins_app_backup_dev'
    ],
    test: [
        sshCredentialId: 'jenkinsTest',
        remoteName: 'vagrant',
        remoteHost: '192.168.56.11',
        remotePort: '22',
        remoteUser: 'vagrant',
        gitBranch: 'test',
        appDir: 'jenkins_app_test',
        appPort: '10000',
        basePath: '~',
        cloneDir: 'jenkins_app_repo_test',
        backupDir: 'jenkins_app_backup_test'
    ],
    prod: [
        sshCredentialId: 'jenkinsProd',
        remoteName: 'vagrant',
        remoteHost: '192.168.56.11',
        remotePort: '22',
        remoteUser: 'vagrant',
        gitBranch: 'prod',
        appDir: 'jenkins_app_prod',
        appPort: '11000',
        basePath: '~',
        cloneDir: 'jenkins_app_repo_prod',
        backupDir: 'jenkins_app_backup_prod'
    ]
]

pipeline {
    agent any

    parameters {
        choice(
            name: 'envToDeploy', 
            choices: envDetails.keySet() as List, 
            description: 'Choose an environment to deploy'
        )
    }

    environment {
        GIT_REPO_URL = 'https://github.com/Namarot/jenkins-docker-compose.git'
    }

    stages {
        stage('Setup and Clone') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${params.SSH_USER}@${params.SSH_IP} \"
                        # Clone the repository
                        git clone ${params.GIT_REPO_URL} ${params.BASE_PATH}/${params.CLONE_DIR}

                        # Create folders
                        mkdir -p ${params.BASE_PATH}/${params.APP_DIR}
                        mkdir -p ${params.BASE_PATH}/${params.BACKUP_DIR}

                        # Backup
                        if [ -d ${params.BASE_PATH}/${params.APP_DIR} ]; then
                            cd ${params.BASE_PATH}
                            tar -czf ${params.BACKUP_DIR}/\$(date '+%Y-%m-%d-%H-%M')-backup.zip ${params.APP_DIR}
                        fi
                    \"
                """
            }
        }
        stage('Compose down and move files') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${params.SSH_USER}@${params.SSH_IP} \"
                        # Docker-compose down
                        cd ${params.BASE_PATH}/${params.APP_DIR}
                        docker-compose down

                        # Move files
                        rm -rf ${params.BASE_PATH}/${params.APP_DIR}/*
                        mv ${params.BASE_PATH}/${params.CLONE_DIR}/fastapi/* ${params.BASE_PATH}/${params.APP_DIR}/
                    \"
                """
            }
        }
        stage('Build and Start Docker Compose') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${params.SSH_USER}@${params.SSH_IP} \"
                        cd ${params.BASE_PATH}/${params.APP_DIR}
                        docker-compose build
                        docker-compose up -d
                    \"
                """
            }
        }
        stage('Show Output') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${params.SSH_USER}@${params.SSH_IP} \"
                        for i in {1..10}
                        do
                            curl --include http://localhost:8000
                            echo ''  # Newline for better readability
                        done
                    \"
                """
            }
        }
    }

    post {
        always {
            sh """
                ssh -o StrictHostKeyChecking=no ${params.SSH_USER}@${params.SSH_IP} \"
                    # Cleanup
                    rm -rf ${params.BASE_PATH}/${params.CLONE_DIR}
                \"
            """
        }
    }
}

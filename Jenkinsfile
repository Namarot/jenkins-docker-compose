pipeline {
    agent any

    parameters {
        string(name: 'SSH_USER', defaultValue: 'vagrant', description: 'SSH User for the VM')
        string(name: 'SSH_IP', defaultValue: '192.168.56.11', description: 'IP Address for the VM')
        string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/Namarot/jenkins-docker-compose.git', description: 'Git Repository URL')
        string(name: 'BASE_PATH', defaultValue: '~', description: 'Base Directory for Operations')
        string(name: 'CLONE_DIR', defaultValue: 'jenkinsapprepo', description: 'Directory Name for Cloned Repo')
        string(name: 'APP_DIR', defaultValue: 'jenkinsapp', description: 'Application Directory')
        string(name: 'BACKUP_DIR', defaultValue: 'jenkinsappbackups', description: 'Backup Directory')
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
                        docker-compose down
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

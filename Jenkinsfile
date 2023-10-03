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
        backupDir: 'jenkins_app_backup_dev',
        composeFilename: 'compose.yaml'
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
        backupDir: 'jenkins_app_backup_test',
        composeFilename: 'compose.yaml'
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
        backupDir: 'jenkins_app_backup_prod',
        composeFilename: 'compose.yaml'
    ]
]

def remote = [:]
remote.allowAnyHosts = true

def chosenEnv

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

    triggers {
        githubPush()
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Debug: Print the value of env.GIT_BRANCH
                    echo "env.GIT_BRANCH: ${env.GIT_BRANCH}"
                    
                    // If the pipeline is not triggered by webhook
                    if (!env.GIT_BRANCH) {
                        if (!params.envToDeploy) {
                            error("No environment selected")
                        }
                        env.GIT_BRANCH = params.envToDeploy
                    }

                    // Debug: Print the value of env.GIT_BRANCH after assignment
                    echo "env.GIT_BRANCH (after assignment): ${env.GIT_BRANCH}"

                    // Ensure the GIT_BRANCH value is one of 'dev', 'test', 'prod'
                    if (!(envDetails.keySet().contains(env.GIT_BRANCH))) {
                        error("Invalid branch: ${env.GIT_BRANCH}")
                    }

                    chosenEnv = envDetails[env.GIT_BRANCH]
                    remote.name = chosenEnv.remoteName
                    remote.host = chosenEnv.remoteHost
                    remote.post = chosenEnv.remotePort
                    remote.user = chosenEnv.remoteUser
                }
            }
        }
        stage('Clone and Backup') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: "${chosenEnv.sshCredentialId}", keyFileVariable: 'identity')]) {
                        remote.identityFile = identity
                        sshCommand remote: remote, command: "git clone -b ${chosenEnv.gitBranch} ${env.GIT_REPO_URL} ${chosenEnv.basePath}/${chosenEnv.cloneDir}"
                        sshCommand remote: remote, command: "mkdir -p ${chosenEnv.basePath}/${chosenEnv.appDir}"
                        sshCommand remote: remote, command: "mkdir -p ${chosenEnv.basePath}/${chosenEnv.backupDir}"
                        sshCommand remote: remote, command: """
                            if [ -d ${chosenEnv.basePath}/${chosenEnv.appDir} ]; then
                                cd ${chosenEnv.basePath}
                                tar -czf ${chosenEnv.backupDir}/\$(date '+%Y-%m-%d-%H-%M')-backup.zip ${chosenEnv.appDir}
                            fi
                        """
                    }
                }
            }
        }
        stage('Compose down and move files') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: "${chosenEnv.sshCredentialId}", keyFileVariable: 'identity')]) {
                        remote.identityFile = identity
                        sshCommand remote: remote, command: """
                            cd ${chosenEnv.basePath}/${chosenEnv.appDir}
                            if [ -f ${chosenEnv.composeFilename} ]; then
                                docker-compose down
                            else
                                echo "${chosenEnv.composeFilename} not found. Skipping docker-compose down."
                            fi
                        """
                        sshCommand remote: remote, command: "rm -rf ${chosenEnv.basePath}/${chosenEnv.appDir}/*"
                        sshCommand remote: remote, command: "mv ${chosenEnv.basePath}/${chosenEnv.cloneDir}/fastapi/* ${chosenEnv.basePath}/${chosenEnv.appDir}/"
                    }
                }
            }
        }
        stage('Build and Start Docker Compose') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: "${chosenEnv.sshCredentialId}", keyFileVariable: 'identity')]) {
                        remote.identityFile = identity
                        sshCommand remote: remote, command: """
                            cd ${chosenEnv.basePath}/${chosenEnv.appDir}
                            docker-compose build
                        """
                        sshCommand remote: remote, command: """
                            cd ${chosenEnv.basePath}/${chosenEnv.appDir}
                            docker-compose up -d
                        """
                    }
                }
            }
        }
        stage('Show Output') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: "${chosenEnv.sshCredentialId}", keyFileVariable: 'identity')]) {
                        remote.identityFile = identity
                        sshCommand remote: remote, command: """
                            for i in {1..10}
                            do
                                curl --include http://localhost:${chosenEnv.appPort}
                                echo ''  # Newline for better readability
                            done
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                withCredentials([sshUserPrivateKey(credentialsId: "${chosenEnv.sshCredentialId}", keyFileVariable: 'identity')]) {
                    remote.identityFile = identity
                    sshCommand remote: remote, command: "rm -rf ${chosenEnv.basePath}/${chosenEnv.cloneDir}"
                }
            }
        }
    }
}

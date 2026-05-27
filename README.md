
***Docker Jenkins Pipeline***


pipeline {
    agent any

    stages {
        stage('code') {
            steps {
                git branch: 'main', url: 'https://github.com/pavan193/Docker2026.git'
            }
        }
        stage('Debug') {
            steps {
                sh '''
                    whoami
                    id
                    groups
                '''
            }
        }
        stage('build') {
            steps {
                sh 'docker build -t firstimage:v1 .'
            }
        }
        stage('deploy') {
            steps {
                sh 'docker run -d --name firstcont -p 1111:80 firstimage:v1'
            }
        }
    }
}

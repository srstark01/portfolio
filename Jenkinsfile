pipeline {
  agent {
    docker { image 'python:3' }
  }
  stages {
   stage('Build') {
      parallel {
        stage('Build') {
          steps {
            withEnv(["HOME=${env.WORKSPACE}"]) {
              sh 'pip3 install numpy pytest'
            }
          }
        }
      }
    }
   stage('Test') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'python3 -m pytest .'
        }
      }
    }
    stage('Deploy')
    {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          echo "deploying the application"
          echo "ssh ubuntu@172.17.0.1 'touch jenkinstest'"
        }
      }
    }
  }
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
    }

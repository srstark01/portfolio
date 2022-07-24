pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'echo "building the repo"'
          }
        }
      }
    }
   stage('Test') {
      steps {
        sh 'echo "Tests go here"'
      }
    }
  
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
        sh "docker-compose up -d"
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

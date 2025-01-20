pipeline {
  agent {
    docker { image 'python:3' }
  }
  stages {
   stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'pip3 install numpy pytest'
          }
        }
      }
    }
   stage('Test') {
      steps {
        sh 'python3 -m pytest .'
      }
    }
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
	sh "docker-compose up -d --build"
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

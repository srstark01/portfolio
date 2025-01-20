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
        echo "deploying the application"
      }
    }
  }
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "All Tests Passed!!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
    }

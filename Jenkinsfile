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
        sshagent(['sshkey']) {
          sh "ssh -o StrictHostKeyChecking=no -l ubuntu 10.10.2.10 'touch jenkinstest'"
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

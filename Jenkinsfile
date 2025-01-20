pipeline {
  agent any
  stages {
    stage('Build') {
       parallel {
         stage('Build') {
           steps {
             sh 'source .venv/bin/activate'
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
    stage('Deploy') {
      steps {
        echo "deploying the application"
        sh "ssh -o StrictHostKeyChecking=no ubuntu@10.10.2.10 'cd portfolio ; git pull ; sudo docker restart portfolio-web-1'"
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

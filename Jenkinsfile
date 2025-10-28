pipeline {
  agent any
  environment {
    DOCKERHUB_CRED = 'dockerhub_pat'
  }
  stages {
    stage('Docker Hub: Login test') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CRED, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker logout || true
          '''
        }
      }
    }
  }
}
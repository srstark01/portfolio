pipeline {
  agent any
  options { skipDefaultCheckout(true) }   // disable auto checkout
  environment {
    DOCKERHUB_CRED = 'dockerhub_pat'
  }

  stages {
    stage('Docker Hub: Login test') {
      when {
        expression { env.TAG?.trim() == 'latest' }   // only run when tag == "latest"
      }
      steps {
        echo "Triggered by tag: ${env.TAG}"
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

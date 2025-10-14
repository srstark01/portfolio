pipeline {
  agent any
  options { timestamps() }
  environment {
    // Provided by Generic Webhook Trigger
    DOCKER_REPO = "${env.DOCKER_REPO ?: ''}"
    DOCKER_TAG  = "${env.DOCKER_TAG  ?: 'latest'}"
  }
  stages {
    stage('Validate payload') {
      steps {
        script {
          if (!env.DOCKER_REPO?.trim()) {
            error "Missing DOCKER_REPO from webhook payload"
          }
          echo "Received image update: ${env.DOCKER_REPO}:${env.DOCKER_TAG}"
        }
      }
    }
    stage('(Optional) Pull image') {
      when { expression { return env.DOCKER_REPO?.trim() } }
      steps {
        sh '''
          docker pull ${DOCKER_REPO}:${DOCKER_TAG}
          docker inspect ${DOCKER_REPO}:${DOCKER_TAG} --format='ID={{.Id}}'
        '''
      }
    }
    // Later: add your deploy/ansible step here
  }
}

pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Show webhook payload variables') {
      steps {
        script {
          echo "DOCKER_REPO='${env.DOCKER_REPO}'"
          echo "DOCKER_TAG='${env.DOCKER_TAG}'"
          if (!env.DOCKER_REPO?.trim()) {
            error "Missing DOCKER_REPO. Check Generic Webhook Trigger JSONPath mappings."
          }
        }
      }
    }

    stage('Pull image (sanity)') {
      when { expression { return env.DOCKER_REPO?.trim() } }
      steps {
        sh '''
          TAG="${DOCKER_TAG:-latest}"
          echo "Pulling ${DOCKER_REPO}:${TAG}"
          docker pull "${DOCKER_REPO}:${TAG}"
          docker inspect "${DOCKER_REPO}:${TAG}" --format='ID={{.Id}}'
        '''
      }
    }
  }
}

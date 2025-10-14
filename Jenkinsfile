pipeline {
  agent any

  stages {
    stage('Show webhook values') {
      steps {
        echo "DOCKER_REPO=${env.DOCKER_REPO}"
        echo "DOCKER_TAG=${env.DOCKER_TAG}"
      }
    }

    stage('Pull image (sanity)') {
      when { expression { return env.DOCKER_REPO?.trim() } }
      steps {
        sh '''
          TAG="${DOCKER_TAG:-latest}"
          echo "Pulling ${DOCKER_REPO}:${TAG}"
          docker pull "${DOCKER_REPO}:${TAG}" || true
          docker inspect "${DOCKER_REPO}:${TAG}" --format='ID={{.Id}}' || true
        '''
      }
    }
  }
}

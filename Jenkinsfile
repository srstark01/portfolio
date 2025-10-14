pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Show webhook values') {
      steps {
        script {
          echo "DOCKER_REPO='${env.DOCKER_REPO}'"
          echo "DOCKER_TAG='${env.DOCKER_TAG}'"
          if (!env.DOCKER_REPO?.trim()) {
            error "Missing DOCKER_REPO (check JSONPath mappings in Generic Webhook Trigger)."
          }
        }
      }
    }

    stage('Docker sanity (non-fatal)') {
      steps {
        sh '''
          set -u
          if ! command -v docker >/dev/null 2>&1; then
            echo "Docker CLI not found on this agent; skipping pull."
            exit 0
          fi

          TAG="${DOCKER_TAG:-latest}"
          echo "Pulling ${DOCKER_REPO}:${TAG}"
          if ! docker pull "${DOCKER_REPO}:${TAG}"; then
            echo "WARNING: docker pull failed; not failing the build."
            exit 0
          fi

          docker inspect "${DOCKER_REPO}:${TAG}" --format='ID={{.Id}}' || true
        '''
      }
    }
  }
}

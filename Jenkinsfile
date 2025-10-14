pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Show webhook values') {
      steps {
        echo "DOCKER_REPO=${env.DOCKER_REPO}"
        echo "DOCKER_TAG=${env.DOCKER_TAG}"
      }
    }
  }
}

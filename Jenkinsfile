pipeline {
  agent any
  stages {
    stage('New "latest" image') {
      when {
        expression { env.TAG?.trim() == 'latest' }   // only run when tag == "latest"
      }
      steps {
        echo "Triggered by tag: ${env.TAG}"
      }
    }
    stage('New "version" image') {
      when {
        expression { env.TAG?.trim() != 'latest' }   // only run when tag == "latest"
      }
      steps {
        echo "Triggered by tag: ${env.TAG}"
      }
    }
  }
}

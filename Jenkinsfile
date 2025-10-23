pipeline {
  agent any
  environment {
    GITHUB_HTTPS_URL = 'https://github.com/srstark01/portfolio'
    DOCKERHUB_CRED   = 'dockerhub_pat'
  }
  stages {
    stage('Checkout (GitHub via HTTPS)') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],     // or '*/**'
          userRemoteConfigs: [[
            url: env.GITHUB_HTTPS_URL,
            credentialsId: env.GITHUB_CRED_ID
          ]]
        ])
        sh 'git rev-parse --short HEAD || true'
      }
    }
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

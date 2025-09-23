pipeline {
  agent any
  environment {
    GITHUB_HTTPS_URL = 'https://github.com/YOUR_ORG_OR_USER/YOUR_REPO.git'
    GITHUB_CRED_ID   = 'Github'
    DOCKERHUB_CRED   = 'Docker Hub'
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

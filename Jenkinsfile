pipeline {
  agent any

  environment {
    IMAGE     = 'srstark01/portfolio'
    CONTAINER = 'portfolio'
    PORT_MAP  = '0.0.0.0:8001:8001'
    SSH_OPTS  = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    HOSTS     = "app-001 app-002"
  }

  stages {
    stage('New "latest" image') {
      when { expression { env.TAG?.trim() == 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"
        withCredentials([sshUserPrivateKey(credentialsId: 'git-ssh-key',
                                           keyFileVariable: 'SSH_KEY',
                                           usernameVariable: 'SSH_USER')]) {
          script {
            timestamps {
              sh '''
                set -euo pipefail
                for HOST in ${HOSTS}; do
                  echo "=== Deploying to $HOST as ${SSH_USER} ==="
                  ssh -i "${SSH_KEY}" ${SSH_OPTS} "${SSH_USER}@${HOST}" bash -lc "
                    set -euo pipefail
                    whoami || true
                    id || true
                    echo 'Docker version:'; docker --version || true
                    echo 'Pulling image...'
                    docker pull ${IMAGE}:latest
                    echo 'Stopping/removing old container (if any)...'
                    docker stop ${CONTAINER} 2>/dev/null || true
                    docker rm   ${CONTAINER} 2>/dev/null || true
                    docker image prune -f
                    echo 'Starting new container...'
                    docker run -d --name ${CONTAINER} -p ${PORT_MAP} ${IMAGE}:latest
                    echo 'Verifying container...'
                    docker ps \
                      --filter name=^/${CONTAINER}$ \
                      --filter status=running \
                      --format '{{.Image}} {{.Names}}' | grep -E '^${IMAGE}:latest ${CONTAINER}$'
                  "
                  echo "=== Success on $HOST ==="
                done
              '''
            }
          }
        }
      }
    }

    stage('New "version" image') {
      when { expression { env.TAG?.trim() != 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"
      }
    }
  }
}

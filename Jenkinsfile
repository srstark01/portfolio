pipeline {
  agent any

  // tweak these as needed
  environment {
    IMAGE      = 'srstark01/portfolio'    // docker image
    CONTAINER  = 'portfolio'              // container name
    PORT_MAP   = '0.0.0.0:8001:8001'      // host:container (IPv4-only bind)
    SSH_KEY    = "${env.HOME}/.ssh/id_rsa"
    SSH_OPTS   = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    HOSTS      = "app-001 app-002"
  }

  stages {
    stage('New "latest" image') {
      when { expression { env.TAG?.trim() == 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"
        sh '''
          set -euo pipefail
          for HOST in ${HOSTS}; do
            echo "=== Deploying to $HOST ==="
            ssh -i "${SSH_KEY}" ${SSH_OPTS} opc@"$HOST" bash -lc "
              set -euo pipefail
              docker pull ${IMAGE}:latest
              docker stop ${CONTAINER} 2>/dev/null || true
              docker rm   ${CONTAINER} 2>/dev/null || true
              docker image prune -f
              docker run -d --name ${CONTAINER} -p ${PORT_MAP} ${IMAGE}:latest
              # verify running (exact name + running status + image tag)
              docker ps --filter name=^/${CONTAINER}$ --filter status=running --format '{{.Image}} {{.Names}}' | grep -E '^${IMAGE}:latest ${CONTAINER}$'
            "
            echo "=== Success on $HOST ==="
          done
        '''
      }
    }

    stage('New "version" image') {
      when { expression { env.TAG?.trim() != 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"
        // add your version-tag deploy logic here if desired
      }
    }
  }
}

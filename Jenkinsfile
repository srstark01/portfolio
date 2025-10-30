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

          echo "=== Local (Jenkins agent) debug ==="
          whoami || true
          id || true
          echo "HOME=$HOME"
          echo "Listing $HOME/.ssh"
          ls -alh "$HOME/.ssh" || true
          echo "Stat on SSH key (if present)"
          if [ -f "$SSH_KEY" ]; then
            # Linux stat syntax
            stat -c '%A %U:%G %a %n' "$SSH_KEY" 2>/dev/null || true
            # macOS/BSD fallback (won't error if not available)
            stat -f '%Sp %Su:%Sg %OLp %N' "$SSH_KEY" 2>/dev/null || true
          else
            echo "SSH key not found at $SSH_KEY"
          fi

          echo "Testing readability of key"
          if [ ! -r "$SSH_KEY" ]; then
            echo "ERROR: Jenkins user cannot read $SSH_KEY"
            exit 1
          fi

          for HOST in ${HOSTS}; do
            echo "=== Deploying to $HOST ==="
            ssh -i "${SSH_KEY}" ${SSH_OPTS} ${SSH_USER}@"$HOST" bash -lc "
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

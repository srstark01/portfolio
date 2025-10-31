pipeline {
  agent any

  environment {
    IMAGE       = 'srstark01/portfolio'
    CONTAINER   = 'portfolio'
    PORT_MAP    = '0.0.0.0:8001:8001'
    SSH_OPTS    = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

    APP_001_IP  = '10.10.3.10'
    APP_002_IP  = '10.10.3.11'

    // 👇 Define as a flat string that you’ll parse later
    TARGETS     = 'app-001=${APP_001_IP},app-002=${APP_002_IP}'
  }

  stages {
    stage('Deploy Latest Image') {
      when { expression { env.TAG?.trim() == 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"

        withCredentials([
          sshUserPrivateKey(credentialsId: 'git-ssh-key',
                            keyFileVariable: 'SSH_KEY',
                            usernameVariable: 'SSH_USER')
        ]) {
          script {
            // Parse TARGETS string -> map
            def targets = env.TARGETS.split(',').collectEntries { pair ->
              def parts = pair.split('=', 2)
              [(parts[0].trim()): parts[1].trim()]
            }

            targets.each { name, ip ->
              echo "=== Deploying to ${name} (${ip}) as ${SSH_USER} ==="
              sh """
                set -euo pipefail
                ssh -i "${SSH_KEY}" ${SSH_OPTS} "${SSH_USER}@${ip}" bash -lc '
                  set -euo pipefail
                  docker pull ${IMAGE}:latest
                  docker stop ${CONTAINER} 2>/dev/null || true
                  docker rm   ${CONTAINER} 2>/dev/null || true
                  docker image prune -f
                  docker run -d --name ${CONTAINER} -p ${PORT_MAP} ${IMAGE}:latest
                  docker ps --filter name=^/${CONTAINER}\$ --filter status=running
                '
              """
              echo "=== ✅ Success on ${name} (${ip}) ==="
            }
          }
        }
      }
    }
  }
}

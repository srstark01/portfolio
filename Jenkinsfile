pipeline {
  agent any

  environment {
    IMAGE       = 'srstark01/portfolio'
    CONTAINER   = 'portfolio'
    PORT_MAP    = '0.0.0.0:8001:8001'
    SSH_OPTS    = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

    APP_001     = '10.10.3.10'
    APP_002     = '10.10.3.11'
    STG_001     = '10.10.2.10'  

    // 👇 Define as a flat string that you’ll parse later
    APP_TARGETS     = 'app-001=${APP_001},app-002=${APP_002}'
    STG_TARGETS     = 'stg-001=${STG_001}'

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
            def targets = env.APP_TARGETS.split(',').collectEntries { pair ->
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
              echo "=== Success on ${name} (${ip}) ==="
            }
          }
        }
      }
    }
    stage('Deploy Staging Image') {
      when { expression { env.TAG?.trim() != 'latest' } }
      steps {
        echo "Triggered by tag: ${env.TAG}"

        withCredentials([
          sshUserPrivateKey(credentialsId: 'git-ssh-key',
                            keyFileVariable: 'SSH_KEY',
                            usernameVariable: 'SSH_USER')
        ]) {
          script {
            // Parse STG_TARGETS string -> map
            def targets = env.STG_TARGETS.split(',').collectEntries { pair ->
              def parts = pair.split('=', 2)
              [(parts[0].trim()): parts[1].trim()]
            }

            targets.each { name, ip ->
              echo "=== Deploying ${IMAGE}:${env.TAG} to ${name} (${ip}) as ${SSH_USER} ==="
              sh """
                set -euo pipefail
                ssh -i "${SSH_KEY}" ${SSH_OPTS} "${SSH_USER}@${ip}" bash -lc '
                  set -euo pipefail
                  echo "Pulling image..."
                  docker pull ${IMAGE}:${env.TAG}

                  echo "Stopping/removing old container (if any)..."
                  docker stop ${CONTAINER} 2>/dev/null || true
                  docker rm   ${CONTAINER} 2>/dev/null || true

                  echo "Removing old images not matching current tag..."
                  docker images ${IMAGE} --format "{{.Repository}}:{{.Tag}}" | \
                    grep -v ":${env.TAG}\$" | xargs -r docker rmi -f || true

                  echo "Starting container from ${IMAGE}:${env.TAG}..."
                  docker run -d --name ${CONTAINER} -p ${PORT_MAP} ${IMAGE}:${env.TAG}

                  echo "Verifying container..."
                  docker ps --filter name=^/${CONTAINER}\$ --filter status=running \\
                    --format "{{.Image}} {{.Names}}" | grep -E "^${IMAGE}:${env.TAG} ${CONTAINER}\$"
                '
              """
              echo "=== Success on ${name} (${ip}) ==="
            }
          }
        }
      }
    }
  }
}

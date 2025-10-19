# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install Python, Docker prerequisites, and Docker itself
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl python3 python3-pip python3-venv && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Modify the existing 'docker' group to match your host's GID (959)
# and add the 'jenkins' user to it.
RUN groupmod -g 959 docker && \
    usermod -aG docker jenkins

RUN apt update -y \
    apt install -y python3 \
    python3 --version \
    ln -s /usr/bin/python3 /usr/bin/python \
    python --version \
    apt install -y python3-pip \
    apt install -y python3-venv \
    exit 

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-cli -y
    
# Switch back to the Jenkins user
USER jenkins
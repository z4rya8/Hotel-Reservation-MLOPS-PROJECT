
# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# the command : docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind 
# the -v /var/run/docker.sock:/var/run/docker.sock
# actually just uses the host machine's docker daemon inside the container instead of installing docker inside the container
# but we will install docker inside the container to use docker-in-docker (DinD)
# this is because the docker client binary is needed to run docker commands inside the container
# When you run a command like docker build inside your Jenkins container, the following happens:
# The Jenkins job executes the docker build command.
# The docker client binary inside the Jenkins container takes this command.
# Because you mounted the host's docker.sock file, the client program sends the command to the Docker engine on the host machine.
# The host's Docker engine then builds the image and creates a new container

# Switch to root user to install dependencies
# initially it is on user jenkins
USER root

# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -g 959 -f docker && \
    usermod -aG docker jenkins

# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins
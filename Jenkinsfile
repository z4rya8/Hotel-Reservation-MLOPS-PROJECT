pipeline{
    agent any

    environment {
        VENV_DIR = "venv"
		GCP_PROJECT = "driven-actor-471620-k7"
		GCLOUD_PATH = "/var/jenkins_home/gcloud/google-cloud-sdk/bin"
		// # the hell is the above line?
		// # it is the path to the gcloud sdk in jenkins container 
		// # you can find it by running `which gcloud` in the jenkins container
		// # but the jenkins_home is a volume mounted from the host machine
		// # so you need to make sure that the gcloud sdk is installed in the host machine too
		// # you can install it by following the instructions here: https://cloud.google.com/sdk/docs/install
    }

    stages{
    	stage('Cloning Github repo to Jenkins'){
	        steps{
	        	script{
		            echo 'Cloning Github repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/z4rya8/Hotel-Reservation-MLOPS-PROJECT.git']])
		        }
	        }
	    }
        stage('Setting up our virtual environment and Installing dependencies'){
	        steps{
	        	script{
		            echo 'Setting up our virtual environment and Installing dependencies.........'
					sh '''
					python -m venv ${VENV_DIR}
					. ${VENV_DIR}/bin/activate
					pip install --upgrade pip
					pip install -r requirements.txt
					'''
		        }
	        }
	    }

        stage('Building Docker Image and Pushing to GCR'){
	        steps{
				withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
					//# is this a function in the above line?
					//# yes, it is a function that takes a list of credentials and a variable name
					//# it will create a file with the credentials and set the variable to the path of the file
					//# you can then use the variable in your shell commands
					script{
						echo 'Building Docker Image and Pushing to GCR.........'
						sh '''
						export PATH=$PATH:${GCLOUD_PATH}

						#teach me more about the above line with syntax explanation
						# the above line is adding the gcloud sdk path to the PATH environment variable
						# so that we can use the gcloud command in the shell

						gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

						# Your personal Gmail account is for you, a human, to log into the Google Cloud console and click around. A service account, on the other hand, is a special non-human account designed for applications and scripts (like Jenkins) to authenticate and use GCP services. It's like giving your Jenkins pipeline its own robot identity. 🤖
						# The command gcloud auth activate-service-account is like the robot swiping its ID card. It uses the secret key file you provided to officially log in to Google Cloud as that service account. From this point forward, any gcloud command run in this script will be performed by that identity.
						# how is the above command working?
						# the above command is using the gcloud sdk to authenticate with the service account
						# using the key file that we created with the credentials
						# this will allow us to push the docker image to the gcr

						gcloud config set project = ${GCP_PROJECT}

						gcloud auth cofigure-docker --quiet

						# why did we use the above command?
						# the above command is configuring our local docker to use the gcloud sdk as a credential helper
						# this will allow us to push the docker image to the gcr
						# without having to login to the gcr manually
						# now our docker is authenticated with gcr
						# so when we run docker push, it will use the gcloud sdk to authenticate
						# instead of asking us to login manually
						# and can push the image directly to gcr
						# --quiet is used to disable all interactive prompts


						docker build -t gcr.io/${GCP_PROJECT}/ml-project-1:latest .

						docker push gcr.io/${GCP_PROJECT}/ml-project-1:latest


						'''
		        	}
			    }
	   		}
		}
	}
}
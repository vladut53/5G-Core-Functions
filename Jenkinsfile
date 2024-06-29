pipeline {
  agent any
  stages {
    stage('Docker Newman container creation') {
      steps {
        sh 'docker run --rm postman/newman run -h'
      }
    }

    stage('NRF Functions Register') {
      steps {
        sh 'docker run --rm -v "${WORKSPACE}:/etc/newman" --workdir /etc/newman postman/newman run /etc/newman/PostmanMsg/NRF_NF_REGISTER.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('SMF Target Routes') {
      steps {
        sh 'docker run --rm -v "${WORKSPACE}:/etc/newman" --workdir /etc/newman postman/newman run /etc/newman/PostmanMsg/SMF-Routes.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('AMF Register Users') {
      steps {
        sh 'docker run --rm -v "${WORKSPACE}:/etc/newman" --workdir /etc/newman postman/newman run /etc/newman/PostmanMsg/AMF-USERS.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('AMF Users access SMF') {
      steps {
        sh 'docker run --rm -v "${WORKSPACE}:/etc/newman" --workdir /etc/newman postman/newman run /etc/newman/PostmanMsg/USERS-ACCESS-SMF.postman_collection.json --color off --disable-unicode'
      }
    }
  }
}

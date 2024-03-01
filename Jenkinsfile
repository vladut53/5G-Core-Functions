pipeline {
  agent any
  stages {
    stage('NRF Functions Register') {
      steps {
        sh 'docker run -t postman/newman run -h'
        sh 'docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run NRF_NF_REGISTER.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('SMF Route to sites') {
      steps {
        sh 'docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run SMF-Routes.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('AMF Register Users') {
      steps {
        sh 'docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run AMF-USERS.postman_collection.json --color off --disable-unicode'
      }
    }
    
    stage('AMF Users access SMF') {
      steps {
        sh 'docker run -v ${WORKSPACE}:/etc/newman --workdir /etc/newman -t postman/newman run USERS-ACCESS-SMF.postman_collection.json --color off --disable-unicode'
      }
    }
  }
}

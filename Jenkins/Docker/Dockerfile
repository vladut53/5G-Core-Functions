FROM jenkins/jenkins:lts

MAINTAINER Vladut ILIE  

USER root

RUN apt-get -y update; apt-get install -y sudo; apt-get install -y git wget

RUN echo "Jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

RUN wget http://get.docker.com/builds/Linux/x86_64/docker-latest.tgz

RUN tar -xvzf docker-latest.tgz

RUN mv docker/* /usr/bin/

# USER jenkins

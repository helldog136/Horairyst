#
# Horairyst Dockerfile
#

# Pull base image.
FROM ubuntu:14.04


MAINTAINER Duncan De Weireld <duncan.deweireld@student.umons.ac.be>


# Set environment variables.
ENV HOME /root

# Add files.
ADD root/.bashrc /root/.bashrc
ADD root/.gitconfig /root/.gitconfig
ADD root/.scripts /root/.scripts

RUN mkdir /home/scip
#COPY scipoptsuite-3.2.1.tgz /home/scip
COPY scip /home/scip

# Install.
# if network fails http://stackoverflow.com/questions/24991136/docker-build-could-not-resolve-archive-ubuntu-com-apt-get-fails-to-install-a
# nmcli d list | grep 'IP4.DNS'
# add the 2 DNS to /etc/default/docker

#RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update && \
    apt-get install -y build-essential \
    python3 \
    nano \
    libgmp3-dev \
    libreadline6 \
    libreadline6-dev \
    zlib1g-dev \
    libncurses5-dev \
    bison \
    flex \
    python3-pip \
    git
RUN rm -rf /var/lib/apt/lists/*


RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
ADD sshKeys/id_rsa2 /root/.ssh/id_rsa

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN git clone git@github.com:helldog136/Horairyst.git /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Install scip
#RUN cd /home/scip && tar  -zxvf scipoptsuite-3.2.1.tgz
#WORKDIR /home/scip/scipoptsuite-3.2.1
#RUN make SHARED=true scipoptlib
#ENV PATH /home/scip/scipoptsuite-3.2.1/scip-3.2.1/bin:$PATH

EXPOSE 4721 4721

ENTRYPOINT ["python3"]
CMD ["main.py"]
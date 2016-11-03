#
# Horairyst Dockerfile
#

# Pull base image.
FROM python:3.4


MAINTAINER Duncan De Weireld <duncan.deweireld@student.umons.ac.be>
# Install.
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y nano
RUN apt-get install -y libgmp3-dev libreadline6 libreadline6-dev  zlib1g-dev libncurses5-dev bison flex
RUN mkdir /home/scip
COPY scipoptsuite-3.2.1.tgz /home/scip
RUN rm -rf /var/lib/apt/lists/*

# Add files.
ADD root/.bashrc /root/.bashrc
ADD root/.gitconfig /root/.gitconfig
ADD root/.scripts /root/.scripts

ADD horairyst /
ADD entrypoint.sh /

# Install scip
RUN cd /home/scip && tar  -zxvf scipoptsuite-3.2.1.tgz
WORKDIR /home/scip/scipoptsuite-3.2.1
RUN make SHARED=true scipoptlib
ENV PATH /home/scip/scipoptsuite-3.2.1/scip-3.2.1/bin:$PATH

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

ENTRYPOINT /entrypoint.sh
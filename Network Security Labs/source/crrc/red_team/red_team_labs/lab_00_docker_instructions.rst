===========================
Lab 0 - Docker Instructions
===========================
--------
Overview 
--------

Setting up Docker in Kali. A few of the following commands wrap lines so
make sure to get the entire command. Some of the commands also will not
copy and paste correctly out of the document like dashes and quotes.
Make sure to retype those in the virtual machine.

1. Add docker repos

::

    curl -fsSL https://download.docker.com/linux/debian/gpg \| sudo apt-key
    add –

    echo 'deb https://download.docker.com/linux/debian stretch stable' >    
    /etc/apt/sources.list.d/docker.list

2. Fetch updated repo info

::

    apt update

3. Install and run docker

::

    apt install -y docker-ce

    systemctl start docker

4. Install and run Metasploitable container

::

    docker run -it tleemcjr/metasploitable2:latest sh -c "/bin/services.sh
    && bash”

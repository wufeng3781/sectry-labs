.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

====
VPN
====


Introduction
-------------

**Overview:** Virtual Private Network (VPN) and its enabling technologies have been widely used for both secure remote access and evading firewall control. 
This lab module focuses on SSL based VPN such as OpenVPN and introduces the setup and operation of SSL VPN.

In this lab, students will learn the basic concepts of VPN. 
Moreover, students will lear how to configure the VPN server and client through deploying and setting up OpenVPN on server and client, respectively. 
At the end of this lab, students will use the created OpenVPN to access a web server in a private network.

**Objectives:** This material in this lab aligns with the following objectives:

* Understand the basic concepts of OpenVPN
* Set up an OpenVPN server and configure the OpenVPN client
* Access the private subnet behind the server

**Required Knowledge:** Students are required to have the following prerequisite knowledge for this lab:

* Familiar with the Linux system.
* The usage of the Linux terminal and basic Linux commands.
* Understand the basic concepts of a VPN and firewall.

**Background:**

  |Description| 
  
  For more information about |Platform|, please see bundled `user manual file`_.
 
  **Secure Shell(SSH)** is a network protocol that allows data to be exchanged over a secure channel between two computers. 
  Encryption provides confidentiality and integrity of data. 
  SSH uses public-key cryptography to authenticate the remote computer and allow the remote computer to authenticate the user, if necessary. 
  
  For more information about SSH Tutorial, please see `<https://wiki.archlinux.org/index.php/Secure_Shell>`_.
 
  **OpenVPN** is a free and open-source software application that implements virtual private network (VPN) techniques to create secure point-to-point or site-to-site connections in routed or bridged configurations and remote access facilities. 
  
  For more information about OpenVPN, please see `<https://openvpn.net/>`_.

**Environment:**

Students should be able to view and access this lab on EZSetup, which is a tool for easily deploying NetSiC labs including this one on a public or private computing cloud. In this lab, students can access three instances on OpenStack: vpn-client, vpn-server, and web-server. The detailed configuration of these three instances is provided in the below **Table 1**.

.. list-table:: **Table 1** VM properties and access information
   :header-rows: 1

   * - Name
     - Image
     - RAM
     - VCPU
     - Disk
     - Login Account
   * - vpn-client
     - Ubuntu 16.04 x64
     - 2GB
     - 2
     - 20GB
     - See |Platform|
   * - vpn-server
     - Ubuntu 16.04 x64
     - 2GB
     - 2
     - 20GB
     - See |Platform|
   * - web-server
     - web-server
     - 2GB
     - 2
     - 20GB
     - See |Platform|

The network topology for this lab looks as shown below in `Figure 1`_.

.. _Figure 1:

.. figure:: /xie/media/vpn_media/lab/fig_1.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 1** Lab Network topology

In this lab, we require two software: (1) OpenVPN (2) Apache2 Web Server. 
OpenVPN is a full-featured open-source Secure Socket Layer (SSL) VPN solution that accommodates a wide range of configurations. 
Sometimes, we use it to traverse untrusted networks privately and securely as if you were on a private network, while we will use this feature to access a web server on a private network in this lab. 
Apache2 Web Server is the most popular used Web server on Linux systems. 
Web servers are used to serve Web pages requested by client computers. 
In this lab, we will use it to set up a simple Web page which is provided for vpn-client instance to access.
We will install OpenVPN in the vpn-server and vpn-client instances. 
Apache2 Web Server was pre-built into the web-server instance.

Also, in this lab, we create two networks: (1) Private network (2) Untrusted network. 
The private network serves the web-server and vpn-server instances. 
For the Untrusted network, it’s just like free Wi-Fi in a mall or airport, which connects with the vpn-client instance. 
Each of these three instances has a public IP that helps instances to be accessed from the outside world.

Each student will get a specific slice (a collection of resources that run in an isolated environment) of this lab, therefore many students can work on this lab each with his/her own unique practice environment. 
This ensures that each one can work separately without the need to worry about his/her own work being interfered by other users’ operation.

Task 1: OpenVPN Server Configuration
------------------------------------

In this task, students will SSH to the VPN server instance and configure the OpenVPN server-side including three subtasks: generating the server certificate and keys, editing the server configuration file, and adjusting the server networking configuration.

Task 1.1: Generating Server Certificates and Keys
#################################################

Firstly, we need to install OpenVPN. ::

	$ sudo apt install openvpn

After that, install the easy-rsa package that helps us generate the SSL key pairs. ::

	$ sudo apt install easy-rsa

Copy the easy-rsa template directory into the home directory with the ``make-cadir`` command. ::

	$ make-cadir ~/openvpn-ca

Then, move into the ``openvpn-ca`` directory and modify the value of CA in ``vars`` file. ::

	$ cd ~/openvpn-ca
	$ vim vars     

First, we need to specify the right SSL configuration file for the variable ``KEY_CONFIG`` as below: ::

	export KEY_CONFIG="$EASY_RSA/openssl-1.0.0.cnf"

.. admonition:: Observe

	Take note of the double quotations around the SSL configuration file name above. 
	By default, you will see single quotations which will cause errors if not changed.

The content below has default values, which should be edited depending on your preference. ::

	export KEY_COUNTRY="US"
	export KEY_PROVINCE="CA"
	export KEY_CITY="SanFrancisco"
	export KEY_ORG="Fort-Funston"
	export KEY_EMAIL="me@myhost.mydomain"
	export KEY_OU="MyOrganizationalUnit"

We will also edit the ``KEY_NAME`` value just below this section. 
To keep this simple, we will call it ``server``: ::

	export KEY_NAME="server"

When you are finished, save and quit using ``ESC`` then ``:wq!`` if you chose to use VIM text editor.

Afterwards, we can use the variables we set and easy-rsa utilities to build our certificate authority. 
We need to source the vars file. ::

	$ source vars

Then, clean the ``~/openvpn-ca/keys`` directory and build certificate authority by the commands below. ::

	$ ./clean-all
	$ ./build-ca

You will be prompted to set the CA. 
Just press ``Enter`` to confirm the selection because we already filled out the values in vars file. 
When we finished it, we will have a CA that can be used to create certificates we need.

Now, let us generate server certificates and key pair following the command below. ::

	$ ./build-key-server server

Press ``Enter`` to accept the default value for the following prompts. 
You do not need to enter a challenge password for this setup. 
In the end, you will have to enter ``y`` to two questions to sign and commit the certificate.

We will generate a strong Diffie-Hellman keys to use during key exchange by typing: ::

	$ ./build-dh

Grab a coffee or tea because it will take several minutes to complete.

After that, generate an HMAC signature to strengthen the server’s TLS integrity verification capabilities. ::

	$ openvpn --genkey --secret keys/ta.key


Tasl 1.2: Editing the Server Configuration File
###############################################

OpenVPN sets up two connections: the control channel and the data channel. 
The control channel is a low bandwidth channel, over which, e.g., network parameters and key material for the data channel is exchanged. 
OpenVPN uses TLS to protect control channel packets. 
The data channel is the channel over which the actual VPN traffic is sent. 
This channel is keyed with key material exchanged over the control channel.

To complete these two connections, let us do the following steps and edit the server configuration file.  
Now, move into the ``~/openvpn-ca/keys`` directory and then copy CA cert, server cert, server key, the HMAC signature and the Diffie-Hellman files to the ``/etc/openvpn`` configuration directory. ::

	$ cd ~/openvpn-ca/keys
	$ sudo cp ca.crt server.crt server.key ta.key dh2048.pem /etc/openvpn

Then, we need to unzip and copy a sample OpenVPN configuration file into configuration directory to configure the server. ::

	$ gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz | sudo tee /etc/openvpn/server.conf

Now, let us open the configuration file and modify it. ::
	
	$ sudo vim /etc/openvpn/server.conf

In the ``server.conf`` file, find the route section by looking for the push directive. Remove the ``;`` to uncomment the push line and modify the private subnet behind the server. ::

	push “route 172.20.0.0 255.255.255.0”

Then, find HMAC section by looking for tls-auth command. 
Remove the ``;`` to uncomment the tls-auth line, which adds an additional layer of HMAC authentication on top of the TLS control channel to mitigate DOS attacks and attack on the TLS stack. 
Below this, set the value of key-direction to 0. 
Because the value of key-direction is 0 in server-side, we will set the value of key-direction to 1 in client-side. ::

	tls-auth ta.key 0

Next, find the section on cryptographic ciphers by finding the cipher ``AES-256-CBC`` line, which encrypts data channel packets with cipher algorithm ``AES-256-CBC``. 
Below this, add an auth line to select ``SHA256`` to authenticate data channel. ::

	cipher AES-256-CBC
	auth SHA256

Finally, find user and group setting and remove the ``;`` to uncomment these lines so that OpenVPN run as the unprivileged ``nobody`` user rather than root. ::

	user nobody
	group nogroup

When you are finished, save and close the file.

Task 1.3: Adjusting the Server Networking Configuration
#######################################################

On the one hand, we need to allow the server to forward the traffic so that the client can reach the instance on the private network besides vpn-server instance. 
We can check whether the value of ``net.ipv4.ip_forward`` equal to 1 following the command below. ::

	$ sudo sysctl -p

On the other hand, we need to use UFW to manipulate the traffic coming into the server. 
Let us open the ``before.rules`` in the ``/etc/ufw`` directory to add some masquerading rules, which set the default policy for the POSTROUTING chain in the nat table and masquerade any traffic coming from the VPN. ::

	$ sudo vim /etc/ufw/before.rules

At the top of the file, put the content below into the place before the conventional UFW rules are loaded. ::

	# START OPENVPN RULES
	# NAT table rules
	*nat
	:POSTROUTING ACCEPT [0:0] 
	# Allow traffic from OpenVPN client to ens3
	-A POSTROUTING -s 10.8.0.0/8 -o ens3 -j MASQUERADE
	COMMIT
	# END OPENVPN RULES

Save and close the file when you are finished.

Opening the UFW file in the ``/etc/default`` directory, we need to set the value of ``DEFAULT_FORWARD_POLICY`` from ``DROP`` to ``ACCEPT``, which allow forwarded packets by default. ::

	$ sudo vim /etc/default/ufw
	DEFAULT_FORWARD_POLICY="ACCEPT"

Save and close the file when you are finished	.

Next, we need to open up UDP traffic to the port 1194, and allow SSH and VNC traffic through port 22 and 6080. ::

	$ sudo ufw allow 1194/udp
	$ sudo ufw allow 22/tcp
	$ sudo ufw allow 6080/tcp

Now, we should disable and re-enable UFW to load the changes from all of the files we have edited. ::

	$ sudo ufw disable
	$ sudo ufw enable

.. note:: At this point, you will no longer be able to use NoVNC to connect to the VM. SSH will be required moving forward.

We need to start the OpenVPN server by specifying our configuration file name as an instance variable after the system unit file name. ::

	$ sudo systemctl start openvpn@server

Check whether the server has started successfully by the following command. ::

	$ sudo systemctl status openvpn@server

Enable the service so that it starts automatically at boot. ::
	
	$ sudo systemctl enable openvpn@server


Lab Exercise 1
~~~~~~~~~~~~~~

When answering the following questions, you should take screenshots and indicate where in the message you’ve found the information that answers the following questions. 
When you hand in your tasks, annotate the output so that it’s clear where in the output you’re getting the information for your answer:

1.	Check the network interfaces by ``ifconfig`` command, what is the different before and after starting the openvpn server.

2.	When you have started the openvpn server, can you take a screenshot of the result after you execute the ``sudo systemctl status openvpn@server`` command?


Task 2: OpenVPN Client Configuration 
------------------------------------

In task 2, students will learn how to generate the client certification and key pair. Moreover, students need to know how to adjust the client configuration file.

Task 2.1: Generating Client Certification 
#########################################

Now, let use generate the client certification and key pair on the server instance for the sake of simplicity. We need to move into the ``openvpn-ca`` directory and re-source the vars file. ::

	$ cd ~/openvpn-ca
	$ source vars

Then, we use the client as the value for our certificate and key pair by typing: ::

	$ ./build-key client 

Hit ``Enter`` to fill out the defaults, when you meet the following prompts. Leave the challenge password blank and make sure to enter ``y`` for the prompts that ask whether to sign and commit the certificate.

Create a new directory for collecting the client configuration files by following commands. ::

	$ mkdir ~/client-configs

Navigate to ``~/openvpn-ca/keys`` and copy ``CA cert``, ``client cert`` and ``key``, and the HMAC signature files to the ``~/client-configs`` directory. ::

	$ cd ~/openvpn-ca/keys 
	$ cp client.crt client.key ta.key ca.crt ~/client-configs

Task 2.2: Editing the Client Configuration File
###############################################

Copy an example client configuration file into the client-configs directory to use as our client configuration by running the command below. ::

	$ cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/client.conf
	
Opening the ``client.conf`` file, you need to add and modify some lines. ::

	$ vim ~/client-configs/client.conf

First, find the remote directive. 
This points the client our OpenVPN server address, which should be the public IP address of OpenVPN server. ::

	remote server_public_IP_address 1194

Uncomment the user and group directives by removing the ``;``. ::
	
	user nobody
	group nogroup
	
Then, find HMAC section by looking for tls-auth command. 
Remove the ``;`` to uncomment the tls-auth line. 
Below this, we need to add the key-direction directive and set the value to 1 so that client-side can work with the server-side. ::

	tls-auth ta.key 1

.. note:: This may already be uncommented.

Find the cipher section. 
You need to add auth line after cipher. ::
	
	cipher AES-256-CBC
	auth SHA256

When you finished it, save and close this file.

Task 3: Access OpenVPN Server from Client
-----------------------------------------

In this task, students will connect to the OpenVPN server from the vpn-client so that the vpn-client instance can access the private network.

At the beginning, we need to SSH to the vpn-client instance, and install openvpn. ::

	$ sudo apt install openvpn

Then you can use SFTP (SSH file transfer protocol) command to transport the client-configs directory from the server side to client side. ::

	$ sftp -r ubuntu@<server_public_ip>:client-configs ~/

When you have downloaded this directory, move into the ``~/client-config`` directory. ::
	
	$ cd ~/client-configs

Now, you can connect to the VPN by just pointing the openvpn command to the client configuration file. ::

	$ sudo openvpn client.conf &

Let us ``curl`` the IP address of the web-server instance. ::
	
	$ curl 172.20.0.6:6677

Lab Exercise 2
##############

When answering the following questions, you should take screenshots and explain where in the message you’ve found the information that answers the following questions. 
When you hand in your tasks, annotate the output so that it’s clear where in the output you’re getting the information for your answer:

1.	What is the result after you curl the IP address of web-server?

2.	Can you ping the IP address of web-server instance from the vpn-client instance and dump the ICMP traffic on your vpn-server instance? What do you find? Why?


What To Sumbit
--------------

Save your answers (with screenshots) to the above questions into a PDF file and name the file as ``vpn-ans.pdf``.
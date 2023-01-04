.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

===========================
Network Intrusion Detection
===========================

Introduction
-------------

**Description:** Network intrusion detection is a critical component of network defense. 
Through effective network intrusion detection, malicious activities and policy violations can be monitored and identified. 
In general, Network intrusion detection system (NIDS) can be classified into two types, signature-based detection, and anomaly-based detection.
The former one detects intrusions by matching network patterns with predefined rules, and the latter one detects deviations from a model of "good" traffic. 
In this lab, students will learn how to use the signature-based detection.

**Lab Objectives:** Upon completing this lab, students should be able to:

* Understand the working mechanisms of two popular open source network intrusion detection systems, Snort and Bro
* Install and configure Snort and Bro packages
* Understand the difference between these two popular NIDS
* Write Snort and Bro rules to detect HTTP brute-force-attck

**Reqiured Knowledge:** Students are required to have the following prerequisite knowledge for this lab:

* Familiar with the Linux system
* Basic use of the Linux terminal and Linux commands
* Familiar with the basic concepts of network security.

**Background:**

  |Description|
  
  For more information about |Platform|, please see bundled `user manual file`_.
 
  **Secure Shell(SSH)** is a network protocol that allows data to be exchanged over a secure channel between two computers. 
  Encryption provides confidentiality and integrity of data. 
  SSH uses public-key cryptography to authenticate the remote computer and allow the remote computer to authenticate the user, if necessary.
  
  For more information about SSH, please see https://wiki.archlinux.org/index.php/Secure_Shell
 
  **Bro** is a passive, open-source network traffic analyzer. 
  It is primarily a security monitor that inspects all traffic on a link in depth for signs of suspicious activity. 
  More generally, however, Bro supports a wide range of traffic analysis tasks even outside of the security domain, including performance measurements and helping with trouble-shooting. 
  
  For more information about Bro Tutorial, please see `<https://www.bro.org/>`_.
 
  **Snort** is an open source intrusion prevention system offered by Cisco. 
  It is capable of real-time traffic analysis and packet logging on IP networks. 
  It can perform protocol analysis, content searching/matching, and can be used to detect a variety of attacks and probes, such as buffer overflows, stealth port scans, CGI attacks, SMB probes, OS fingerprinting attempts, and much more. 
  
  For more information about Snort, please see `<https://snort.org/>`_.
 
  **Wireshark** is a free and open-source packet analyzer. 
  It is used for network troubleshooting, analysis, software and communications protocol development, and education. 
  Wireshark is very similar to tcpdump, but has a graphical front-end, plus some integrated sorting and filtering options. 
  
  For more information about Wireshark, please see its User\'s Manual:`<https://www.wireshark.org/docs/wsug_html_chunked/>`_
 
  **Vim** is a highly configurable text editor built to enable efficient text editing. 
  It is an improved version of the vi editor distributed with most UNIX systems. 
  Vim is often called a "programmer's editor," and so useful for programming that many consider it an entire IDE. 
  It's not just for programmers, though. 
  
  For more information on Vim, please see   `<https://en.wikipedia.org/wiki/Vim_(text_editor)>`_.
 
  **Enviornment:** In this lab, students can access two virtual machines (VM) in the cloud from |Platform|. 
  One acts as an attacker that is equipped with an Nmap scanner, and the other works as a victim. 
  The victim VM is installed with an Apache web server as well as two NIDS, Snort and Bro, which are used for detecting network attacks against the web server. 
  The access information about these two virtual machines is provided below in **Table 1**. 
  Please refer to the EZSetup dashboard for the actual public IP addresses and passwords. 
  The network topology for this lab is provided below in **Figure 1**.


.. list-table:: **Table 1** VM properties and access information
   :header-rows: 1

   * - Name
     - Image
     - RAM
     - VCPU
     - Disk
     - Login Account
   * - Attacker
     - nids-attacker
     - 2 GB
     - 1
     - 20 GB
     - See |Platform|
   * - Victim
     - nids-victim
     - 2 GB
     - 1
     - 20 GB
     - See |Platform|

.. figure:: /xie/media/network_media/lab/enviornment.png
	:alt: alternate text
	:figclass: align-center

	**Figure 1** Lab Network topology


Task 1: Bro NIDS
----------------

Bro is an open-source network traffic analyzer, which is primarily a security monitor that inspects all traffic on a link in depth for signs of suspicious activities. 
Bro supports a wide range of traffic analysis tasks even outside of the security domain. 
The most immediate benefit that a site gains from deploying Bro is an extensive set of log files that record a network’s activity in high-level terms. 
These logs include not only a comprehensive record of every connection seen on the wire but also application-layer transcripts. 
Bro provides users with a domain-specific, Turing-complete scripting language for expressing arbitrary analysis task.

.. figure:: /xie/media/network_media/lab/figure2.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 2** Architecture of Bro and packet processing flow

Bro is made of two major components as shown in **Figure 2**. 
The event engine reduces the incoming packet stream into a series of higher-level events. 
These events reflect the network activity in policy-neutral terms. 
Script interpreter is Bro’s second main component, which executes a set of event handlers written in Bro’s custom scripting language. 
These scripts can express a site’s security policy, generate real-time alerts and execute arbitrary external programs on demand.


Lab Exercise 1
~~~~~~~~~~~~~~

 1. Basic operation with Bro: Login to the Victim VM and change to root privilege by entering ``sudo su``, and then launch BroControl shell by typing ``broctl``. 
 Enter the following commands in the shell: ``deploy``, ``status``. 
 Take a screenshot for each result returned by the above commands
 
  .. note:: You may need to wait for a minute or two before getting the result of the deploy command.
 
 2. Check the policies that have been installed in the Bro configuration. Take a screenshot of the policies.
 
  .. admonition:: Hint
 
	Check this log file ``/opt/bro/logs/current/loaded_scripts.log``



Task 2: Snort NIDS
------------------

Snort is an open-source NIDS that is able to perform real-time traffic analysis and packet logging. 
It performs protocol analysis, content searching and content matching. 
The program can also be used to detect probes or attacks. Snort has three main modes: sniffer, packet logger, and network intrusion detection. 
In sniffer mode, Snort captures the network packets and displays them on a console. 
In packet logger mode, Snort logs packets to the disk. 
In intrusion detection mode, Snort monitors network traffic and analyzes it against a rule set defined by the user and then performs a specific action based on what has been identified.

.. figure:: /xie/media/network_media/lab/figure3.png
		:alt: alternate text
		:figclass: align-center

		**Figure 3** Architecture of Snort and packet processing flow
		
Snort is logically divided into multiple components as shown in **Figure 3**. These components work together to detect specific attacks and to generate output in a required format from the detection system. The four major components of Snort’s architecture are listed as below:

 #. **Sniffer**: The sniffer can collect packets from real-time network traffic covering the different types of network interfaces and prepare the raw packets to be sent to preprocessors.

 #. **Preprocessors**: The preprocessor deals with the raw packet from the sniffer and checks them against certain plugins which determine what kind of packets or what kind of behavior is Snort dealing with. After that, the processors will send packets with a particular type of behavior defined in the plugins to the detection engine.

 #. **Detection Engine**: The detection engine is the most important part of signature-based IDS in Snort. It will compare every packet with each rule from a predefined rule set and sends the packets that match any rules to the output. If the packets do not match any rules, they will be dropped.

 #. **Output**: It generates alerts and log messages depending upon the action rule that is defined in the detection engine.

A Snort rule consists of two parts, as shown in **Figure 4**:

 * **Rule header**: 
    * Rule’s action (log or alert) 
    * Protocol (TCP, UDP, ICMP, and IP) 
    * Source / Destination IP address 
    * Netmasks, and the 
    * Source / Destination ports information
 * **Rule options**: The rule options are optional.

.. figure:: /xie/media/network_media/lab/figure4.png
	:alt: alternate text
	:figclass: align-center

	**Figure 3** The Snort rule format

Lab Exercise 2
~~~~~~~~~~~~~~

#. Verify that Snort has been properly installed: change to root privilege by entering ``sudo su``, and then type command ``snort -V`` to get the version of the Snort installed on the victim machine. A screenshot is needed to show you have finished this task.



Task 3: HTTP Brute-Force Attack
-------------------------------

**Concept:** Before understanding the concept of HTTP brute-force attack, we should know the concept of brute force attack.
This attack can manifest itself in many different ways, but primarily consists of an attacker configuring predetermined values, making requests to a server using those values, and then analyzing the response. 
For the sake of efficiency, an attacker may use a dictionary attack.

One of the most common methods of HTTP access authentication is basic access authentication, which requests clients identify themselves with a login name and password. 
For the HTTP brute-force attack, the attacker will try a massive combination of login names and passwords. 
If the credentials are valid, the server sends the requested content. 
Otherwise, the server responds with HTTP status code 401.

**Tool - Nmap:** Nmap (Network Mapper) is a security scanner, which is used to discover hosts and services on a computer network, thus building a "map" of the network. To accomplish its goal, Nmap sends specially crafted packets to the target host(s) and then analyzes the responses. The software provides a number of features for probing computer networks, including host discovery and service and operating-system detection. These features are extensible by scripts that provide more advanced service detection, vulnerability detection, and other features. In this experiment, we use the script of http-brute, which performs brute force password auditing against HTTP basic authentication.

.. note:: Lab Exercise 3 below assumes you use VNC link to access the victim VM


Lab Exercise 3
~~~~~~~~~~~~~~

 #. On the victim VM, first, make sure the apache web server is running by entering ``service apache2 status`` in a terminal window, and then type ``firefox`` to launch the browser. Type `<http://localhost>`_ in the URL field to bring up the website hosted on the victim VM. In the pop-up authentication window, enter web as the username and password as the password, and then click ``OK`` button. Take a screenshot of the web page displayed.
 
 #. On the victim VM, launch Wireshark by typing ``sudo wireshark-gtk`` in a terminal window, and then select :font:`ens3` as the interface to capture traffic from and click start to begin. On the attacker VM, enter the command below: ::
 
	$ nmap --script http-brute -p 80 192.168.1.20
 
  Wait until nmap finishes, what is the output of nmap? What do you see from the HTTP traffic captured by the Wireshark?
  
  .. admonition:: Hint 
	
	Type ``http`` in the filter window.
  

Task 4: Detection Using Bro
---------------------------

The HTTP brute-force attack can be detected by analyzing the Bro log file ``http.log`` which logs request/response pairs and all relevant metadata. ``http.log`` is in the ``/opt/bro/logs/current`` directory. There are many lines in the log showing that attacker (192.168.1.10) failed to log in the webpage hosted on the victim (192.168.1.20). **Figure 5** shows a portion of the log file. The **administrator** is an account that the nmap brute-force attack tries.

.. figure:: /xie/media/network_media/lab/figure5.png
	:alt: alternate text
	:figclass: align-center

	**Figure 5** A log entry of ``http.log`` file

To enable Bro’s automatic detection of HTTP brute-force attack, we can add a detection script (``detect-bruteforce.bro`` located in ``/opt/bro/share/bro/policy/protocols/http``) and load it into Bro. If Bro detects such an attack, it will create alerts in a log file named ``notice.log``, which records specific activities that Bro recognizes as potentially interesting, odd, or bad.

To use ``detect-bruteforce.bro`` script to detect the HTTP brute-force attack (i.e., too many rejected usernames and passwords occurring from unauthorized requests), we define a new notice type **HTTP_Auth_Bruteforce_Attack**, a threshold for the number of attempts (**30**) and a monitoring interval (**1 minute**).

.. figure:: /xie/media/network_media/lab/figure6.png
	:alt: alternate text
	:figclass: align-center

	**Figure 6** Define a new notice type in Bro HTTP policy
	
Using the ``http_reply`` event, we check whether the HTTP status code is 401. If so, we use the Summary Statistics (SumStats) Framework to keep track of the number of failed attempts.

.. figure:: /xie/media/network_media/lab/figure7.png
	:alt: alternate text
	:figclass: align-center

	**Figure 7** Observe failed HTTP authentication response in SumStats

We use the SumStats framework to produce a notice of attack when the number of attempts without valid credentials exceeds the specified threshold during a measuring interval. The function ``threshold_crossed`` in **Figure 8** below is a callback that is called when a threshold has been crossed. If the number of attempts is over 30 within 1 minute, a notice will be generated in ``notice.log``.

.. figure:: /xie/media/network_media/lab/figure8.png
	:alt: alternate text
	:figclass: align-center

	**Figure 8** Use SumStats framework to produce attack notice

Next, move ``detect-bruteforce.bro`` file into ``/opt/bro/share/bro/policy/protocols/http`` directory, and also add ``/opt/bro/share/bro/policy/protocols/http/detect-bruteforce.bro`` in the config file ``/opt/bro/share/bro/site/local.bro``. After that, go to BroControl by entering the command ``broctl`` with root privilege in a terminal window. In the BroControl shell, enter deploy to install the new rule. 


Lab Exercise 4
~~~~~~~~~~~~~~

 #. On the attacker VM, launch the attack by entering the following command. ::
 
	$ nmap --script http-brute -p 80 192.168.1.20
 
  On the victim VM, wait for a few minutes, and check if there is a ``notice.log`` file in the ``/opt/bro/logs/current`` directory. If yes, check the content of the file and take a screenshot.
  
  

Task 5: Detection Using Snort
-----------------------------

We need to create a rule file named ``local.rules`` in ``/etc/snort/rules folder`` on the victim machine. 
The rule to put inside the ``local.rules`` is shown below, which is used to detect HTTP brute-force attacks:

Using the command below will allow you to edit this file. ::

	$ vim local.rules

.. figure:: /xie/media/network_media/lab/figure9.png
	:alt: alternate text
	:figclass: align-center

	**Figure 9** A Snort rule for detecting HTTP brute-force attacks

* The *msg* keyword includes the message that will be displayed once HTTP brute-force attack is detected.

* The *content* keyword can search for content with “401” that is an error status response code in the packet payload and trigger response based on that data.

* The *threshold* keyword means that this rule logs 30th event on this sid during a 60-second interval. After an event is logged, a new time period starts for type threshold.

* The *track by_dst* keyword means track by destination IP.

* The *count* keyword means count number of events.

* The *seconds* keyword means time period over which the count is accrued.

* The *sid* keyword is used to uniquely identify Snort rules.

* The *rev* keyword is used to uniquely identify revision of Snort rules

The ``local.rules`` file has to be included in ``/etc/snort/snort.conf`` ::

	include $RULE_PATH/local.rules

You can include this rule by opening ``snort.conf`` through vim and adding the line of text above.

.. admonition:: Important!

   Before starting Snort, TX (packets transmitted out the interface) checksum offload has to be disabled on the NIC by typing... ::

      $ sudo ethtool -K ens3 tx off

Then start Snort program and run it in background with the following command. ::

	$ sudo snort -q -c /etc/snort/snort.conf -i ens3 &


Lab Exercise 5
~~~~~~~~~~~~~~

 #. On the victim VM, check the content of the alert file via the command below. ::
 
	tail -f /var/log/snort/alert
	
  .. note:: You should not see output from the alert file until moving forward with the next command.
  
  Now, on the attacker VM, launch the attack by entering the following command. ::
  
	$ nmap --script http-brute -p 80 192.168.1.20
  
  Observe the alert output on the victim VM and take a screenshot of the alerts for HTTP brute-force attacks.
  
  

What To Submit
--------------
**Network Intrusion Detection**

Save your answers (with screenshots) to all Task questions into a PDF file and name the file as ``nids-ans.pdf``.
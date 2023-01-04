.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

==============
SDN Controller
==============

Introduction
------------

**Overview:** This lab covers the software-defined networking (SDN) controller, 
which is an application in SDN that manages flow control to enable
intelligent networking. SDN controllers are based on protocols, such
as OpenFlow, that allow servers to tell switches where to send packets.
The controller is the core of an SDN network. It connects the northbound
applications and service and the southbound networking infrastructure. Any
communications between applications and infrastructure have to go
through the controller.

In this lab, students will learn the basic concept of the SDN controller by
using OpenDayLight controller in a simulated SDN environment. They will
also learn how to check the network topology in the OpenDayLight User
Interface (DLUX UI), understand the northbound interface by learning a
set of common REST APIs, and learn about the southbound interface by analyzing the
packet walkthrough between SDN controller and switch.

**Objectives:** The material in this lab aligns with the following
objectives:

-  Understand the concepts of an SDN controller

-  Learn to inspect the topology in the DLUX UI

-  Learn to use REST APIs in the DLUX UI

-  Observe the packet walkthrough in Software-Defined Networking

**Required Knowledge:** Students are required to have the following prerequisite knowledge for
this lab:

-  Familiar with the Linux system

-  Basic use of the Linux terminal and Linux commands

-  Familiar with the basic concept of REST APIs

-  Understand the process of HTTP request from a client to server

**Background:**

   |Description|

   For more information about |Platform|, please see bundled `user manual
   file`_.

   **Secure Shell (SSH)** is a network protocol that allows data to be
   exchanged over a secure channel between two computers. Encryption
   provides confidentiality and integrity of data. SSH uses public-key
   cryptography to authenticate the remote computer and allow the remote
   computer to authenticate the user, if necessary.

   For more information about SSH Tutorial, please see
   `<https://wiki.archlinux.org/index.php/Secure_Shell>`_

   **Mininet** is a network emulator which creates a network of virtual
   hosts, switches, controllers, and links. Mininet hosts run standard
   Linux network software, and its switches support OpenFlow for highly
   flexible custom routing and Software-Defined Networking.

   | For more information about Mininet Tutorial, please see
   | `<http://mininet.org/walkthrough/>`_

   **Opendaylight** is a collaborative open source project hosted by The
   Linux Foundation. The goal of the project is to promote software-defined
   networking and network functions virtualization. The software is written
   in the Java programming language.

   | For more information about Opendaylight Tutorial, please see
   | `https://www.opendaylight.org/ <https://www.opendaylight.org/%20>`__

   **Wireshark** is a free and open-source packet analyzer. It is used
   for network troubleshooting, analysis, software and communications
   protocol development, and education. Wireshark is very similar to
   tcpdump, but has a graphical front-end, plus some integrated sorting
   and filtering options.

   | For more information about Wireshark, please see its User’s Manual:
   | `<https://www.wireshark.org/docs/wsug_html_chunked/>`_

**Environment:**

Students should be able to view and access this lab on |Platform|, which is
a tool for easily deploying NetSiC labs including this one on a public
or private computing cloud. In this lab, students can access two
instances on OpenStack: one called mininet-vm and the other called
sdn-controller. The detailed configuration of these two instances is
provided below in `Table 1`_. The network topology for this lab looks as shown in below `Figure 1`_.

.. _Table 1:

**Table 1** VM properties and access information

+---------------+---------------+--------+----------+----------+----------------+
|**Name**       | **Image**     | **RAM**| **VCPU** | **Disk** | **Login        |
|               |               |        |          |          | account**      |
+===============+===============+========+==========+==========+================+
| sdn-controller| sdn-controller| 2GB    | 1        | 20GB     | See |Platform| |
|               |               |        |          |          |                |
+---------------+---------------+--------+----------+----------+----------------+
| mininet-vm    | mininet-vm    | 2GB    | 1        | 20GB     | See |Platform| |
+---------------+---------------+--------+----------+----------+----------------+

.. _Figure 1:

.. figure:: /xie/media/SDNmedia/SDN_img1.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 1** Lab network topology

In this lab, we need two tools: (1) Mininet (2) OpenDayLight. For
Mininet, we need to use it to emulate a network of virtual hosts,
switches, controllers, and links. Mininet hosts run standard Linux
network software, and its switches support OpenFlow for highly flexible
custom routing and Software-Defined Networking. OpenDayLight is an
open-source SDN controller, which can support network programmability
via southbound protocols, a bunch of programmable network services, a
collection of northbound APIs, and a set of applications. We have
pre-installed Mininet and Wireshark in the mininet-vm instance. We also
pre-built OpenDayLight controller into the sdn-controller instance.

Each student will get a specific slice (a collection of resources that
run in an isolated environment) of this lab, therefore many students can
work on this lab each with his/her own unique practice environment. This
ensures that each one can work separately without the need to worry
about his/her own work being interfered by other users’ operation.

Task 1: Use dashboard of OpenDayLight
-------------------------------------

In this task, students will learn how to use the OpenDayLight dashboard,
compare different types of network topology created by the ``mininet`` command
and check the node information.

Firstly, access the sdn-controller and turn on OpenDayLight by
typing the command line as below and press enter to open the shell when prompted. ::

	$ ./odl/bin/karaf

You should see the OpenDayLight controller is running as shown in
below `Figure 2`_.

.. _Figure 2:

.. figure:: /xie/media/SDNmedia/SDN_img2.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 2** Starting OpenDayLight controller from terminal

Open a browser on your host system and enter the URL in your browser
(Chrome is recommended). 

.. note:: It is running on the sdn-controller
          instance, so the IP address is floating IP of sdn-controller and the
          port defined by the application is 8181.

| Navigate to the URL and login to the dashboard: 
| **http://<sdn-controller’s floating IP>:8181/index.html**
| The default username and password are both **"admin"**.

.. figure:: /xie/media/SDNmedia/SDN_img3.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 3** OpenDayLight dashboard login screen

Access the mininet-vm and type the Mininet command shown below,
which will build a simple network topology including one switch, three
hosts, and connect to the remote SDN controller. ::

	$ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo single,3
	--mac --switch ovs,protocols=OpenFlow13

Now, let’s see the network topology by returning to the sdn-controller and clicking the **topology** tab on
the left pane. Type the ``pingall`` command on the mininet-vm instance,
and check the network topology again. You will see the topology just
like below in **Figure 4**.

.. figure:: /xie/media/SDNmedia/SDN_img4.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 4** Network topology of the OpenDaylight controlled network

Click on the **Nodes** on the left pane to see information about each
switch in the network.

.. figure:: /xie/media/SDNmedia/SDN_img5.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 5** Network nodes of the OpenDaylight controlled network

Click on the number of Node Connectors to view details such as port ID,
port name, number of ports per switch, MAC address and so on.

.. figure:: /xie/media/SDNmedia/SDN_img6.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 6** Node connectors of node openflow:1

Click **Node Connectors** to view Node Connector Statistics for the
particular node ID.

.. figure:: /xie/media/SDNmedia/SDN_img7.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 7** Node connector statistics of the nodes in openflow:1
   
.. admonition:: Important
	
				Make sure you finish task 1 below before you exit the Mininet console.

When you finish task 1, including the lab exercises, exit the Mininet
console following the command line below. ::

	mininet> exit

.. note:: Every time you exit the Mininet console, please use ``sudo mn -c`` command
          line to clean up the junk.

Lab Exercise 1
~~~~~~~~~~~~~~

1. What is the difference in network topology shown on the OpenDayLight DLUX UI
   before and after executing the ``pingall`` command on the mininet
   instance? Can you explain it?

2. Please execute the following two command lines, and take
   screenshots of each network topology in the DLUX UI.
   Compare the two topologies and describe the
   differences. ::

	   $ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo linear,3
	   --mac --switch ovs,protocols=OpenFlow13

	   $ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo tree,3
	   --mac --switch ovs,protocols=OpenFlow13

Task 2: Northbound REST API
---------------------------

The northbound interface provides controller services and a set of
common REST APIs that applications can leverage to manage networking
infrastructure configuration. In this task, students will learn some
REST APIs on the DLUX UI, which can help us to develop network
applications in the future.

Yangman is an ODL application offering dynamically generated UI form and
native JSON representation base on REST APIs. We can use Yangman to
build and send REST requests to the OpenDaylight data store. Also, we
can use it to get information from the data store, or to build REST
commands to modify information in the data store — changing network
configurations.

Now, open a terminal in the mininet-vm instance and clean up junk first
by the following command. ::

	$ sudo mn -c

Type the Mininet command line below on the mininet-vm instance. 
This command is the same one that was executed in Task 1 ::

	$ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo single,3
	--mac --switch ovs,protocols=OpenFlow13

Login the DLUX UI and then click on the **Yangman** tab in the left
pane. You will see the Yangman dashboard like this:

.. figure:: /xie/media/SDNmedia/SDN_img8.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 8** Yangman dashboard

On the left pane, you will see all available APIs. However, not all of
them will work because we did not install all features. One API that
will work is the **opendaylight-inventory rev**. Click on it, then click
“operational” in the drop-down menu and choose the “nodes”. On the right
pane, you can see four HTTP methods (GET, PUT, POST, and DELETE) by
clicking GET drop-down menu.

.. table:: **Table 2** HTTP methods for Northbound REST API

	+----------------+-----------------------------------------------------+
	| **Function**   | **Operation**                                       |
	+================+=====================================================+
	| GET            | Get data from OpenDayLight                          |
	+----------------+-----------------------------------------------------+
	| PUT / POST     | Send data to OpenDayLight for saving                |
	+----------------+-----------------------------------------------------+
	| DELETE         | Send data to OpenDayLight for deleting              |
	+----------------+-----------------------------------------------------+

Click on the blue “Send” button to send the GET API method to the
controller. You will see all the inventory information about network:
nodes, ports, statistics, etc. just like **Figure 9** below.

.. figure:: /xie/media/SDNmedia/SDN_img9.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 9** Requesting a REST API of OpenDaylight from Yangman
   dashboard

Understanding the Yang data model and learning how to read and write to
the data store is key to understanding Software Defined Networking with
the OpenDayLight controller.

Lab Exercise 2
~~~~~~~~~~~~~~

Your answers to the following questions should include screenshots of
the data you received.

1. Inspect the content of data you received in this task, what is the
   current speed of :font:`openflow:1:2 node-connector`?

2. Following the same method, can you use the GET API method to get the
   data of network topology in the Yangman dashboard? Please take a
   screenshot for “node-id” equal to “openflow:1”.
   
   .. admonition:: Hint
                   
				   API name is network-topology rev

Task 3: Southbound Protocol
---------------------------

The southbound interface implements protocols to manage and control the
underlying networking infrastructure. In this task, we will help
students to understand the packet walkthrough in the SDN environment by
giving a specific example. We will continue to use the simulated network
environment created in Task 2, and launch a simple HTTP server on :font:`h3`.
After that, we can make a request from :font:`h1` by Mininet. Let’s analyze the
HTTP request traffic by Wireshark.

Firstly, we will use the Mininet command line to launch a simple Python
web server as shown below. Secondly, we start Wireshark and start listening for packets.

::

	mininet> h3 python -m SimpleHTTPServer 80 &

::

        $ sudo wireshark-gtk
        
In this task, we will skip ARP and focus on the HTTP request. In :font:`h1` take
an HTTP GET request to :font:`h3` using the following command below. Since these
are TCP conversations, they always start with a SYN packet. 

::

	mininet> h1 wget h3

When :font:`s1` receives this request packet, it will check its local flow
tables. Since this is the first packet of the flow, it probably doesn’t
have a flow entry matching this incoming packet, which is called
table-miss. When there are no matching flows, the default actions will
forward the packet to the controller. :font:`s1` will send a Packet-IN message
to the SDN controller, which will encapsulate the original TCP SYN
message inside of it. When the controller receives the Packet-In
message, it might send a Packet-OUT message or a flow modification
message. The Packet-OUT message is an instruction from the controller to
the switch about what to do with the specific packet. And it contains an
encapsulated packet or references a buffer ID of a packet which is
stored. In this scenario, the controller will instruct the switch :font:`s1` to
send the packet from h1 out its port towards :font:`h3`.

Flow modification message instructs the switch to install a new flow
entry in its flow tables. The flow entry lets the switch know what to do
in the future. Any TCP port 80 requests from IP address and MAC of :font:`h1` to
IP address and MAC of :font:`h3` send all of those out port three. Flow
modification message also references a buffer ID. This will tell the
switch that first packet you buffered release the packet from your
buffer and apply the action in this message to it as well.

The Packet walkthrough of a HTTP request is shown in **Figure 10**.

.. figure:: /xie/media/SDNmedia/SDN_img10.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 10** An HTTP request packet flow in the OpenDaylight controlled
   network

When you’ve finished task 3, including the lab exercise, exit the
Mininet console by typing ``exit``.

Lab Exercise 3
~~~~~~~~~~~~~~

1. Depending on the study of a HTTP request, can you describe the packet
   walkthrough of a HTTP reply from h3 to h1?

2. Try to access the web server from h1 again, and inspect the content
   captured by the Wireshark. What is the difference compared to
   accessing the web server for the first time?

What to submit 
--------------

Save your answers (with screenshots) to the above questions into a PDF
file and name the file as ``sdn-controller-ans.pdf``.

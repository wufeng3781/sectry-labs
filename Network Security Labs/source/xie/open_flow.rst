.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt; font-style:bold} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

.. _EZSetup: http://172.16.9.209/login

========
OpenFlow
========

Introduction
------------


**Overview:** This lab covers OpenFlow, which is a software-defined
networking (SDN) standard specifying the control of the forwarding plane
operating on OpenFlow-compatible switches including Open vSwitch (OVS). OpenFlow
enables SDN in which the control plane and data/forwarding plane are decoupled.
OpenFlow specifies a southbound protocol between controller and switch,
and defines the components and functions of an OpenFlow logical switch.

In this lab, students will learn about the OpenFlow protocol, tables, access control list (ACL) and
basic concepts and programming of SDN. They will also practice on how to
create, maintain, and close an OpenFlow communication channel between a
switch and a controller, how to configure an OpenFlow switch using
standard OpenFlow controller and switch procedures, how to explore and
program tables in OpenFlow switches.

**Objectives:** This material in this lab aligns with the following
objectives.

-  Understand the concept of OpenFlow protocol

-  Analysis of the communication between a switch and a SDN controller

-  Learn the concept of flow entries and flow priority

-  Explore tables present in OpenFlow switches such as a flow table, and group
   table

**Required Knowledge:** Students are required to have the following prerequisite knowledge for
this lab:

-  Familiar with the Linux system

-  Basic use of the Linux terminal and Linux commands

-  Understand the basic concepts about Internet Control Message Protocol (ICMP)

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
provided in the below `Table 1`_. The network topology for this lab is shown below in `Figure 1`_.

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

.. figure:: /xie/media/OFmedia/OF_img1.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 1** Lab network topology

In this lab, we need three tools: (1) Mininet (2) Wireshark (3)
OpenDayLight. Mininet is used to emulate a network of
virtual hosts, switches, controllers, and links. Mininet hosts run
standard Linux network software, and its switches support OpenFlow for
highly flexible custom routing and Software-Defined Networking (SDN).
Wireshark will be used to sniff the traffic in network testbed
created by Mininet, which can help us analyze the OpenFlow protocol.
OpenDayLight is an open-source SDN controller, which can support network
programmability via southbound protocols, a bunch of programmable
network services, a collection of northbound APIs, and a set of
applications. We have pre-installed Mininet and Wireshark in the
mininet-vm instance and pre-built OpenDayLight controller into the
sdn-controller instance.

Each student will get a specific slice (a collection of resources that
run in an isolated environment) of this lab, therefore many students can
work on this lab each with his/her own unique practice environment. This
ensures that each one can work separately without the need to worry
about his/her own work being interfered by other users’ operation.

Task 1: Observe the communication between SDN controller and switch
-------------------------------------------------------------------

In this task, students will capture the packets of the OpenFlow protocol
between SDN controller in sdn-controller instance and switch in
mininet-vm instance.

Firstly, access the sdn-controller through |Platform| and 
turn on the OpenDayLight on the sdn-controller instance by
typing the command line as below. 

.. note:: Please note that in the command below it is ODL in lowercase, not to be confused with od1.

::
  
   $ ./odl/bin/karaf

You will see the OpenDayLight controller is running as shown in below `Figure 2`_

.. _Figure 2:

.. figure:: /xie/media/OFmedia/OF_img2.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 2** Starting OpenDayLight controller from terminal

Secondly, access the GUI of mininet-vm instance through |Platform|, and type
the command below in a terminal window to open Wireshark so that we can
view the traffic between the SDN controller and the switch. 

::

   $ sudo wireshark-gtk

In Wireshark, choose :font:`ens3` Interface, then click “Start” button.

In the Wireshark filter box, type the “openflow_v4” filter, then click
“Apply”:

.. _Figure 3:

.. figure:: /xie/media/OFmedia/OF_img3.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 3** Apply Wireshark filter and start capturing OpenFlow packets

.. note:: For now, there should be no OpenFlow packets displayed in the main
          window as displayed above in `Figure 3`_.

Then, type the Mininet command on the mininet-vm instance as below,
which can build a simple network topology including one switch, three
hosts, and connect to the remote SDN controller. 

::

   $ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo single,3 --mac --switch ovs,protocols=OpenFlow13

The topology looks as shown below in `Figure 4`_.

.. _Figure 4:

.. figure:: /xie/media/OFmedia/OF_img4.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 4** Mininet host and controller topology

Your Wireshark window should show some OpenFlow protocol packets
like the ones in `Figure 5`_.

.. _Figure 5:

.. figure:: /xie/media/OFmedia/OF_img5.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 5** Captured OpenFlow packets in Wireshark

You should see the OFPT_HELLO message, which is used by both the
switch and the controller to identify and negotiate the OpenFlow version
supported by both the devices. "Hello" messages should be sent from the
switch once the TCP/TLS connection is established and are considered
part of the communication channel establishment procedure.

The OFPT_FEATURES_REQUEST message goes from the controller once the
connection setup is completed which is used by the controller to fetch
the basic capabilities and features supported by the switch. The switch
should respond with supported features via an OFPT_FEATURES_REPLY
message.

.. admonition:: Important

   Make sure you fully complete `Lab Exercise 1`_ before exiting the Mininet console.

When you finished the task 1, exit the Mininet following the command. 

::

   mininet> exit

Lab Exercise 1
~~~~~~~~~~~~~~

When answering the following questions, you should take screenshots and
indicate where in the message you’ve found the information that answers
the following questions. When you hand in your tasks, annotate the
output so that it’s clear where in the output you’re getting the
information for your answer:

1. Before sending the OFPT_HELLO message from the switch, how is the TCP
   connection established between the switch and controller? (hint:
   view the packet before OFPT_HELLO message)

2. What is your version of OpenFlow?

3. Except the **OFPT_HELLO**, **OFPT_FEATURES_REQUEST** and **OFPT_FEATURES_REPLY**
   message, please list any **eight** OpenFlow protocol messages
   shown in your Wireshark windows.

Task 2: Flow Entries and Priority
---------------------------------

In this task, students will learn how to add, delete, dump the flow
entries and understand the concept of flow priority.

Task 2.1: Flow Entries
~~~~~~~~~~~~~~~~~~~~~~

Open a terminal in the mininet-vm instance and clean up junk first by
the following command. 

::

   $ sudo mn -c

Type the Mininet command line found below on the mininet-vm instance, which
will build a simple network topology like the `Figure 4`_ excluding the SDN
controller. 

::

   $ sudo mn --topo=single,3 --mac

There are three ports on the :font:`s1` switch, namely :font:`s1-eth1`, :font:`s1-eth2`,
:font:`s1-eth3`. You can use ``ovs-ofctl`` command as below to show the port
information. ::

	mininet> sh ovs-ofctl show s1
	OFPT_FEATURES_REPLY (xid=0x2): dpid:0000000000000001
	n_tables:254, n_buffers:0
	capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
	actions: output enqueue set_vlan_vid set_vlan_pcp strip_vlan mod_dl_src
	mod_dl_dst mod_nw_src mod_nw_dst mod_nw_tos mod_tp_src mod_tp_dst
	 1(s1-eth1): addr:52:20:4f:b1:e6:5d
		 config: 0
		 state: 0
		 current: 10GB-FD COPPER
		 speed: 10000 Mbps now, 0 Mbps max
	 2(s1-eth2): addr:52:dd:cd:cf:16:ba
		 config: 0
		 state: 0
		 current: 10GB-FD COPPER
		 speed: 10000 Mbps now, 0 Mbps max
	 3(s1-eth3): addr:a6:22:27:0d:69:c2
		 config: 0
		 state: 0
		 current: 10GB-FD COPPER
		 speed: 10000 Mbps now, 0 Mbps max
	 LOCAL(s1): addr:da:c2:dc:5d:2a:48
		 config: PORT_DOWN
		 state: LINK_DOWN
		 speed: 0 Mbps now, 0 Mbps max
	OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0

.. note:: You will see the corresponding port number of these three ports are 1,
          2, 3, respectively.

Now, let us look at flow entries that are the instructions that tell an
OpenFlow switch what to do with an incoming stream of packets. Let us
execute the command ``ovs-ofctl dump-flows <bridge>`` to print the
OpenFlow table entries on bridge :font:`s1`. ::

	mininet> sh ovs-ofctl dump-flows s1

You will see the output like the following result but the values in
duration, n_packets, and n_bytes fields may be different with yours: ::

	cookie=0x0, duration=9.757s, table=0, n_packets=17, n_bytes=1462,
	priority=0 actions=NORMAL

The meanings of the fields in the above output are listed below:

-  **duration**: number of seconds the entry has been in the table
-  **table**: specific table in which the flow is installed on
-  **n_packets**: number of packets that have matched the entry
-  **idle_age**: number of seconds since last packet matched the entry
-  **actions**: actions to take when a packet matches the flow entry

For this default flow on bridge :font:`s1` with “actions=NORMAL”. A **NORMAL**
action allows the device to conduct normal L2/L3 packet processing.

Let us add a new flow entry on bridge :font:`s1`, which matches all ICMP
packets. ::

	mininet> sh ovs-ofctl add-flow s1 icmp,action=normal

After that, we can implement ``pingall`` command line. ::

	mininet> pingall

.. warning:: Before moving on, complete #1 on Lab Exercise 2, Task 2.1

Then delete entry of :font:`s1`. ::

	mininet> sh ovs-ofctl del-flows s1

Dump flows again. We can see there are no longer flow entries. ::

	mininet> sh ovs-ofctl dump-flows s1

Task 2.2: Flow Priority
~~~~~~~~~~~~~~~~~~~~~~~

Now, let’s study the concept of priority, which is a critical concept
for OpenFlow. If a packet arrives at the switch and there are multiple
flow entries matching this packet, only the flow entry with the highest
priority will be used and all others will be ignored. This idea is
similar to traditional switch ACL where the first match is acted on and
all other matches in ACL would be ignored.

First, let’s add flow entries using the commands shown
below. the packets arriving at the OpenFlow port one will be sent to OpenFlow
port two and vice versa. ::

	mininet> sh ovs-ofctl add-flow s1 priority=500,in_port=1,actions=output:2

	mininet> sh ovs-ofctl add-flow s1 priority=500,in_port=2,actions=output:1

Now, type the command below. ::

	mininet> h1 ping h2 -c 3

It is obvious that :font:`h1` and :font:`h2` can reach each other. Let’s dump flows
again for :font:`s1`. We can see two flow entries and some packets have hit to
them as shown in the screenshot below. ::

	mininet> sh ovs-ofctl dump-flows s1
	cookie=0x0, duration=28.037s, table=0, n_packets=5, n_bytes=378,
	priority=500,in_port="s1-eth1" actions=output:"s1-eth2"
	cookie=0x0, duration=23.741s, table=0, n_packets=5, n_bytes=378,
	priority=500,in_port="s1-eth2" actions=output:"s1-eth1"

.. note:: If you want to see the port number instead of the port name, you can
          append --no-names on the command above. ::

			mininet> sh ovs-ofctl dump-flows s1 --no-names
			NXST_FLOW reply (xid=0x4):
			cookie=0x0, duration=220.066s, table=0, n_packets=6, n_bytes=448,
			idle_age=49, priority=500,in_port=1 actions=output:2
			cookie=0x0, duration=215.769s, table=0, n_packets=6, n_bytes=448,
			idle_age=148, priority=500,in_port=2 actions=output:1

Let’s test this priority concept with a new flow entry. ::

	mininet> sh ovs-ofctl add-flow s1 priority=5000,actions=drop

There is no match condition which means this rule matched every packet.

When you have finish task 2, exit the Mininet console by typing the command ``exit``.

Lab Exercise 2
~~~~~~~~~~~~~~

Please answer the following questions and take screenshots showing your
ping information if needed.

**Task 2.1**

1. Before deleting flows on switch :font:`s1`, observe the content of dump
   flows. For the flow entry that matches the ICMP packets you just
   added, how many packets and how many bytes matched it?

2. After deleting your flow, execute the ``pingall`` command. What content
   is shown on your screen?

**Task 2.2**

1. Can you add flow entries that :font:`h3` can ping :font:`h2`? Please take a
   screenshot showing your ping information.

2. Can you ping from :font:`h1` to :font:`h2` now after adding a new flow entry (``sh
   ovs-ofctl add-flow s1 priority=5000,actions=drop``)? If not, can you
   modify the priority of flows which let :font:`h1` can ping :font:`h2`?

Task 3: Group Table
-------------------

Group table is an abstraction that facilitates more complex and
specialized packet operations that cannot easily be performed through a
flow table entry. Each group receives packets as input and performs any
OpenFlow actions on these packets. Group table contains separate lists
of actions, and each individual action list is referred to as an
OpenFlow bucket. Thus, it’s said that a group table contains a bucket
list. Each bucket or list of buckets can be applied to incoming packets.
The exact behavior depends on the group table type. There are four types
of groups as shown below in the **Table 2**.

**Table 2** OpenFlow group table type and functionalities

+----------------+-----------------------------------------------------+
| **Type**       | **Functionality**                                   |
+================+=====================================================+
| ALL            | Execute all buckets in the group. This group is     |
|                | used for multicast or broadcast forwarding. The     |
|                | packet is effectively cloned for each bucket; one   |
|                | packet is processed for each bucket of the group    |
+----------------+-----------------------------------------------------+
| SELECT         | Execute one bucket in the group. Packets are        |
|                | processed by a single bucket in the group, based on |
|                | a switch-computed selection algorithm               |
+----------------+-----------------------------------------------------+
| INDIRECT       | Execute the one defined bucket in this group.       |
+----------------+-----------------------------------------------------+
| FAST FAILOVER  | Execute the first live bucket. Each action bucket   |
|                | is associated with a specific port and/or group     |
|                | that controls its liveness. The buckets are         |
|                | evaluated in the order defined by the group, and    |
|                | the first bucket which is associated                |
+----------------+-----------------------------------------------------+

In this task, we will learn to use group table by practicing a simple
experiment under a simulated environment. Just like the beginning of the
last task, let’s open a terminal in the mininet-vm instance and clean up
the junk first by executing the command below. 

::

   $ sudo mn -c

Then, type the Mininet command line on the mininet-vm instance as below
to build a simple network topology including one switch, three hosts. 

::

   $ sudo mn --topo=single,3 --mac

Set up the Open vSwitch that can support OpenFlow version 1.3. ::

	mininet> sh ovs-vsctl set bridge s1 protocols=OpenFlow13

Add a group table by typing the command line below. ``type=all`` means
this group table will execute all the buckets in the group. In this
group table, packets will be forwarded to port one, two and three. The code below is one command

::

	mininet> sh ovs-ofctl -O OpenFlow13 add-group s1
	group_id=50,type=all,bucket=output:1,bucket=output:2,bucket=output:3

When packets come into port one, it will match the flow entry below that
will implement the group table with ID 50. ::

	mininet> sh ovs-ofctl -O OpenFlow13 add-flow s1 in_port=1,actions=group:50

The following flow entry shows that packets arrived at OpenFlow port two
will be sent to OpenFlow port one. ::

	mininet> sh ovs-ofctl -O OpenFlow13 add-flow s1 in_port=2,actions=output:1

Let’s dump the flow of :font:`s1`. ::

	mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 --no-names

You will the flow entries like this: ::

	mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
	OFPST_FLOW reply (OF1.3) (xid=0x2):
	cookie=0x0, duration=49.692s, table=0, n_packets=0, n_bytes=0, in_port=1
	actions=group:50
	cookie=0x0, duration=16.541s, table=0, n_packets=0, n_bytes=0, in_port=2
	actions=output:1
	cookie=0x0, duration=30.559s, table=0, n_packets=22, n_bytes=1828,
	priority=0 actions=NORMAL

Type the command below in terminal window to open Wireshark so that we can view
the traffic between SDN controller and switch. 

::

   $ sudo wireshark-gtk

In Wireshark, choose interface of :font:`host3` called :font:`s1-eth3`, then click
“Start” button.

In the Wireshark filter box, type the “icmp” filter, then click “Apply”.
In your terminal, let :font:`h1` ping :font:`h2` following the command line below. ::

	mininet> h1 ping h2 -c 5

The procedure of ICMP packets in topology is shown in the below `Figure 6`_.

.. _Figure 6: 

.. figure:: /xie/media/OFmedia/OF_img6.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 6** ICMP packet flow from virtual host 1 to host 2

Your Wireshark window should be shown ICMP request packets from :font:`h1` to :font:`h2`
as shown in below screenshot `Figure 7`_.

.. _Figure 7:

.. figure:: /xie/media/OFmedia/OF_img7.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 7** ICMP packets capture by Wireshark on s1-eth3

Lab Exercise 3
~~~~~~~~~~~~~~

1. Can you add a group table that h3 can not only receive the ICMP
   request packets but also ICMP reply packets? Please take a
   screenshot of Wireshark window that captures the :font:`s1-eth3` interface
   including ICMP request and ICMP reply packets.

What to submit 
--------------

Save your answers (with screenshots) to the above questions into a PDF
file and name the file as ``openflow-ans.pdf``.

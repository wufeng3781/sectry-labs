.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

============
Open vSwitch
============

Introduction
------------

**Overview:** This lab will cover the Open vSwitch, which is a software
application that connects virtual machine (VM) instances to a layer 2
(or L2, data link layer) virtual networks. In network virtualization,
virtual switches become the primary provider of network services for
VMs. OpenStack Neutron supports multiple virtual switching techniques
including Linux Bridge and Open vSwitch (OVS). OVS is a highly popular
open source virtual switch that supports standard management interfaces
and protocols including NetFlow and 802.1q VLAN tagging.

In this lab, students will learn basic concepts and terms of virtual
switching (e.g., bridge, port) and basic function and components of Open
vSwitch. Students will also be instructed to use Open vSwitch in a
series of exercises on switching in a cloud.

**Objectives:** This material in this lab aligns with the following
objectives:

-  Understand the basic concept of Open vSwitch

-  Learn the basic commands of Open vSwitch

-  Learn the core components of Open vSwitch

**Required Knowledge:** Students are required to have the following prerequisite knowledge for
this lab:

-  Familiar with the Linux system

-  Basic use of the Linux terminal and Linux commands

-  Understand the function of a physical switch

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
   `<https://wiki.archlinux.org/index.php/Secure_Shell?>`_

   **Open vSwitch** is a production quality, multilayer virtual switch
   licensed under the open source `Apache
   2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`__ license.  It is
   designed to enable massive network automation through programmatic
   extension, while still supporting standard management interfaces and
   protocols (e.g. NetFlow, sFlow, IPFIX, RSPAN, CLI, LACP, 802.1ag). 

   | For more information about Open vSwitch, please see
   | http://www.openvswitch.org/

   **Mininet** is a network emulator which creates a network of virtual
   hosts, switches, controllers, and links. Mininet hosts run standard
   Linux network software, and its switches support OpenFlow for highly
   flexible custom routing and Software-Defined Networking.

   | For more information about Mininet Tutorial, please see
   | http://mininet.org/walkthrough/

   **Opendaylight** is a collaborative open source project hosted by The
   Linux Foundation. The goal of the project is to promote software-defined
   networking and network functions virtualization. The software is written
   in the Java programming language.

   | For more information about Opendaylight Tutorial, please see
   | `https://www.opendaylight.org/ <https://www.opendaylight.org/%20>`__

**Environment:**
Students should be able to view and access this lab on |Platform|, which is
a tool for easily deploying NetSiC labs including this one on a public
or private computing cloud. In this lab, students can access two
instances on OpenStack: one called mininet-vm and the other called
sdn-controller. The detailed configuration of these two instances is
provided in the below **Table 1**.

**Table 1** VM properties and access information

+--------------+--------------+--------+----------+----------+----------------+
|**Name**      | **Image**    | **RAM**| **VCPU** | **Disk** | **Login        |
|              |              |        |          |          | account**      |
+==============+==============+========+==========+==========+================+
| mininet-vm   | mininet-vm   | 4GB    | 2        | 60GB     | See |Platform| |
+--------------+--------------+--------+----------+----------+----------------+
| sdn          | sdn          | 4GB    | 2        | 60GB     | See |Platform| |
| - controller | - controller |        |          |          |                |
+--------------+--------------+--------+----------+----------+----------------+

The network topology for this lab as shown in Figure 1 below.

.. figure:: /xie/media/OVSmedia/OVS_img1.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 1** Lab network topology

In this lab, we need two tools: (1) Mininet (2) OpenDayLight. For the
Mininet, we need to use it to emulate a network of virtual hosts,
switches, controllers, and links. Mininet hosts run standard Linux
network software, and its switches support OpenFlow for highly flexible
custom routing and Software-Defined Networking (SDN). OpenDayLight is an
open-source SDN controller, which can support network programmability
via southbound protocols, a bunch of programmable network services, a
collection of northbound APIs, and a set of applications. Mininet 
has been pre-installed on the mininet-vm instance and OpenDayLight 
controller has been pre-built into the sdn-controller instance.

Also, in this lab, we have created two networks: (1) internal network (2) test
network. For the internal network, the ethernet interface ens3 of both
instances connect to it. Moreover, these instances can access outside
networks through it, because the IP address of each interface is
associated with a floating IP. Test network will serve the task 1. The
ethernet interface ens4 on the mininet-vm instance connects to this
network.

Each student will get a specific slice (a collection of resources that
run in an isolated environment) of this lab, therefore many students can
work on this lab each with his/her own unique practice environment. This
ensures that each one can work separately without the need to worry
about his/her own work being interfered by other users’ operation.

Task 1: Basic OVS Commands
--------------------------

Open vSwitch is an open-source virtual switch software designed for
virtual servers, which is very similar to a physical server connecting
to physical ports on a Layer 2 network switch. The role of this software
is to forward traffic between different virtual machines within the same
host and even traffic between a VM and a physical network. This supports
standard management interfaces like NetFlow, sFlow, CLI, and SPAN. Open
vSwitch can accept program extensions and control using OpenFlow, as
well as make use of the OVSDB management protocol.

In this first task, students will be acquainted with the ``ovs`` command through
practicing binding hosts with your local OVS bridge. In this scenario,
we will use Mininet to create a simulated network environment through the Mininet
command line, which will include one switch and several hosts.

Before working on this task, we need to know how Mininet works. Mininet
creates virtual networks using process-based virtualization and network
namespaces. In Mininet, hosts are emulated as bash processes running in
a network namespace. The Mininet "Host" will have its own private
network interface and can only see its own processes. Switches in
Mininet are software-based switches like Open vSwitch or the OpenFlow
reference switch. Links are virtual ethernet pairs, which live in the
Linux kernel and connect our emulated switches to emulated hosts
(processes).

In fact, this lab will instruct you how to connect your local bridge to the
network namespaces created by Mininet. This task is composed of
three subtasks. "`Task 1.1: Add an Ethernet Interface to OVS Bridge`_"
will guide you how to add an ethernet interface to
an OVS bridge in the mininet-vm instance. "`Task 1.2: Show the Network Namespace of Each Mininet Hosts`_" 
will introduce Mininet hosts. In "`Task 1.3: Connection between OVS bridge and Mininet Hosts`_", 
we will detach the hosts from the Open
vSwitch created by Mininet, and then connect these detached hosts to our
bridge. Now, let’s do it!

Task 1.1: Add an Ethernet Interface to OVS Bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this task, students will create a new bridge and add their Ethernet
ports to this new bridge. First, open a terminal of the mininet-vm
instance using SSH. We use the ``ovs`` command to add a new bridge called :font:`br0`. ::

	$ sudo ovs-vsctl add-br br0

Now, we know a new bridge exists on our system. Let’s look at the layout
of this bridge by running the following ``ovs`` command. ::

	$ sudo ovs-vsctl show
	4be7bdf3-cab2-4940-b432-961867dc99d4
		Bridge "br0"
			Port "br0"
				Interface "br0"
					type: internal

Then, let’s bring this new bridge and ethernet interface :font:`ens4` up
following the command line below. And you will see this interface
information by running ``ifconfig`` command. ::

	$ sudo ifconfig br0 up
	$ sudo ifconfig ens4 up
	$ ifconfig
	br0       Link encap:Ethernet HWaddr 6e:0f:06:18:66:4a
			  inet6 addr: fe80::6c0f:6ff:fe18:664a/64 Scope:Link
			  UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
			  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1
			  RX bytes:0 (0.0 B) TX bytes:648 (648.0 B)

	ens3      Link encap:Ethernet HWaddr fa:16:3e:d5:b7:c2
			  inet addr:10.0.0.5 Bcast:10.0.0.255 Mask:255.255.255.0
			  inet6 addr: fe80::f816:3eff:fed5:b7c2/64 Scope:Link
			  UP BROADCAST RUNNING MULTICAST MTU:1400 Metric:1
			  RX packets:17143 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:10744 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000
			  RX bytes:175644870 (175.6 MB) TX bytes:892630 (892.6 KB)

	ens4 	  Link encap:Ethernet HWaddr \**:**:**:**:**:*\*
			  inet6 addr: fe80::f816:3eff:fee3:e4af/64 Scope:Link
			  UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
			  RX packets:13 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:5 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000
			  RX bytes:1058 (1.0 KB) TX bytes:418 (418.0 B)

	lo        Link encap:Local Loopback
			  inet addr:127.0.0.1 Mask:255.0.0.0
			  inet6 addr: ::1/128 Scope:Host
			  UP LOOPBACK RUNNING MTU:65536 Metric:1
			  RX packets:160 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:160 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1
			  RX bytes:11840 (11.8 KB) TX bytes:11840 (11.8 KB)

After that, we can add :font:`ens4` to :font:`br0`. ::

	$ sudo ovs-vsctl add-port br0 ens4

.. warning:: Please make sure that you type in the correct interface name. 
	If you type :font:`ens3`, you will lose the internet connectivity. 
	This is because the interface :font:`ens3` is on the :font:`br0`, 
	the system is still trying to connect to the internet directly via :font:`ens3`.

To ensure the connection was created successfully, type the command shown
below, which displays the bridge interfaces and the connection state. ::

	$ sudo ovs-vsctl show
	4be7bdf3-cab2-4940-b432-961867dc99d4
	Bridge "br0"
		Port "ens4"
			Interface "ens4"
		Port "br0"
			Interface "br0"
				type: internal

Task 1.2: Show the Network Namespace of Each Mininet Hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the network is working, we can SSH the mininet-vm instance. Now we
need to open two terminals of mininet-vm instance by SSH. In one of the
terminals, we type the ``sudo mn`` and press ``Enter``, which can build a
simple network topology including one switch and two hosts. In order to
distinguish from the other terminal, we call it **Terminal 1**.

In the other terminal, we type ``sudo ip netns`` to check network
namespaces. You should see nothing because the network namespace gets
associated with the host via its process id (PID) and does not get a
name. However, you will see a new bridge and three ports created by
Mininet using the command shown below. ::

	$ sudo ovs-vsctl show
	4be7bdf3-cab2-4940-b432-961867dc99d4
		Bridge "br0"
			Port "ens4"
				Interface "ens4"
			Port "br0"
				Interface "br0"
					type: internal
		Bridge "s1"
			Controller "ptcp:6634"
			fail_mode: standalone
			Port "s1-eth1"
				Interface "s1-eth1"
			Port "s1"
				Interface "s1"
					type: internal
			Port "s1-eth2"
				Interface "s1-eth2"

Now, we use ``ps`` command line to check the process id of hosts created by
Mininet. ::

	$ ps -ef | grep mininet
	root 25744 25737 0 01:19 pts/2 00:00:00 bash --norc -is mininet:h1
	root 25747 25737 0 01:19 pts/3 00:00:00 bash --norc -is mininet:h2
	root 25753 25737 0 01:19 pts/4 00:00:00 bash --norc -is mininet:s1

We can use the command line below to check the namespaces under
different processes. Replace ``<PID>`` with the process id of any of the
hosts given by the command above. ::

	$ sudo ls -al /proc/<PID>/ns
	total 0
	dr-x--x--x 2 root root 0 Mar 18 01:23 .
	dr-xr-xr-x 9 root root 0 Mar 18 01:19 ..
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 cgroup -> cgroup:[4026531835]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 ipc -> ipc:[4026531839]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 mnt -> mnt:[4026532227]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 net -> net:[4026532229]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 pid -> pid:[4026531836]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 user -> user:[4026531837]
	lrwxrwxrwx 1 root root 0 Mar 18 01:23 uts -> uts:[4026531838]

When the namespace is created, the ip command adds a bind mount point
for it under ``/var/run/netns``. This allows the namespace to persist even
if there’s no process attached to it. Now, let us see the content in
this directory. ::

	$ ls /var/run/netns
	ls: cannot access '/var/run/netns': No such file or directory

For now, ``/var/run/netns`` directory is not created. We use ``ip`` command line
as shown below to create a new namespace called :font:`test_ns`. ::

	$ sudo ip netns add test_ns

Checking the ``/var/run/netns`` directory again, you will see a new file
named :font:`test_ns`. ::

	$ ls /var/run/netns
	test_ns

Also, you can use ip command to check the namespace you just created. ::

	$ sudo ip netns
	test_ns

Now, we need to create a symbolic link in ``/var/run/netns`` directory
indicating the abstract location of h1 network namespace. The name of
this link called :font:`h1_ns`. ::

	$ sudo ln -s /proc/<PID of h1>/ns/net /var/run/netns/h1_ns

.. note:: Make sure to include the space after ``net`` in the command above.

After creating this soft link, we can use ip command to see the
namespace of host :font:`h1`. ::

	$ sudo ip netns
	h1_ns (id: 0)
	test_ns

Use the ``ip`` command line below to check the interface information of
:font:`h1_ns`. ::

	$ sudo ip netns exec h1_ns ifconfig -a
	h1-eth0   Link encap:Ethernet HWaddr 36:5d:1f:bc:af:e4
	          inet addr:10.0.0.1 Bcast:10.255.255.255 Mask:255.0.0.0
	          inet6 addr: fe80::345d:1fff:febc:afe4/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
	          RX packets:15 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:1206 (1.2 KB) TX bytes:648 (648.0 B)
			  
	lo        Link encap:Local Loopback
	          inet addr:127.0.0.1 Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING MTU:65536 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

In **Terminal 1**, type the Mininet command below. ::

	mininet> h1 ifconfig
	h1-eth0   Link encap:Ethernet HWaddr 36:5d:1f:bc:af:e4
	          inet addr:10.0.0.1 Bcast:10.255.255.255 Mask:255.0.0.0
	          inet6 addr: fe80::345d:1fff:febc:afe4/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
	          RX packets:15 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:1206 (1.2 KB) TX bytes:648 (648.0 B)
			  
	lo        Link encap:Local Loopback
	          inet addr:127.0.0.1 Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING MTU:65536 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

.. note:: **Terminal 1** will be used later on in Lab Exercise 2, so please do not ``exit`` until this lab has been completed.

Task 1.3: Connection between OVS bridge and Mininet Hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In task 1.3, we will connect OVS bridge and Mininet hosts. And we will
implement it following the **Figure 2** below.

.. figure:: /xie/media/OVSmedia/OVS_img2.png
   :align: center
   :alt: alternate text
   :figclass: align-center
   
   **Figure 2** Connection between OVS bridge and Mininet Hosts

Before connecting Mininet host to our local bridge, we need to detach
the hosts from the Open vSwitch created by Mininet. We will use ``ip``
command line below to delete :font:`s1-eth1` and :font:`s1-eth2` ports. ::

	$ sudo ip link del s1-eth1
	$ sudo ip link del s1-eth2

Now, checking the interface information of host :font:`h1`, you cannot see the
:font:`h1-eth0`. ::

	$ sudo ip netns exec h1_ns ifconfig -a
	lo        Link encap:Local Loopback
	          inet addr:127.0.0.1 Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING MTU:65536 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

Then, we need to create the veth pairs, which are virtual ethernet
interfaces. One veth interface will come out the other
peer veth interface. ::

	$ sudo ip link add h1-ens1 type veth peer name vport1

Set :font:`h1-ens1` in the Host h1 network namespace. ::

	$ sudo ip link set h1-ens1 netns h1_ns

You will see a new interface when you check the interface information of
:font:`h1`. ::

	$ sudo ip netns exec h1_ns ifconfig -a
	h1-ens1   Link encap:Ethernet HWaddr ee:55:ae:86:2e:17
	          BROADCAST MULTICAST MTU:1500 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

	lo        Link encap:Local Loopback
	          inet addr:127.0.0.1 Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING MTU:65536 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

Add :font:`vport1` in :font:`br0`. ::

	$ sudo ovs-vsctl add-port br0 vport1

We can now see a new port that exists on the bridge :font:`br0` following the command below. ::

	$ sudo ovs-vsctl show
	4be7bdf3-cab2-4940-b432-961867dc99d4
		Bridge "br0"
			Port "ens4"
				Interface "ens4"
			Port "vport1"
				Interface "vport1"
			Port "br0"
				Interface "br0"
					type: internal
		Bridge "s1"
			Controller "ptcp:6634"
			fail_mode: standalone
			Port "s1-eth1"
				Interface "s1-eth1"
					error: "could not open network device s1-eth1 (No such device)"
			Port "s1"
				Interface "s1"
					type: internal
			Port "s1-eth2"
				Interface "s1-eth2"

Bring up the interface :font:`vport1`. ::

	$ sudo ifconfig vport1 up

:font:`h1-ens1` has been moved to the :font:`h1_ns` namespace, we need to configure the interface using the ``ip netns exec`` command below. In this case, we are using ``ifconfig`` to assign an IP address to the vport1 interface. ::

	$ sudo ip netns exec h1_ns ifconfig h1-ens1 10.0.0.3

Let us check the new interface information of :font:`h1-ens1` by the following
command. ::

	$ sudo ip netns exec h1_ns ifconfig -a
	h1-ens1   Link encap:Ethernet HWaddr ee:55:ae:86:2e:17
              inet addr:10.0.0.3 Bcast:10.255.255.255 Mask:255.0.0.0
              inet6 addr: fe80::ec55:aeff:fe86:2e17/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
              RX packets:8 errors:0 dropped:0 overruns:0 frame:0
              TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:648 (648.0 B) TX bytes:648 (648.0 B)
			  
	lo        Link encap:Local Loopback
	          inet addr:127.0.0.1 Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING MTU:65536 Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1
	          RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

Lab Exercise 1
~~~~~~~~~~~~~~

Please answer the following question.

**Task 1.1**

1. What is your :font:`ens4` MAC address? Please take a screenshot and indicate
   where in the message you’ve found the information that answers the
   following questions.

2. What is your version of Open vSwitch?

**Task 1.2**

1. Based on task 1.2, please create the soft link called :font:`h2_ns` for
   host :font:`h2`. You need to use ip commands used above and take screenshots
   to prove that you created :font:`h2_ns` successfully.

**Task 1.3**

1. Following the instruction of connecting :font:`h1-ens1` and :font:`vport1`, please create a new port in bridge :font:`br0` to connect to the :font:`h2-ens1`. Can you assign 10.0.0.4 IP address to this :font:`h2-ens1` interface?

2. Can you use ``ip netns exec`` command to ping 10.0.0.4 from :font:`h1_ns`?
   Please take a screenshot, if you can ping the IP address of :font:`h2`
   successfully.

Task 2: Components of Open vSwitch
----------------------------------

In this task, we will introduce the main component of Open vSwitch
including ovs-vswitchd, ovsdb-server, and kernel module.
**Ovs-vswitchd** is a daemon that implements the switch, along with a
companion Linux kernel module for flow-based switching.

**Ovsdb-server** is a lightweight database server. The switch configuration
for OVS is stored in the ovsdb-server. Moreover, ovs-vswitchd queries obtain
its configuration from ovsdb-server.

The ``sudo ovs-vsctl list`` command shows records of different tables in
the ovsdb-server. For example, we can check the bridge information from
ovsdb-server following the command line. ::

	$ sudo ovs-vsctl list Bridge
	\_uuid : ee3d37ec-5353-4a53-8bed-05a4c56722ab
	auto_attach : []
	controller : [1aeb50e5-a459-45f7-87c8-e84dba3cb933]
	datapath_id : "0000000000000001"
	datapath_type : ""
	datapath_version : "<unknown>"
	external_ids : {}
	fail_mode : standalone
	flood_vlans : []
	flow_tables : {}
	ipfix : []
	mcast_snooping_enable: false
	mirrors : []
	name : "s1"
	netflow : []
	other_config : {datapath-id="0000000000000001", disable-in-band="true"}
	ports : [88616ff2-5275-4df3-aa2d-b589ef6777b6,
	a6896145-0a33-4e90-9288-135f2b144c97,
	baabca29-4eca-4a9a-b8b9-f933b6800cdf]
	protocols : []
	rstp_enable : false
	rstp_status : {}
	sflow : []
	status : {}
	stp_enable : false

**Kernel module** is also an important part of the Open vSwitch. When a
packet arrives at a virtual switch, if there is a cached match in the
kernel module, the cached actions are taken. If there’s not a match in
the kernel module, the packet is sent to SDN controller using OpenFlow
protocol. And the SDN controller will send a message to instruct Open
vSwitch to install a new flow entry in its flow tables. Further packets
will have a fast path through the cached entries in OVS kernel module.

Firstly, turn on the OpenDayLight on the sdn-controller instance by
typing the command line as below. ::

	$ ./odl/bin/karaf

Then, type the Mininet command line on the mininet-vm instance as below,
which can build a simple network topology including one Open vSwitch
enabling OpenFlow 1.3, three hosts, and connect to the remote SDN
controller. ::

	$ sudo mn --controller=remote,ip=10.0.0.8,port=6633 --topo single,3
	--mac –-switch ovs,protocols=OpenFlow13

Let’s dump flows of the :font:`s1`. Use the ``-O`` option to enable support for the version of OpenFlow 1.3 in ovs-ofctl. ::

	mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
	cookie=0x2b00000000000000, duration=10.137s, table=0, n_packets=0,
	n_bytes=0, priority=100,dl_type=0x88cc actions=CONTROLLER:65535
	cookie=0x2b00000000000000, duration=8.216s, table=0, n_packets=1,
	n_bytes=70, priority=2,in_port="s1-eth3"
	actions=output:"s1-eth2",output:"s1-eth1",CONTROLLER:65535
	cookie=0x2b00000000000001, duration=8.216s, table=0, n_packets=1,
	n_bytes=70, priority=2,in_port="s1-eth2"
	actions=output:"s1-eth3",output:"s1-eth1",CONTROLLER:65535
	cookie=0x2b00000000000002, duration=8.216s, table=0, n_packets=1,
	n_bytes=70, priority=2,in_port="s1-eth1"
	actions=output:"s1-eth3",output:"s1-eth2",CONTROLLER:65535
	cookie=0x2b00000000000000, duration=10.137s, table=0, n_packets=7,
	n_bytes=590, priority=0 actions=drop

we can generate some network traffic using the ping command. ::

	mininet> h1 ping h2 -c3

Let us dump the :font:`s1` again. When you created new traffic in the SDN
environment, new entries will be added in your flow table. ::

	mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1

	cookie=0x2b00000000000003, duration=65.524s, table=0, n_packets=0,
	n_bytes=0, priority=100,dl_type=0x88cc actions=CONTROLLER:65535
	cookie=0x2a00000000000012, duration=45.244s, table=0, n_packets=3,
	n_bytes=294, idle_timeout=600, hard_timeout=300,
	priority=10,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01
	actions=output:"s1-eth1"
	cookie=0x2a00000000000013, duration=45.244s, table=0, n_packets=3,
	n_bytes=294, idle_timeout=600, hard_timeout=300,
	priority=10,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02
	actions=output:"s1-eth2"
	cookie=0x2b00000000000009, duration=63.519s, table=0, n_packets=5,
	n_bytes=370, priority=2,in_port="s1-eth3"
	actions=output:"s1-eth2",output:"s1-eth1",CONTROLLER:65535
	cookie=0x2b0000000000000a, duration=63.519s, table=0, n_packets=10,
	n_bytes=748, priority=2,in_port="s1-eth2"
	actions=output:"s1-eth3",output:"s1-eth1",CONTROLLER:65535
	cookie=0x2b0000000000000b, duration=63.519s, table=0, n_packets=9,
	n_bytes=678, priority=2,in_port="s1-eth1"
	actions=output:"s1-eth3",output:"s1-eth2",CONTROLLER:65535
	cookie=0x2b00000000000003, duration=65.523s, table=0, n_packets=12,
	n_bytes=1068, priority=0 actions=drop

Lab Exercise 2
~~~~~~~~~~~~~~

Please answer the following questions.

1. Before exiting the simulated network topology created in Task 1.2,
   please check the interface information from ovsdb-server. What
   is the MTU value of bridge :font:`br0` and :font:`vport1` respectively? Take a
   screenshot to prove your answer.

2. Under Mininet environment, let :font:`h1` ping :font:`h2` again. Are there any
   changes when you dump the :font:`s1`?

3. Try ``pingall`` Mininet command, what entries do you find when you dump
   :font:`s1`.

What to submit 
--------------

Save your answers (with screenshots) to the above questions into a PDF
file and name the file as ``openflow-ans.pdf``.

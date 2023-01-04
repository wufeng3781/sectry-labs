.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

===============
Overlay Network
===============

Introduction
------------

**Overview:** Overlay networking is a way of building networks upon
existing physical or software networks to provide one or multiple
virtualized network layers for applications or security benefits. An
example of a widely-used overlay network would be the Internet, which is
built on the LAN (Local Area Network) by introducing various TCP/IP
protocols. The advantages of using overlay networking include reusing
existing network infrastructure, good scalability, and flexibility. In
the context of cloud computing, network providers also utilize a broad
range of overlay networks to support complex cloud networking
configurations. In this lab, we will introduce two types of overlay
networks that are popular in cloud data centers—GRE (Generic Routing
Encapsulation) and VXLAN (Virtual Extensible LAN). Students will get to
know the basic concepts of these two overlay network protocols, as well
as have some hands-on experiments of managing GRE and VXLAN networks by
utilizing EZSetup lab environment, Mininet, OpenVSwitch and Wireshark.

**Objectives:** Upon completing the experiments, students should

-  Understand the concepts of overlay networking;

-  Learn to set up overlay networks using Mininet and OpenvSwitch;

-  Learn to capture overlay network traffic using Wireshark;

-  Analyze overlay network packet and identify its difference to the
   traditional network.

**Required Knowledge:**

   Students are required to have the following prerequisite knowledge
   for this lab:

1. The usage of the text-based terminal and basic Linux commands;

2. Knowledge of accessing a remote Linux server using SSH;

3. Basic understanding of Linux networking and the use of common network
   devices such as routers and switches.

**Background:**

   **EZSetup** is a novel Web application capable of creating a variety
   of user-defined cybersecurity practice environments (e.g., labs and
   competition scenarios) in one or more computing clouds (e.g.,
   OpenStack or Amazon AWS). EZSetup provides a Web user interface for
   practice designers to create a practice scenario by dragging and
   dropping icons visually and the links between them thus allows for
   customization and significantly reduces overhead in creating and
   using practice environments. Completely spared from the complexity of
   creating practice environments, end users can jump right in and fully
   concentrate on cybersecurity practice.

   For more information about EZSetup, please see bundled `user manual
   file`_.

   **Secure Shell (SSH)** is a network protocol that allows data to be
   exchanged over a secure channel between two computers. Encryption
   provides confidentiality and integrity of data. SSH uses public-key
   cryptography to authenticate the remote computer and allow the remote
   computer to authenticate the user, if necessary.

   For more information about SSH, please see
   `<https://wiki.archlinux.org/index.php/Secure_Shell>`_

   **Mininet** is a network emulator, or perhaps more precisely a
   network emulation orchestration system. It runs a collection of
   end-hosts, switches, routers, and links on a single Linux kernel. It
   uses lightweight virtualization to make a single system look like a
   complete network, running the same kernel, system, and user code.

   For more information about Mininet, please see
   `<https://github.com/mininet/mininet/wiki/Introduction-to-Mininet>`_

   **Open vSwitch**, sometimes abbreviated as OVS, is an open-source
   implementation of a distributed virtual multilayer switch. The main
   purpose of Open vSwitch is to provide a switching stack for hardware
   virtualization environments, while supporting multiple protocols and
   standards used in computer networks.

   For more information about Open vSwitch, please see
   `<http://docs.openvswitch.org/en/latest/>`_

   **Wireshark** is a free and open-source packet analyzer. It is used for
   network troubleshooting, analysis, software and communications protocol
   development, and education. Wireshark is very similar to tcpdump, but
   has a graphical front-end, plus some integrated sorting and filtering
   options.

   For more information about Wireshark, please see its User’s Manual:
   `<https://www.wireshark.org/docs/wsug_html_chunked/>`_

**Environment:**

In this lab, students can access three virtual machines (VM) from
EZSetup deployed on public or private clouds like AWS or OpenStack. One
of them acts as a router, which provides connectivity between different
networks, and we can monitor network traffic on it in the meantime. The
other two are guest VMs, each in its local network with the router. We
create two virtual hosts using Mininet on each guest VM to mimic a
multiple-tenant situation in the cloud environment. The following **Figure
1** illustrates the initial network topology.

.. figure:: /xie/media/ONmedia/ON_img1.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 1** Lab network topology

The access information about these VMs is provided in the below **Table 1**.
Please refer to the EZSetup dashboard for the actual public IP addresses
and passwords.

**Table 1** VM properties and access information

+---------------+----------------------+--------+----------+----------+---------------+
|**Name**       | **Image**            | **RAM**| **VCPU** | **Disk** | **Login       |
|               |                      |        |          |          | account**     |
+===============+======================+========+==========+==========+===============+
| guest-vm-1    | overlaynetwork-vm-1  | 1GB    | 1        | 30GB     | See EZSetup   |
|               |                      |        |          |          |               |
+---------------+----------------------+--------+----------+----------+---------------+
| guest-vm-2    | overlaynetwork-vm-1  | 1GB    | 1        | 30GB     | See EZSetup   |
|               |                      |        |          |          |               |
+---------------+----------------------+--------+----------+----------+---------------+
| router        | overlaynetwork-router| 2GB    | 2        | 40GB     | See EZSetup   |
|               |                      |        |          |          |               |
+---------------+----------------------+--------+----------+----------+---------------+

Task 1: Setup the virtual hosts
-------------------------------

Most of the commercial cloud service providers use virtualization
technologies to create VMs or containers as servers and sell them to the
users. Using virtualized servers instead of the physical ones can
achieve higher resource utilization and better scalability, thus save
the cost for both consumers and companies. Inside a cloud environment,
resources of different tenants, or user groups, need to be isolated from
each other. Such resources can be CPU, memory, hard disk or network.
Before we dig into the methods of isolating networks for multiple
tenants, we should first create a multi-tenancy environment for the
following experiments. Here, we use Mininet to spawn some virtualized
hosts on the VMs.

Mininet is a network simulation tool for creating virtual hosts,
switches, network controllers and links, and it is often used for
research and education purposes. The Mininet command line tool should be
preinstalled on your guest VMs. To verify that the installation is
successful, please first SSH into your guest VM and type the following
command in the console: ::

	$ mn --version // show the Mininet version

Next, move to your guest VM corresponding lab directory (e.g. For the
guest VM 1, you should move to the ``~/labs/overlay_network/guest-vm-1``
directory) and use the setup scripts to create the hosts and switch that
connects them. Type ::

	$ sudo python start.py

This will add two virtual hosts, a NAT (Network address translation)
server and a switch to your Mininet environment. We will focus on the
hosts. After executing the script, you can validate the setup using ::

	mininet> dump

This command will list all the hosts, switches and controllers in the
current Mininet environment. You should have the following output on
your guest VM 1 ::

	<Host h1: h1-eth0:10.0.0.1 pid=15347>
	<Host h2: h2-eth0:10.0.0.1 pid=15350>
	<NAT nat0: nat0-eth0:10.0.0.3 pid=15406>
	<OVSBridge s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None,s1-eth3:None
	pid=15356>

As we can see from above, we now have two hosts named :font:`h1` and :font:`h2`, and an
OpenVSwitch named :font:`s1`. Also, each host has a network interface that is
named after the host’s name, and a corresponding network interface on
the switch. To show the network links between hosts and the switch, type ::

	mininet> links

In a Mininet environment, we can execute commands from both the VM and
the virtual hosts. To execute commands from the supporting VM, type ::

	mininet> sh <command of your choice>

An example would be ::

	mininet> sh hostname

This will show the hostname of the VM. To fire up a command from the
virtual host, simply type ::

	mininet> <virtual host name> <command>

like ::

	mininet> h1 route -n

This command shows the routing table of the host 1. For more information
about using Mininet, please type ::

	mininet> help

Lab Exercise 1
~~~~~~~~~~~~~~~~

Please log into the guest VM 2 and set up virtual hosts in the same way,
and answer the following questions:

1. On guest VM 2, which interface on the switch is host :font:`h3` connecting
   to? What about :font:`h4`?

2. On guest VM 2, what is the default gateway of the virtual host :font:`h3`?

   .. admonition:: Tip
   
      Find the gateway of the address 0.0.0.0 in the routing table

3. On guest VM 2, what is the MAC address of host :font:`h4`’s network
   interface? 
   
   .. admonition:: Tip

      Use ``ifconfig`` command to list all the interfaces

Task 2: Deploy VXLAN Network
----------------------------

Before we move into the Task 2, let us set up the routing rules in guest
VMs so that they can communicate with each other via Router VM.

In the guest VM 1, run the command line below. ::

	$ sudo ip route add 192.168.2.0/24 via 192.168.1.10

In the guest VM 2, execute the following command line. ::

	$ sudo ip route add 192.168.1.0/24 via 192.168.2.10 

After setting up the routing rules, we can deploy the Mininet
environment on both guest VMs. The network topology should like below
**Figure 2**.

.. figure:: /xie/media/ONmedia/ON_img2.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 2** Network topology after setting up the Mininet

As we can see from here, :font:`h1` and :font:`h2` have the same IP address, as well as
:font:`h3` and :font:`h4`. This is quite common in a multi-tenancy cloud environment,
where different user groups may have similar local network
configurations. To let network traffic reach the right destination even
though the machines have the same IP address as the target machine, we
need to isolate the tenant networks. Here, we assume :font:`h1` and :font:`h3` belong to
the same tenant and :font:`h2` and :font:`h4` belong to another tenant, which can be
illustrated in the following **Figure 3**.

.. figure:: /xie/media/ONmedia/ON_img3.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 3** Tunneling virtual hosts to form two tenant networks

In this network, hosts within the same tenant can communicate with each
other, even when they are not on the same VM, while hosts in different
tenants can’t. An intuitive way to achieve this would be deploying VLANs
(Virtual LAN) on switches. In a VLAN network, traffic will be tagged
with VLAN IDs at its outgoing switch port and will be accepted by a
destination switch port only if it has the same VLAN tag as the port. We
can assign different VLAN tags to the tenants to isolate their networks,
so we can separate traffic even if the hosts of different tenants have
same IPs.

We can also use VXLAN to isolate networks. VXLAN can be seen as an
upgrade to the traditional VLAN, which encapsulate OSI (Open Systems
Interconnection model) layer 2 Ethernet frames within layer 4 UDP (User
Datagram Protocol) diagrams. It uses 24-bit long VXLAN IDs (VNI) instead
of 12-bit long VLAN IDs, thus supports a more substantial number of
devices. Switch ports for VXLAN, or VXLAN tunnel endpoints (VTEP), is
responsible for routing, encapsulation, and decapsulation of the VXLAN
packets. The format of a VXLAN packet is shown in **Figure 4**.

.. figure:: /xie/media/ONmedia/ON_img4.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 4** VXLAN message packet format

The original packet is encapsulated with several headers, including
Outer Ethernet header, Outer IP header, Outer UDP header and VXLAN
header. Outer Ethernet and IP header have the MAC and IP addresses of
the sending and receiving hypervisor, in our case, are the addresses of
guest VMs. Outer UDP header contains the sending UDP port and receiving
UDP port number. The IANA (Internet Assigned Numbers Authority) has
assigned a well-known UDP port 4789 for the destination port number, so
the destination VTEP UDP port will always be 4789. The source port
number is calculated using a hash of the encapsulated packet. VXLAN
header contains the VNI, which will be matched by the VTEP port.

To further illustrate the communication process, we use the following
**Figure 5** to show packet changes during an ICMP (Internet Control Message
Protocol) ping. We can see that once the ICMP packet leaves the sending
VTEP, it will be wrapped with headers containing network location of the
sending and receiving guest VMs, along with VXLAN information. Upon
arriving at the receiving side VTEP, the VXLAN packet will be unwrapped
and sent to the host according to the destination information inside
ICMP packet.

.. figure:: /xie/media/ONmedia/ON_img5.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 5** Packet changes when passing through a VXLAN tunnel

To deploy VXLAN in the Mininet environment we built, enter the following
command on the guest VM 1 ::

	mininet> sh ovs-vsctl add-port s1 vtep -- set interface vtep type=vxlan
	option:remote_ip=192.168.2.20 option:key=flow ofport_request=10

This will create a VTEP port on the OpenVSwitch with port number 10 and
the remote sending/receiving VTEP IP address 192.168.2.20. Next, we have
to add some flow rules to redirect hosts’ traffic to the VTEP port and
filter incoming traffic to match the VNI. Load flow rules from local
file by executing ::

	mininet> sh ovs-ofctl add-flows s1 flows.txt

The content of flows.txt is ::

	table=0,in_port=1,actions=set_field:100->tun_id,resubmit(,1)
	table=0,in_port=2,actions=set_field:200->tun_id,resubmit(,1)
	table=0,actions=resubmit(,1)
	
	table=1,tun_id=100,dl_dst=00:00:00:00:00:01,actions=output:1
	table=1,tun_id=200,dl_dst=00:00:00:00:00:02,actions=output:2
	table=1,tun_id=100,dl_dst=00:00:00:00:00:03,actions=output:10
	table=1,tun_id=200,dl_dst=00:00:00:00:00:04,actions=output:10
	table=1,tun_id=100,arp,nw_dst=10.0.0.1,actions=output:1
	table=1,tun_id=200,arp,nw_dst=10.0.0.1,actions=output:2
	table=1,tun_id=100,arp,nw_dst=10.0.0.2,actions=output:10
	table=1,tun_id=200,arp,nw_dst=10.0.0.2,actions=output:10
	table=1,priority=100,actions=drop

The first two rules set the tunnel ID, or VNI in this case, of port 1
and 2. Port 1 is connected to :font:`host1` and port 2 is connected to :font:`host2`.
So all the outgoing traffic of :font:`host1` will be tagged as 100, and 200 for
:font:`host2`. To see a complete list of OpenVSwitch ports, please type ::

	mininet> sh ovs-vsctl show

The rest rules match incoming and outgoing traffic by tunnel ID and
destination MAC address. If the tunnel ID and MAC match a certain rule,
traffic will be sent to the corresponding port, either local or remote.
We should also take care of the ARP traffic so hosts in the same tenant
can find each other. Last, we drop other the traffic that does not match
any rule.

Using the same method, we can add VTEP port and flow rules on guest VM
2. The command and flow rules will be little different from VM 1. The
flows.txt for VM 2 should be already present. Please edit the VTEP
adding command by yourself.

To verify that hosts in the same tenant can communicate with each other,
please run the following commands on guest VM 1 ::

	mininet> h1 ping 10.0.0.2 -c 3
	mininet> h2 ping 10.0.0.2 -c 3

To make sure that we are visiting the right host inside the same tenant,
let’s set up a simple HTTP server on :font:`h3` on guest VM 2 ::

	mininet> h3 python -m SimpleHTTPServer

Once the HTTP server is up, run following commands on guest VM 1 to
access the server ::

	mininet> h1 curl 10.0.0.2:8000
	mininet> h2 curl 10.0.0.2:8000

.. note::In order to access the server of h2 that you will need to stop
   the SimpleHTTPServer on h3 and switch to h4.

Finally, let’s capture some VXLAN packets using Wireshark. To use
Wireshark GUI, we should first log into the VNC of the router use noVNC
provided by EZSetup. Then, type ``sudo wireshark-gtk`` in a terminal to
launch. Before we can get some packets, we need to choose on which
interface we want to capture. Click the first button in the toolbar and
check the first network interface. Click “Start” to start the capture.

.. figure:: /xie/media/ONmedia/ON_img6.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 6** Wireshark interface selection dialog

Your capture list pane may be overwhelmed by the incoming packets, so
let’s apply some filtering rules. Type “vxlan” or “udp.port==4789” (both
without quotes) into the filter text box and hit enter, all the packets
that are not VXLAN packet will disappear. Type the following command on
guest VM 1 to generate some VXLAN packets for capturing ::

	mininet> h1 ping 10.0.0.2 -c 3

You should see the result that looks like **Figure 7**.

.. figure:: /xie/media/ONmedia/ON_img7.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 7** Wireshark VXLAN traffic capturing window

We can see the ping requests from :font:`h1` to :font:`h3` and the responses from :font:`h3` to
:font:`h1`, as well as the ARP requests. The details of a packet will show up
once you select a packet from the list. In the above picture, we can see
the VNI of the packet is 100, the source UDP is 38599 and the
encapsulated ICMP packet, etc. You can try some other protocols to see
if the result matches your anticipation.

Lab Exercise 2
~~~~~~~~~~~~~~

1. What is your command for adding the VTEP port on guest VM 2?

2. What are the results when you try to access the HTTP server on :font:`h4`
   from :font:`h1` and :font:`h2`? What do they mean?

3. Start the packet capturing using Wireshark on the router VM. Then
   create an HTTP server on h4 using the command ::

	   mininet> h4 python -m SimpleHTTPServer

   And access it from :font:`h2` using command ::

	   mininet> h2 curl 10.0.0.2:8000

   What have you observed from the Wireshark? For example, what is the
   VNI of the VXLAN packets? What about the “Server” field in the HTTP
   response header?

Task 3: Deploy GRE Network
--------------------------

Similar to VXLAN, we can also use GRE to separate networks of different
tenants by encapsulating tenant traffic in tunnels. GRE was developed by
Cisco Systems to carry any OSI layer 2 or layer 3 protocol over an IP
network. GRE endpoints, like VTEPs, are responsible for routing,
encapsulation and decapsulation of the GRE packets. The format of a GRE
packet is shown in **Figure 8**. Compared to the VXLAN packet, GRE packet
does not have a UDP header, and a GRE header is in place of the VXLAN
header. GRE protocol does not use a specific tag to denote tunnel ID
like VNI. Instead, it provides an optional (or reserved) field that can
be used as the tagging field. The packet encapsulation and decapsulation
process are much the same as VXLAN, so it is not described here.

.. figure:: /xie/media/ONmedia/ON_img8.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 8** GRE message packet format

To create the GRE network, we should first delete the VXLAN port we
created in the last section. Type the following command on guest VM 1 to
remove the VTEP port ::

	mininet> sh ovs-vsctl del-port s1 vtep

Then, we can add the GRE endpoint port ::

	mininet> sh ovs-vsctl add-port s1 gre -- set interface gre type=gre
	option:remote_ip=192.168.2.20 option:key=flow ofport_request=10

Commands for guest VM 2 are similar to guest VM 1. 

.. note:: It is worthwhile to mention that we do not 
          clear the flow rules added previously because
          those flow rules are VXLAN/GRE independent. 
		  
To test the connectivity of the GRE network, we can type the following commands on guest VM 1 ::

	mininet> h1 ping 10.0.0.2
	mininet> h2 ping 10.0.0.2

Also, to verify that hosts do not communicate with hosts in other
tenants, let’s create an HTTP server on :font:`h3` on guest VM 2 ::

	mininet> h3 python -m SimpleHTTPServer

and access it from both :font:`h1` and :font:`h2` ::

	mininet> h1 curl 10.0.0.2:8000
	mininet> h2 curl 10.0.0.2:8000

Finally, we can use Wireshark to inspect GRE packets on the router VM.
Type “GRE” (without quotes) into the filter input textbox to filter out
GRE packets like it is shown in **Figure 9**.

.. figure:: /xie/media/ONmedia/ON_img9.png
   :align: center
   :alt: alternate text
   :figclass: align-center

   **Figure 9** Wireshark VXLAN traffic capturing window

We can see from here that the original HTTP packet along with its
ethernet headers are wrapped in the GRE packet, and the Outer Ethernet
Header and IP Header points to the network location of the guest VM.
Please try some other protocols and compare GRE protocol to the VXLAN
protocol.

Lab Exercise 3
~~~~~~~~~~~~~~

1. From what you captured using Wireshark, can you tell where is the
   tunnel ID in a GRE packet?

2. What are the differences between GRE and VXLAN? If you are going to
   build a cloud infrastructure that supports hundreds and thousands
   of tenants, which protocol will you choose for network isolation?
   Why?

What to submit 
--------------

Save your answers (with screenshots) to the above questions into a PDF
file and name the file as ``overlay-network-ans.pdf``.

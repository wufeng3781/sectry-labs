.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

================
TCP/IP Security
================


Introduction
-------------

**Overview:** The Internet protocol suite, also known as TCP/IP, is the foundation of the modern Internet. 
This suite provides various protocols that lie upon the Internet Protocol (IP) for end-to-end data communications. 
Vulnerabilities in TCP/IP protocols may have serious effects on the upper layer protocols and applications and can endanger communication and data security. 
In this lab, we will look into three types of TCP/IP protocols, learn how they work and analyze their vulnerabilities, and finally show the ways to attack them.

**Objectives:** Upon completing the experiments, students should:

* Be familiar with the operation procedure and data format of ARP, TCP, and DNS protocol. 
* Understand how ARP spoofing attack, TCP SYN flooding attack, and DNS cache poisoning attack works and have the ability to conduct these attacks in an experiment environment. 
* Understand the vulnerabilities of ARP, TCP, and DNS protocols, and give feasible protection solutions.

**Required Knowledge:** Students are required to have the following prerequisite knowledge for this lab:

* The usage of the text-based terminal and basic Linux commands.
* Knowledge of accessing a remote Linux server using SSH.
* Basic understanding of Linux networking and some popular network protocols.

**Background:**

  |Description|
  
  For more information about |Platform|, please see bundled `user manual file`_.
 
  **Secure Shell(SSH)** is a network protocol that allows data to be exchanged over a secure channel between two computers. 
  Encryption provides confidentiality and integrity of data. SSH uses public-key cryptography to authenticate the remote computer and allow the remote computer to authenticate the user, if necessary.
  
  For more information about SSH, please see https://wiki.archlinux.org/index.php/Secure_Shell.
 
  **tcpdump** is a common packet analyzer that runs under the command line. 
  It allows the user to display TCP/IP and other packets being transmitted or received over a network to which the computer is attached. 
  Distributed under the BSD license, tcpdump is free software. 
  
  For more information about tcpdump, please see its manual page: `<https://www.tcpdump.org/tcpdump_man.html>`_.

  For tcpdump and wireshark filtering syntax, please see `<http://www.tcpdump.org/manpages/pcap-filter.7.html>`_.
 
  **Wireshark** is a free and open-source packet analyzer. 
  It is used for network troubleshooting, analysis, software and communications protocol development, and education. 
  Wireshark is very similar to tcpdump, but has a graphical front-end, plus some integrated sorting and filtering options. 
  
  For more information about Wireshark, please see its User\'s Manual: `<https://www.wireshark.org/docs/wsug_html_chunked/>`_.
 
  In information and communications technology, a **Request for Comments** (RFC) is a type of publication from the technology community. RFCs may come from many bodies including from the Internet Engineering Task Force (IETF), the Internet Research Task Force (IRTF), the Internet Architecture Board (IAB) or from independent authors. The RFC system is supported by the Internet Society (ISOC). 
  
  For more information about specifications of some popular network protocols, please refer to the RFC official documentation: `<https://tools.ietf.org/rfc/index>`_.
 
  **Ettercap** is a comprehensive suite for man in the middle attacks. 
  It features sniffing of live connections, content filtering on the fly and many other interesting tricks. 
  It supports active and passive dissection of many protocols and includes many features for network and host analysis. 
  It can be used as an alternative tool in this lab to launch Man-in-the-middle, DNS cache poisoning, and ARP cache poisoning attack. 
  
  For more information about Ettercap, please see `<https://github.com/Ettercap/ettercap>`_.
 
  **Scapy** is a powerful interactive packet manipulation program. 
  It is able to forge or decode packets of a wide number of protocols, send them on the wire, capture them, match requests and replies, and much more. 
  It can easily handle most classical tasks like scanning, tracerouting, probing, unit tests, attacks, or network discovery. 
  It also performs very well at a lot of other specific tasks that most other tools can’t handle, like sending invalid frames and injecting your own 802.11 frames. 
  Some of the scripts used in this lab is written with the help from scapy. 
  
  For more information about scapy, please see `<https://scapy.readthedocs.io/en/latest/>`_.
 
**Enviornment:**

In this lab, students can access three virtual machines (VM) from |Platform|, attacker, victim, and observer VM. 
The network topology looks as shown in `Figure 1`_, the VM properties are listed in `Table 1`_. 
Please refer to the EZSetup dashboard for the actual public IP addresses and passwords.

.. _Table 1:

.. list-table:: **Table 1** VM properties and access information
   :header-rows: 1

   * - Name
     - Image
     - RAM
     - VCPU
     - Disk
     - Login Account
   * - ts-attacker
     - tcpipsecurity-attacker
     - 2GB
     - 1
     - 20GB
     - See EZSetup
   * - ts-victim
     - tcpipsecurity-victim
     - 2GB
     - 1
     - 20GB
     - See EZSetup
   * - ts-observer
     - tcpipsecurity-observer
     - 2GB
     - 1
     - 20GB
     - See EZSetup

.. _Figure 1:

.. figure:: /xie/media/tcpip_media/lab/fig_1.png
	:alt: alternate text
	:figclass: align-center

	**Figure 1** Lab network topology


Task 1: ARP Spoofing Attack
---------------------------
	
The Address Resolution Protocol (ARP) is an important link layer protocol for mapping an upper layer protocol address to a lower layer hardware address, such as IPv4 address to MAC address. 
ARP is usually used in host discovery within a single network, and it is not routed across different networks.

The message format of ARP is shown in `Figure 2`_. The numbers above the table measure the length in bytes of a field, and the numbers on the left of the table give the offset of a field of the ARP packet header. The **hardware type** field specifies lower layer protocol type, e.g., hardware type for Ethernet is 1. The **protocol type** field specifies the EtherType value of upper layer protocol, e.g., 0x0800 for IPv4. **Hardware address length** field defines the length of following hardware address of sender and target, and **protocol address length** defines the length of sender and target’s protocol address. **Operation** field has four possible values: 1 for ARP request, 2 for ARP reply, 3 for RARP (Reverse Address Resolution Protocol) request, and 4 for RARP reply. The content and size of following hardware and protocol addresses are decided by previous fields.

.. _Figure 2:

.. figure:: /xie/media/tcpip_media/lab/fig_2.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 2** ARP message format

Let’s assume the hardware type is Ethernet and upper layer protocol is IPv4. 
To find the hardware address of a target host within the same network for the first time, a host will broadcast an ARP request with its MAC and IP address, as well as target host’s IP address to the network. 
At this moment, the target’s MAC address is not known, so it is set to FF:FF:FF:FF:FF:FF. 
Then, upon receiving this request, the target host will reply an ARP response with its MAC address. 
Both hosts will also insert an entry in their ARP cache table with each other’s IP and MAC address to save for future queries until the entry expires.

Because ARP does not authenticate replies on the network, forged ARP replies sent by a malicious host can be cached by the ARP request sender, even when it does not have the asked hardware and protocol address. 
As a result, the victim will send all of its traffic to a specific host to the malicious host, making the malicious host a “man-in-the-middle.” `Figure 3`_ shows the process of the ARP spoofing attack.

.. _Figure 3:

.. figure:: /xie/media/tcpip_media/lab/fig_3.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 3** ARP spoofing attack process

Sometimes a machine needs to announce its ownership of an IP address on a network. 
To accomplish this it will send a “gratuitous ARP reply”, which is an ARP reply but without a prior ARP request. 
The receiving hosts will update their ARP cache table to record this change. 
This is useful for a moving IP address because the IP address may be bound to different devices from time to time. 
Instead of other hosts asking for its MAC address, gratuitous ARP reply can be more efficient. 
But a malicious host can also exploit this to poison the ARP table of other hosts.

We can start an ARP spoofing attack using the arping tool. 
Arping is a Linux command line tool for sending and receiving ARP requests and replies. 
To start an attack, use the following command to send gratuitous ARP replies to a victim. ::

	$ sudo arping -q -c 3 -P -S <spoofed_ip> -I <interface> <target_ip>

.. admonition:: Meaning for options above
	
	-q: suppress output
	
	-c: number of packets to be sent
	
	-P: send ARP replies instead of requests
	
	-S: override the packet sender’s IP
	
	-I: network interface through which the packets will be sent

To view all the ARP entries in the cache table, please use this command. ::

	$ sudo arp -a

To delete an ARP entry from the cache table, you can use the following command. ::

	$ sudo arp -d <IP address>


Lab Exercise 1
~~~~~~~~~~~~~~

 1. On the attacker VM, send spoofed ARP replies to the victim VM with the IP address of the observer VM. 
 Then, try to ping the observer from the victim, and capture incoming ICMP packets on the attacker. 
 What command(s) do you use for this attack? 
 How do you know your attack is successful?
 
 2. Move into ``~/labs/tcp_ip_security/`` directory and run the arpspoof tool from attack VM: ::
	
	$ sudo ./arpspoof <victim IP> <observer IP>

  This will carry out an ARP spoofing attack on both the victim and the observer. 
  Then, start a simple HTTP server on the victim using the command below. ::
 
	 $ sudo python -m SimpleHTTPServer

  After that, try to visit the website (10.0.0.20:8000) hosted on the victim from the observer’s browser. 
  What do you see on the attacker’s terminal? 
  What does this mean?

 3. Can you think of any way of preventing ARP spoofing attack?


Task 2: TCP SYN Flooding Attack
-------------------------------
	
Transmission Control Protocol is an essential protocol of the TCP/IP protocol suite. 
It is a transport layer protocol which provides highly reliable and ordered host-to-host communication in computer networks. 
Many Internet applications and high-level protocols rely on TCP, such as World Wide Web (HTTP), Email (SMTP) and Secure Shell (SSH). 
On the lower level, TCP uses the IP protocol, which is responsible for addressing hosts and routing data between hosts.

.. _Figure 4:

.. figure:: /xie/media/tcpip_media/lab/fig_4.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 4** TCP Connection between two remote processes

TCP is connection-oriented, so applications using TCP need to establish a connection before exchanging data. 
TCP uses a socket, which is an IP address and TCP port pair, at each end of a connection so application processes TCP can be differentiated. 
TCP also supports full duplex, which means both sides of a TCP connection can send or receive data streams simultaneously. 
`Figure 4`_ illustrates how a TCP connection between two processes of two different hosts works.

To understand how TCP operates to achieve a reliable communication, we should first take a look at the TCP message format, which is shown in `Figure 5`_. 
The size of a TCP packet header is 20 bytes unless additional options are present. 
The **source port** and **destination port** fields are the sender and receiver TCP ports of a connection. 
The **sequence number** identifies the position of a packet’s first octet in all the data of the current session. 
When SYN is set to 1, the sequence number is the initial sequence number and the corresponding acknowledgment number is this sequence number plus 1. 
The **acknowledgment number** is the sequence number that the sender expects for the next incoming TCP packet when ACK flag is set. 
**Header length**, or data offset, denotes the TCP header size in 32-bit words because the length of the options field is variable. 
The **reserved field** is for future use and is set to zero.

.. _Figure 5:

.. figure:: /xie/media/tcpip_media/lab/fig_5.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 5** TCP message format

The following 9 bits are control flags. 
The **SYN** and **FIN** flags are set respectively when establishing and terminating a TCP connection. 
The **ACK** is always set after the initial SYN packet is received and indicates the acknowledgment field is significant. 
The **RST** flag means the sender wants to reset the connection. 
The **URG** flag signifies this TCP segment contains urgent data. 
If it is set, the **urgent pointer** indicates the offset of last urgent data byte from the sequence number. 
The **PSH** flag asks the receiver to push buffered data to its application. 
The **window size** field signifies the number of unacknowledged data octets the sender wants to receive, and its value usually depends on the amount of memory available to this connection. 
The **checksum** field is for error checking by the receiver. 
And the **options** field is optional, with zero paddings to make sure data starts on a 32bit boundary.

.. _Figure 6:

.. figure:: /xie/media/tcpip_media/lab/fig_6.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 6** Packet flow in a TCP session

`Figure 6`_ shows the simplified process of the packet flow during a TCP session. 
To establish a TCP connection, clients on both sides use a three-way handshake. 
The client that initiates the connection first sends a packet with SYN flag set to its receiving client (or TCP server for short), and the sequence number is set to a random number X. 
Then, the server replies an SYN-ACK to inform the client that connection request is received. 
The acknowledgment number is set to X+1, and the sequence number is chosen by the server randomly, i.e., Y. 
Finally, the client sends back an ACK to the server with a sequence number of X+1 and an acknowledgment number of Y+1. 
The three-way handshake is to make sure both sides of a connection are willing to connect and agree on the connection parameters. 
The connection termination uses a similar four-way handshake, which will not be covered in detail in this guide.

In the TCP three-way handshake process, when the server receives the initial SYN, it will store the pending connection information in its memory. 
This is called a half-open connection because only the server side confirms the connection. 
We can easily create half-open connections by sending SYN to the server without replying to the received SYN-ACK. 
As there is only finite size of a queue in the memory to store TCP connection information, we can overflow it by intentionally creating many half-open connections in a short period. 
Once there is no more space for storing connection information, the server will stop accepting new connections, eventually blocking other legitimate users from connecting to the server.

This is called TCP SYN flooding attack, which is a form of denial-of-service (DoS) attack. 
The process is illustrated in `Figure 7`_. 
Although after a certain time the half-open connection data will be removed from memory, the attacker can always send SYN faster that the victim can process, thus making this attack very efficient. 
The key to a successful attack is to spoof random source IP addresses in the SYN packets so that this TCP traffic seems to come from legitimate users. 
Otherwise, the firewall may block our attack if too many SYN packets are sent from the same source. 
Also, if the host with a source IP address exists and it receives the SYN-ACK from the server, it will reply with an RST, which remove the half-open connection from the server’s memory. 
Thus, the randomness of the source IP address is very important.

.. _Figure 7:

.. figure:: /xie/media/tcpip_media/lab/fig_7.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 7** TCP SYN flooding attack process

To conduct a TCP SYN attack, you can use tools like ``hping3``. 
``hping3`` is a command-line TCP/IP packet assembler and analyzer. 
It supports TCP, UDP, and raw IP protocols, and can be used for firewall testing, port scanning, TCP/IP attack auditing, etc. 
You can use the following command to start a TCP SYN flood attack. ::

	$ sudo hping3 -d <packet_len> -S --flood --rand-source -p <target_port> <target_host>

.. admonition:: Meaning for options above
	
	-c: number of packets to be sent
	
	-d: packet data length in bytes
	
	-S: set TCP SYN flag
	
	--flood: send packets as fast as possible, hide incoming replies from the output
	
	--rand-source: send out packets with random source IP addresses
	
	-p: destination port

You need to specify a valid destination with an open port for this attack to work. 
For more details about ``hping3``, please refer to the manpage. ::

	$ man hping3

You can check all the TCP connections using ``netstat -antp``. 
This command will show the local and remote IP address and port of a connection, as well as the connection state and the program bound to this connection. 
The status field has a few possible states, including ``ESTABLISHED``, ``LISTEN``, and ``CLOSE``. 
Please refer to the manpage of netstat for a complete description of these states.

Lab Exercise 2
~~~~~~~~~~~~~~

 1. Here, we are going to capture the TCP traffic when you visit a website. 
 Please start a traffic capturing using Wireshark with the following filter options. ::
 
	ip.src_host == 144.167.4.20 || ip.dst_host == 144.167.4.20

  and then make an HTTP request to the `<http://www.ualr.edu>`_ (not `<http://ualr.edu>`_) using ``curl``: ::
 
	 $ curl www.ualr.edu

  Looking at your capturing result, what is the data length of the TCP packets during the three-way handshake? 
  How many TCP packets do you capture (including HTTP packets)?
 
 2. Log in to the attacker machine, launch a TCP SYN flooding attack on the victim’s port 23. 
 Use ``netstat`` tool to check the connection status on the victim before and during the attack. 
 What do you observe? To see if your attack works, try to ``telnet`` into the victim from the observer machine. 
 Can you connect to the victim? 
 If you are connected to the victim before the attack begins, will you lose the SSH connection when the attack is going on?
 
 3. There are several countermeasures for defending against TCP SYN flooding attack. 
 One is called SYN cookie. It uses a specially crafted sequence number in the SYN+ACK and discards SYN queue entry in the three-way handshake. 
 This defense is on by default. You can check your current settings using: ::
 
	$ sudo sysctl -n net.ipv4.tcp_syncookies

  and turn it on by: ::
	
	 $ sudo sysctl -w net.ipv4.tcp_syncookies=1

  Turn on SYN cookie and see if your attack still works. 
  Please briefly explain why SYN cookie can protect the system from SYN flooding attack.


Task 3: DNS cache poisoning attack
----------------------------------

Most of the web services and resources today use the domain names as location identifications. 
Domain Name System (DNS) is a decentralized system responsible for easy-to-remember domain names to IP addresses translations (DNS records). 
To maintain countless records, DNS uses a distributed hierarchical database system. 
The top of the hierarchy is the root name servers, which directly answer root domain queries or return authoritative name servers for other queries. 
Below that are the authoritative name servers, which are usually owned by companies and organizations and give answers to domain names in a certain zone managed by them. 
For instance, top-level domain (TLD) name servers are responsible for resolving top-level domains like .com and .us. 
Finally, local domain name servers are often deployed at the edge of the network to proxy and cache DNS query results for performance purpose.

User’s DNS queries are often sent to its default local DNS server. 
A local DNS server will first look at its cache to find if there already exists a valid answer, and if there is, it will directly reply to the request sender. 
Otherwise, it will ask root and authoritative DNS servers for answer. 
Let’s assume a user asks its local DNS server for the IP address of a domain, e.g., netid.ualr.edu. 
If a valid cache does not exist, local DNS server will first ask the root server to see it has the domain’s DNS record. 
The root domain will reply the IP address if it has the DNS record, or it will return the address of the TLD name server that manages the top-level domain of the requested domain (.edu). 
The above process is the same between local DNS server and TLD name server, except the TLD server will return the Authoritative DNS server for that domain. 
Finally, local DNS can reply user with the IP address of netid.ualr.edu or Non-Existent Domain (NXDomain) if no record for that domain is found. 
`Figure 8`_ depicts the above stated DNS iterative resolving process.

.. _Figure 8:

.. figure:: /xie/media/tcpip_media/lab/fig_8.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 8** DNS iterative queries resolving process
		
DNS protocol defines many DNS record types, and the most used ones are A, CNAME, NS, and MX. 
Type A records are address records, which are used for mapping domain names to IP addresses. 
CNAME record, or canonical name record, is an alias of another domain like www.ualr.edu is an alias of ualr.edu. 
NS records are name server record, which maps DNS zones to their authoritative name servers. 
Finally, MX is a mail exchange record, which gives the message transfer agents for a domain.

The message format of DNS is shown in `Figure 9`_. 
DNS messages are based on UDP, hence, there is no connection between the DNS server and the client. 
To determine which DNS packet is the response to a given query, DNS uses (source IP address, source UDP port, destination IP address, destination UDP port, identification) tuple. 
The identification (ID) here is a 16-bit unsigned integer, which is randomly generated by the DNS request sender, and the response has the same ID as the request. 
The flags field indicates the properties of the DNS packet and the DNS server, e.g., the packet is a query or answer, and if the DNS server supports recursion query. 
The following fields indicate the number and content of the DNS questions and answers. 
The questions field contains one or more DNS questions; each question contains a domain name and the DNS record type that is being asked. 
The next three sections (answers, authority, and additional information) share a common format called resource record (RR), which contains the domain name, record type, time-to-live and resource value. 
The answers section has the DNS records to the questions. 
Authority section gives the authoritative server information about the queried domain. 
Additional information section contains other DNS records that are relevant to the questions and may be used sometimes later.

.. _Figure 9:

.. figure:: /xie/media/tcpip_media/lab/fig_9.png
		:alt: alternate text
		:figclass: align-center
		
		**Figure 9** DNS message format

DNS is not encrypted by default, which makes DNS vulnerable to many attacks. 
Moreover, DNS attacks usually affect not only the server itself but clients that use it. 
Thus, a successful DNS attack can be very efficient and influential. 
DNS cache poisoning is a form of attack in which spoofed DNS records are injected into DNS server’s cache, making it returns incorrect IP addresses for certain domains. 
The attacker can force compromised DNS server users to be directed to the wrong hosts chosen by the attacker, and trick them into downloading malicious contents or leaking sensitive information.

To perform a DNS cache poisoning attack, the attacker needs to get the corrupted DNS records cached in the DNS server, by exploiting flaws either in DNS software or protocol. 
If the attacker is on the same network with the DNS server and he/she can sniff the packets sent by it, this attack would be much simpler to perform. 
For instance, the attacker wants to insert a DNS record that says www.google.com is at 192.168.0.10. 
The attacker can first send a DNS request to the server asking about that domain. 
If the server has no record of that domain in the cache or the cached record expires, it will send out a query to the root or authoritative DNS server. 
The attacker listens for the server query in the network, learning its source and destination IP and port number, as well as the identification number. 
Then, the attacker generates a spoofed DNS response with the corresponding information except for a faked answer. 
If this response beats the one returned from the genuine server, the wrong DNS record will be cached on the server, and hence the attack succeeds.

This attack method has some obvious disadvantages, and will be very limited in real life because of the following facts:

  #. If the attacker is not in the same network with the target DNS server, or the underlying network does not allow packet sniffing, the attack would have no idea of the source port, destination IP address and identification number of server’s DNS query. In addition, DNS server software now use random query UDP port and identification number,  it is very difficult to create a legitimate reply by purely guessing these numbers.
  
  #. Even if the attacker can guess all the information he/she need to create a spoofed reply, he/she still needs to make sure the spoofed packet arrives before the real one does. If not, the correct response will be cached, usually for hours or days. This makes another poisoning attack of the same domain impossible for a while because the server will not initiate a query before cache expires.
  
  #. Some DNS software enforces a spoof-defense mechanism called Domain Name System Security Extensions (DNSSEC). DNSSEC requires DNS resource records to be signed by asymmetrical cryptography. Without the private key, it is impossible for the attacker to forage an authenticated DNS response.

For the sake of experiment simplicity, we use Dnsmasq as the DNS server. Dnsmasq is a networking service toolkit which provides DNS, DHCP, and network boot functions. When acting as a local DNS server, Dnsmasq forwards DNS queries to the upstream DNS server and caches responses. To make the attack easier, we made the following changes to Dnsmasq and its configurations:

  #. Reduce the value space of DNS identification number from 2^16 to 2^8;
  
  #. Use a fixed DNS query port 8053. In other words, DNS server sends DNS requests through a single port 8053;
  
  #. There is only one upstream DNS server, which is at 8.8.8.8;
  
  #. DNSSEC features are disabled.

In order to mitigate cache’s impact on the attack, we do not try to poison the target domain directly. 
During the attack, the attacker floods the victim DNS server with queries and replies of nonexistent domains like 4c6ef977.example.com, hoping the spoofed replies beat the real ones. 
Because the server does not have cached answers for these domains, it will send queries the upstream DNS server with random identification, fixed source/destination IP addresses and ports. 
Also, as the identification number space is decreased to [0, 2^8-1], it is feasible for the attacker to guess the right identification number in a short time. 
Furthermore, in every DNS reply sent by the attacker, we set the made-up domain as a CNAME to the target domain along with the A record for the target domain, e.g. ::

	CNAME 4c6ef977.example.com → ualr.edu
	A ualr.edu → 192.168.0.10

Once the bogus DNS reply is accepted by the server, the A record of target domain will also be cached. 
Thus, the attack is completed.

To bring up the Dnsmasq service, please stop the default DNS service and start the Dnsmasq service using the following commands. ::	

	$ sudo systemctl stop systemd-resolved.service
	$ sudo dnsmasq -C /etc/dnsmasq.conf -Q <query_port_number>

We also provide a tool in the ``~/labs/tcp_ip_security/`` directory for performing DNS cache poisoning attack, and you can use it by executing the following command. ::

	$ sudo dnspoisoning -u <upstream_dns> -d <dmoain> -s <domain_ip> <target_dns_ip>:<target_dns_port>

For example, the victim DNS server is at 192.168.0.10, and it uses UDP port 9000 as query port and 8.8.8.8 as upstream DNS server. 
You can insert a spoofed record to point www.google.com to 192.168.0.20 by... ::

	$ sudo ./dnspoisoning -u 8.8.8.8 -d www.google.com -s 192.168.0.20 192.168.0.10:9000

Also, Dnsmasq caches records in the memory. 
To clear cached DNS records, you may use the following command to stop Dnsmasq first. ::

	$ sudo killall dnsmasq

And please check cached DNS record by this command. ::

	$ sudo pkill -USR1 dnsmasq && cat /var/log/syslog | grep dnsmasq

Lab Exercise 3
~~~~~~~~~~~~~~

 1. Use ``dig`` tool to make a DNS query about domain “ualr.edu” ::
 
		 $ dig ualr.edu
			
  Use Wireshark to capture the DNS request and response with the following filter options: ::
	
		 dns.qry.name == ualr.edu
	
  What is the flags field of the DNS request? What is the query type (A, CNAME, NX or MX)? What is the answer?
 
 2. Start Dnsmasq on the victim VM. 
 Now, switch to the observer VM and make it use the victim VM as its default DNS server by editing the default nameserver IP address in ``/etc/resolv.conf`` to the IP of the victim VM.  ::
 
	$ sudo nano /etc/resolv.conf
	
  Then, use the DNS poisoning tool to insert a spoofed record for pointing ualr.edu to the attacker’s machine. 
  Finally, stop the apache2 server, enter the ``fake_site`` directory and start an HTTP server on the attacker VM using ::
 
	 $ sudo systemctl stop apache2.service
	 
	 $ cd ~/labs/tcp_ip_security/fake_site
	 
	 $ sudo python -m SimpleHTTPServer 80
	
  Open a browser on the observer VM and visit `<http://ualr.edu>`_. 
  Also, use Wireshark to capture DNS packets on the victim during the attack. 
  What command(s) do you use for this attack? Also, describe your observations.


What To Submit
--------------

Save your answers (with screenshots) to the above questions into a PDF file and name it to ``tcp-ip-security-ans.pdf``.

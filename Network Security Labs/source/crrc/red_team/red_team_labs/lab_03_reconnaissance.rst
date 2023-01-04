======================
Lab 3 - Reconnaissance
======================
--------
Overview 
--------

Your job is to do some initial **passive** reconnaissance of a target.
You should submit only the screenshots of the results from the queries
that you run. Please submit all of the screenshots in one Word document
or PDF. Do not submit them as separate images.

.. note:: 
   When running the following tools be very careful and if you think
   that the tool you’re about to run is not passive in any way **stop** and
   **ask**. Do not a run a tool without first understanding what it does.

**Target: DSU.EDU**

Whois & DNS & Mail information
------------------------------

Perform the following using online tools of your choosing:

1. Gather DNS information

2. Gather site information

3. Gather mail information

Recon-ng
--------

Perform the following using recon-ng:

1. Create a workspace for your target, use your first initial + last
   name as the name

2. Add a company (Dakota State University)

3. Add the **dsu.edu** domain name

4. Run the following modules within Recon-ng:

   a. recon/domains-hosts/bing_domain_web

   b. recon/domains-hosts/google_site_web

   c. recon/domains-hosts/netcraft

   d. recon/hosts-hosts/resolve

   e. recon/hosts-hosts/reverse_resolve

   f. recon/domains-contacts/pgp_search

   g. recon/contacts-credentials/hibp_paste

5. Create an HTML report with your name as the CREATEDBY and DSU as the
   CUSTOMER

6. Open the HTML report in a browser and take a screenshot of the
   summary pane. This should have you name at the bottom of the page.

Discover Scripts
================

Install the Discover Scripts from Lee Baird on your Kali VM
(`<https://github.com/leebaird/discover>`_) and complete the following:

1. Launch the discover.sh file

2. Once it is running, choose **1. Domain** and then select **1.
   Passive**

3. Enter in your name as the company name and **dsu.edu** as the domain
   name

4. Once the discover scripts have finished, open the report in a browser
   and take a screenshot

Your Choice
-----------

1. Find another tool that is used to perform information gathering and
   footprinting of a target

2. Install/Run the tool and collect its output

3. Explain how the information provided by the tool could be useful

4. Do not use active tools such as nmap!

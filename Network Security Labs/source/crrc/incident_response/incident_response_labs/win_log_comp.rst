*******************************************************
Lab 9 - Sysmon, Windows Logs - Compromise Investigation
*******************************************************

In this lab, you’ll use Windows logs and Sysmon logs to investigate a
possible breach.

1. If you haven’t already, start the Graylog Virtual Machine.

   a. When Graylog boots up, you should see a message in the VM with its
      IP address.

2. Open Graylog in a web browser, and log in.

   a. Default username and password is admin

3. The dataset for this lab can be obtained by limiting the source and
   searching for messages over all time.

   a. In the search query, enter source:Host-Compromise and click enter.

      i. You should see 3416 messages

4. Network indicators noticed something suspicious occurring on the
   Windows machine in the logs. Nothing else is known at this point. See
   if you can figure out what happened. Ideally, spend some time looking
   through the logs on your own. If you get stuck, go through the
   walkthrough, continuing with step 5.

   Answer the following:

-  What is the “malicious” executable in this case?

-  Where did it come from, how did it get on the system?

-  Can you identify it? Is it a custom-written tool?

-  Who was logged on at the time?

5. Let’s start by looking at processes and network connections. Most of
   the time, attackers and malware will traverse the network at some
   point.

   a. Generate a Quick Values chart for EventID 3

   b. ``source:Host-Compromise`` AND EventID:3

   c. Are there any processes that shouldn’t normally be making network
      connections?

6. PowerShell.exe certainly could make network connectinos, but not
   normally. This might be something to check on.

   a. Click on the plus/magnifying glass to add PowerShell to the
      search, and click enter.

   b. Generate a quick values chart for DestinationIP to see where
      PowerShell is connecting

      i. This is a private IP address that we don’t necessairily know
         about – maybe something to keep investigating.

   c. Generate a QuickValues chart for ProcessID

      i. It looks like just one PowerShell process is running, making
         all the network connections

   d. Take a look at the histogram. It looks like there are about 12
      messages every minute – that is, 12 network connections every
      minute. It’s fairly consistent – this could be indicative of some
      beaconing activity.

7. Let’s see if we can find when that PowerShell process was created
   using Sysmon EventID 1.

   a. ``source:Host-Compromise`` AND ``*powershell*`` AND ProcessID:2220 AND
      NOT EventID:1

   b. Take a look the event.

      i.   CommandLIne: This is how this PowerShell process was created.
           Notice the encoded payload.

      ii.  The parent image is cmd.exe -this means it was cmd.exe that
           started Powershell.exe

      iii. Notice the ParentCommandLine, and the clickme.bat file

8. Let’s see if we can find anything else in the logs on clickme.bat

   a. ``source:Host-Compromise`` AND ``*clickme.bat*``

   b. There are 10 events returned: one process create, one process
      terminate, one 4688 process create, and 6 file stream creations.

   c. The process creates are from the starting of the powershell.exe
      process

   d. Look at the Image field in the 6 file stream events, or generate a
      QuickValues.

      i. All are created using chrome.exe

9. It seems the file was downloaded using Chrome – can we find where it
   was downloaded from?

   a. Looking at network connection events for chrome.exe, there are 222
      events, and no good way to correlate with the clickme file
      download other than time. If the user visited multiple sites
      around the same time, that. Can become difficult. This is where
      correlating network events can be useful!

Summary:

A malicious .bat file was downloaded using chrome, and was subsequently
executed. It creates a powershell.exe process that beacons to
192.168.1.104. Through looking at the encoded payload, you might have
been able to find this is PowerShell Empire.

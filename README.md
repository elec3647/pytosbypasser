# pytosbypasser
## Python Terms of Service Bypasser
An intelligent form filler client that can bypass the TOS agreements that routers present on public wifi.

A client to,
  * anonymize MAC addresses using the very handy [spoof-mac](https://feross.org/spoofmac/) utility before connecting to a network. 
  * anonymize user data using free public Wifi access points.
  * bypass those pesky TOS popups that kill your internet connection in coffee shops when it asks you to accept the terms of service.
  * detect popups for paid service and autofill or ignore.

## Project Goals
* Create a client that "learns" how to fill out forms as a human would.
  * Read and analyze form fields and attempt to fill them. 
  * Use anonymized user data to prevent data collection and user tracking.
* Log forms that fail to be bypassed and send information to a central server for further analysis and global learning/updates of all TOS Bypasser clients.


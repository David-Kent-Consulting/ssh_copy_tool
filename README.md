SSH Copy Utility That Demonstrates a Real World Use Case of python's pysftp library
===================================================================================
This utility's purpose is to copy files from a source Linux VM to a remote Linux
VM using the python pysftp library. It copies all of the files from a source
directory to a target directory on the remote host. This tool by design will not
recursively copy files. This tool sets the file access mode of remote files to
660. It can with the correct option remove files on the remote hosts that are not
present on the source host. We note that even today many sysadmin and DBA admin
types still rely on rsync or secure NFS. We do not care for either approach
because: 1) rsync is not secure; 2) NFS is not secure unless setup to use
encryption, and; 3) encrypted NFS is difficult to setup and maintain.

DATE OF LATEST UPDATE
===================================================================================
26-June-2023

LICENSE REQUIREMENTS
===================================================================================
This code is public domain and is considered open source. The code is provided
for the purpose of demonstrating a practical use of the pysftp tool. The code is
provided without guarantee. You may use this code in part or in whole as you see
fit. You may modify the code. You agree that use of this code is solely at your
own risk.

WARNING!
===================================================================================
This tool should be used by experienced system and DBA types with python
experience. We do not advocate its use by the inexperienced. You should not kiddie
script this. Know what you are getting into. Get your training in order.

CAEATS
===================================================================================
Make sure your SSH private key is kept secure. We recommend an access mode of 0600
for this file. Make sure when testing that your defined timeout in
/etc/sshd/sshd_config is appropriately defined. This utility should run fine
when called from cron.

REQUIREMENTS
===================================================================================
The following requirements are based on when these examples were created as of 30-May-2023. Technology changes fast, so be certain to
consider testing at more current versions.

| Package                           |  Version      |  Source                                                                                                       |
|-----------------------------------|---------------|---------------------------------------------------------------------------------------------------------------|
| A Fedora kernel                   | V7 or V7      | We have tested on RHEL 7.9 and 8.x. We have tested on OLE 7.9, 8.x, and 9.0. We have not tested on Ubuntu.    |
| Python                            | 3.6x or 3.8x  | We strongly recommend 3.8x or later since 3.6x is deprecated.                                                 |
| PIP                               | Version 3     | Sets with your Linux distro.                                                                                  |
| pysftp                            | V 0.2.9       | This is old but stable code.                                                                                  |

FILES IN THIS REPOSITORY
===================================================================================
| File Name                         | Description                                                                                                                   |
| ssh_copy_files.py                 | The described utility within this repository                                                                                  |
| README.md                         | This README.md file

INSTRUCTIONS
===================================================================================
SSH Copy Utility That Demonstrates a Real World Use Case of python's pysftp library
===================================================================================
This utility's purpose is to copy files from a source Linux VM to a remote Linux
VM using the python pysftp library. It copies all of the files from a source
directory to a target directory on the remote host. This tool by design will not
recursively copy files. This tool sets the file access mode of remote files to
660. It can with the correct option remove files on the remote host that are not
present on the source host or remove the source file after copying, but not both.
We note that even today many sysadmin and DBA admin types still rely on rsync or
secure NFS. We do not care for either approach because: 1) rsync is not secure;
2) NFS is not secure unless setup to use encryption, and; 3) encrypted NFS is
difficult to setup and maintain.

VERSION AND DATE OF LATEST UPDATE
===================================================================================
VERSION 1.1 - 25-August-2023

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
for this file. Make sure when testing that your set timeout in
/etc/sshd/sshd_config is appropriately defined. This utility should run fine
when called from cron.

REQUIREMENTS 
===================================================================================
The following requirements are based on when these examples were created as of
26-June-2023 and subsequently modified on 25-August-2023. Technology changes fast,
so be certain to consider testing at more current versions.

| Package                           |  Version      |  Source                                                                                                       |
|-----------------------------------|---------------|---------------------------------------------------------------------------------------------------------------|
| A Fedora or ubuntu kernel         | V7, V8, or V9 | We have tested on RHEL 7.9 and 8.x. We have tested on OLE 7.9, 8.x, and 9.0. We have tested on WSL's ubuntu.  |
| Python                            | 3.6x or 3.8x  | We strongly recommend 3.8x or later since 3.6x is deprecated.                                                 |
| PIP                               | Version 3     | Sets with your Linux distro.                                                                                  |
| pysftp                            | V 0.2.9       | This is old but stable code.                                                                                  |

FILES IN THIS REPOSITORY
===================================================================================
| File Name                         | Description                                                                                                                   |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| ssh_copy_files.py                 | The described utility within this repository                                                                                  |
| README.md                         | This README.md file

INSTRUCTIONS
===================================================================================
1. Make sure your system is up-to-date with all appropriate OS patches.
2. Setup an SSH key without a passphrase. You can use a passphrase with the library. Note you would have to modify the code to do that.
3. Make sure the public key has been copied to the remote host.
4. Make sure the remote host's SSH timeout values are appropriately set. This utility was build to be a replacement to rsync and can be used to copy big files.
   Big files take time to copy. Adjust accordingly.
5. We recommend you not save the public key on the same host that holds the private key. Storing the public key on the target and in a cloud key vault
   reduces the attack vector.
6. Follow the instructions in the utility. Running the utility without any arguments will return these instructions.
7. Be certain to send both stdout and stderr to a log file when calling this utilty with cron.

REFERENCES
===================================================================================
https://pypi.org/project/pysftp/
https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html#pysftp-connection-walktree
http://alvincjin.blogspot.com/2014/09/recursively-fetch-file-paths-from-ftp.html

Acknowledgements
===================================================================================
We wish to acknowledge the work of Alvin's Big Data Notebook, otherwise known as
Changjiu Jin. We don't see a profile for Changejiu on linkedIN anymore. But we do
appreciate his work that enabled us to solve some problems.

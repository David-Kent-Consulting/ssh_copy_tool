SSH Copy Utility That Demonstrates a Real World Use Case of python pysftp library
=================================================================================
This utility's purpose is to copy files from a source Linux VM to a remote Linux
VM using the python pysftp library. It copies all of the files from a source
directory to a target directory on the remote host. This tool by design will not
recursively copy files. This tool sets the file access mode of remote files to
660. It can with the correct option remove files on the remote hosts that are not
present on the source host. We note that even today many sysadmin and DBA admin
types still rely on rsync or secure NFS. We do not care for either approach
because: 1) rsync is not secure; 2) NFS is not secure unless setup to use
encryption, and; 3) encrypted NFS is difficult to setup and maintain.

LICENSE REQUIREMENTS
=================================================================================
This code is public domain and is considered open source. The code is provided
for the purpose of demonstrating a practical use of the pysftp tool. The code is
provided without guarantee. You may use this code in part or in whole as you see
fit. You may modify the code. You agree that use of this code is solely at your
own risk.


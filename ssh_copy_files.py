#!/bin/python3


#  replace above with /bin/python3 in final testing

'''

File name:      ssh_copy_tool.py

Version:        1.0

Purpose:        This utility's purpose is to copy files from a source Linux
                VM to a remote Linux VM using the python pysftp library. It
                copies all of the files from a source directory to a target
                directory on the remote host. This tool by design will not
                recursively copy files in subdirectories. This tool sets the
                file access mode of remote files to 660. It can with the
                correct option remove files on the remote host that are not
                present on the source host. We note that even today many
                sysadmin and the source host. We note that even today many
                sysadmin and DBA admin types still rely on rsync or secure
                NFS. We do not like either approach because:
                    1) rsync is not secure;
                    2) NFS is not secure unless setup to use encryption, and;
                    3) encrypted NFS is difficult to setup and maintain.

Requirements:   Please see the README.md file for requirements, caveats, and
                use cases within the GIT repository
                https://github.com/David-Kent-Consulting/ssh_copy_tool

Author:         Hank L Wojteczko
                Practice Manager
                Kent Cloud Solutions, Inc
                hankwojteczko@davidkentconsulting.com

Created On:     22-June-2023

Last Modified:  n/a

License:        This code is public domain and is considered open source.
                The code is provided for the purpose of demonstrating
                a practical use of the pysftp tool. The code is provided without
                guarantee. You may use this code in part or in whole as you see
                fit. You may modify the code.

                You agree that use of this code is solely at your own risk.


Acknowledgements:
                We wish to acknowledge the work of Alvin's Big Data Notebook,
                otherwise known as Changjiu Jin. We don't see a profile for
                Changejiu on linkedIN anymore. But we do appreciate his work
                that enabled us to solve some problems.


Variables:
                Input Variables
                ===============

                var name            position    purpose
                ============================================================================
                pkey_file           1           The private SSH key used to connect to the
                                                target host.

                source_dir          2           The source directory from which to copy file
                                                from.

                host                3           The remote host to copy files to.

                user                4           User on the remote host.

                remote_dir          5           The target directory to where the files will
                                                be copied.

                overwrite_target    variable    Over-write the remote files if already
                                                present.

                delete_obsolete     variable    Remove files on the remote system that are
                                                not present on the source host within the
                                                source directory.
                                                
                delete_input        variable    Deletes all input source files in the directory
                                                after the copy operation completes. This option
                                                may not be used in conjunction with the option
                                                delete_obsolete

                Global Variables of concern
                ===========================

                var name            purpose
                ============================================================================             
                sftp                    method created from pysftp.Connection
                source_files            A list of the source files per os.walk()
                wtcb                    Callback method create from pysftp.WTCallbacks for use
                                        by sftp.walktree.

                Functions
                =========
                function name       purpose
                ============================================================================   
                copy_files              Copies the source files to the remote host to the
                                        specified remote directory. Tests to see if 
                                        overwrite_target is True, if so, over-writes target
                                        files with source files, otherwise skips target file
                                        if already present on remote system.
                
                delete_obsolete_files   Deletes files on remote system in remote directory
                                        if not found in the source system within the
                                        source directory.

                

Order of logic
1. set the options vars for subsequent logic
2. test local file data
3. Open a connection to the remote host and test for the remote target directory
4. Change to source_dir and build a list of files to copy to the remote directory
5. Re-open an SSH session and copy the files to the remote host
6. If delete_obsolete, delete files on remote system in remote directory that
   are not present on the local system
7. If delete_input, delete the input files from the source system
                
'''

def copy_files(my_source_files,
               my_remote_dir):


    # build a list of files on the remote host using a callback method.
    # Call to walktree() is poorly documented with many errors in
    # many blogs. Use exactly as shown and your headaches will melt
    # away.
    print("\nBuilding a list of files on the remote host......\n")
    wtcb = pysftp.WTCallbacks()
    with pysftp.Connection(
        host=host,
        private_key=pkey_file,
        username=user
    ) as sftp:
        sftp.walktree(my_remote_dir,
                  fcallback=wtcb.file_cb,
                  dcallback=wtcb.dir_cb,
                  ucallback=wtcb.unk_cb)
        #sftp.close() done below in finally: block
    try:
        remote_files = []
        for f in wtcb.flist:
            remote_files.append(f)

        # copy the files to the remote host and set the target files to access mode 640        
        # This logic over-writes all remote files on the remote host within the
        # remote directory.
        failed_files = []
        if overwrite_target:
            for s in my_source_files:
                if exists(source_dir + "/" + s):
                    print("Copying " + s + " to remote host " + host)
                    with pysftp.Connection(
                        host=host,
                        private_key=pkey_file,
                        username=user
                    ) as sftp:
                        try:
                            sftp.put(s, remote_dir + "/" + s, preserve_mtime=True)
                            sftp.chmod(remote_dir + "/" + s, 640)

                            print("Copy of file " + s + " to remote host " + host + " completed to " + remote_dir + "/" + s)
                        except Exception as err:
                            # this will log the full error message and traceback
                            print("ERROR: copy of file " + s + " to remote host " + host + " failed to " + remote_dir + "/" + s, err)
                            failed_files.append(s) 
                            continue
                        finally:
                            sftp.close()
        
        # This is how the utility is normally used.        
        else:    
            for s in my_source_files:
                if exists(source_dir + "/" + s):    
                    if (remote_dir + "/" + s) not in remote_files:
                        print("Copying " + s + " to remote host " + host)
                        with pysftp.Connection(
                            host=host,
                            private_key=pkey_file,
                            username=user
                        ) as sftp:
                            try:
                                sftp.put(s, remote_dir + "/" + s, preserve_mtime=True)
                                sftp.chmod(remote_dir + "/" + s, 640)

                                print("Copy of file " + s + " to remote host " + host + " completed to " + remote_dir + "/" + s)
                            except Exception as err:
                                # this will log the full error message and traceback
                                print("ERROR: copy of file " + s + " to remote host " + host + " failed to " + remote_dir + "/" + s, err) 
                                failed_files.append(s) 
                                continue
                            finally:
                                sftp.close()
                        #end with 
                    #end if remote file not found
                else:
                    print("Error copying " + source_dir + "/" + s + " the copy failed, and now the source file no longer exists.")

                #end if exists source file
            #end for loop over source dir
        #end else, not ovewriting

        iLoopLimit = 0
        iNumFailures = len(failed_files)
        for s in failed_files:
            iLoopLimit += 1
            print("Number of failed files was: " + iNumFailures + " and Loop Limit is: " + iLoopLimit + "...")
            if exists(source_dir + "/" + s):
                print("Copying " + s + " to remote host " + host)
                with pysftp.Connection(
                    host=host,
                    private_key=pkey_file,
                    username=user
                ) as sftp:
                    try:
                        sftp.put(s, remote_dir + "/" + s, preserve_mtime=True)
                        sftp.chmod(remote_dir + "/" + s, 640)

                        print("Copy of file " + s + " to remote host " + host + " completed to " + remote_dir + "/" + s)
                    except Exception as err:
                        # this will log the full error message and traceback
                        print("ERROR: copy of file " + s + " to remote host " + host + " failed to " + remote_dir + "/" + s, err)
                        failed_files.append(s) 
                        continue
                    finally:
                        sftp.close()
            else:
                print("Error copying " + source_dir + "/" + s + " the copy failed, and now the source file no longer exists.")
            #if we had failed files from above, make sure we loop over them twice
            if ((iNumFailures > 0) & ((iLoopLimit > iNumFailures) & (iLoopLimit % iNumFailures == 0))):
                print("Number of failed files was: " + iNumFailures + " and Loop Limit is: " + iLoopLimit + ", breaking the loop.")
                break
        #end for failed
    
    except Exception as err1:
        print("ERROR: issue in building remote file list: ", err1)
    finally:
        sftp.close()
# end function copy_files()


def delete_obsolete_files(my_remote_dir):
    
# build a list of files on the remote host using a callback
    print("\nPreparing to remove obsolete files from the remote host......\n")
    wtcb = pysftp.WTCallbacks()
    with pysftp.Connection(
        host=host,
        private_key=pkey_file,
        username=user
    ) as sftp:
        
        sftp.walktree(my_remote_dir,
                  fcallback=wtcb.file_cb,
                  dcallback=wtcb.dir_cb,
                  ucallback=wtcb.unk_cb)
        sftp.close()
    
    remote_files = []
    for f in wtcb.flist:
        remote_files.append(f)


    with pysftp.Connection(
        host=host,
        private_key=pkey_file,
        username=user
    ) as sftp:
        
        # We tried many approaches to this problem. Testing for the presence of the file
        # requires the least amount of code and is simplistic logic. Note how we strip
        # away the path from each full file path name and then simply test for the presence
        # of a file on the local system. We simply delete the file from the remote
        # system if it is not found.
        count = len(remote_dir) +1
        for r in remote_files:
            if not exists(r[count:]):
                sftp.remove(r)
                print("Removed file " + r + " which is no longer present in the local host directory " + source_dir)

    sftp.close()
            
# end function delete_obsolete_files()

def delete_source_files(my_source_files):
    for s in my_source_files:
        if exists(source_dir + "/" + s):
            print("Deleting file " + s + " from source directory")
            os.unlink(s)
            
# end function delete_source_files()

######################################
# Main program body
######################################

import os, pysftp, sys
from os.path import exists

print("ssh_copy_files.py version 1.1")

if len(sys.argv) < 6 or len(sys.argv) > 8:
    print(
        "\n\nssh_copy_tool.py : Usage\n\n" +
        "ssh_copy_tool.py [ssh_key] [source_dir] [remote host] [remote user]\n" +
        "\t[remote directory] options\n\n" +
        "Use Case Example 1: Copies all files in the specified source directory\n" +
        "to the remote host within the specified remote directory\n\n" +
        "ssh_copy_tool.py $HOME/.ssh/id_rsa /data 10.1.0.4 remote_user\n" +
        "\t/home/remote_user/data\n\n" +
        "Options for use with this utility include:\n" +
        "\t--overwrite-target\tOver-write any target files already present in the remote system's directory\n" +
        "\t--delete-obsolete\tRemove files on the remote system that are not present on the local system\n" +
        "\t--delete-input\t\tRemoves all source input files after they have been copied to the target system.\n" +
        "\t\t\t\t--delete-inpute may not be used with --delete-obsolete\n"
    )
    raise RuntimeWarning("\n\nINVALID USAGE\n")

pkey_file           = sys.argv[1]
source_dir          = sys.argv[2]
host                = sys.argv[3]
user                = sys.argv[4]
remote_dir          = sys.argv[5]

# 1. set the options vars for subsequent logic
overwrite_target    = False
delete_obsolete     = False
delete_input        = False
if "--overwrite-target" in sys.argv or "--OVERWRITE-TARGET" in sys.argv:
    overwrite_target = True
if "--delete-obsolete" in sys.argv or "--DELETE-OBSOLETE" in sys.argv:
    delete_obsolete  = True
if "--delete-input" in sys.argv or "--DELETE-INPUT" in sys.argv:
    delete_input = True

if delete_input and delete_obsolete:
    raise RuntimeWarning("\n\nWARNING! --delete-input may not be used with --delete-obsolete\n")

# 2. test local file data
if not exists(pkey_file):
    raise RuntimeWarning("\nSSH private key " + pkey_file + " not found\n\n")
elif not exists(source_dir):
    raise RuntimeWarning("\nSource directory " + source_dir + " not found\n\n")

# 3. Open a connection to the remote host and test for the remote target directory
with pysftp.Connection(host=host,
                       private_key=pkey_file,
                       username=user) as sftp:
    
    output = sftp.listdir(remote_dir)

    # Our practice is to always close the SFTP connection at the end of a code block.
    # There are opposed views on this approach. We believe this approach poses the
    # least security risk. We repeat the practice throughout this utility.
    sftp.close()

# 4. Change to source_dir and build a list of files to copy to the remote directory
#    and stay in that directory untiol the utility exits.
os.chdir(source_dir)
source_files = []
this_dir = os.getcwd()
# r = root, d = direcories, f = files
for r, d, f in os.walk(this_dir):
    for file in f:
        source_files.append(file)


# 5. Re-open an SSH session and copy the files to the remote host
copy_files(source_files,
           remote_dir)

# 6. If delete_obsolete, delete files on remote system in remote directory that
#    are not present on the local system


if delete_obsolete:
    
    delete_obsolete_files(remote_dir)
    
# 7. If delete_input, delete the input files from the source system
if delete_input:
    delete_source_files(source_files)

print("\n\nssh_copy_files.py exiting normally.\n")

'''
References:
https://pypi.org/project/pysftp/
https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html#pysftp-connection-walktree
http://alvincjin.blogspot.com/2014/09/recursively-fetch-file-paths-from-ftp.html
'''
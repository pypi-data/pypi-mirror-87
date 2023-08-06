RESIF DATA TRANSFER
==

A helper script to send data to RESIF datacentre and get  transaction status back.

## REQUIREMENTS

### SYSTEM REQUIREMENTS


 - This program is validated for:
      - Python 3.6
      - Redhat Enteprise Linux 6.x and above, 32 or 64 bits
      - Debian Linux, Lenny and above, 32 or 64 bits
  however, this should work under any modern Unix/Linux system

- You also need a working 'rsync' command (version 3.0.6 and above). Check your
rsync command by entering :

  ```
   $ rsync --version
  ```
   >IMPORTANT NOTE : as of April 2016, we are considering an update of the minimal rsync    version requirement. Meanwhile, it is recommended that in case of unpredictible transfer timeouts, the most recent version of rsync be installed.

- A working GNU 'du' command. Most often, du is provided with GNU coreutils,  version 8.4 or above is advised. Check your du command by entering:
  ```
  $ du --version
  ```
- You need a working Python interpreter on your system (version 3
 and above), with its full standard library. Check your python interpreter by entering:
  ```
   $ /usr/bin/env python --version
  ```
- It is highly advised that your system time be synchronized (eg. using NTP)


### NETWORK REQUIREMENTS


- You need a working rsync connection to resif rsync server. You may
check your IP connectivity is working using 'nc', eg:
  ```
  $ nc -z rsync.resif.fr 873
  ```
  should return :
  ```
   Connection to rsync.resif.fr 873 port [tcp/rsync] succeeded!
  ```
  If you don't have nc, you may use telnet, eg:
  ```
  $ telnet rsync.resif.fr 873
  ```
  should return:
   ```
    Trying xxx.xxx.xx.xx ...
    Connected to rsync.resif.fr.
    Escape character is '^]'.
    @RSYNCD: xx.yy
  ```
   If your IP connection to the remote rsync server does not work :

   - First, check with RESIF datacenter operator the remote server
is up and running

  - Then, check with your IT team that you are allowed to reach
port tcp/873 on rsync.resif.fr


### AUTHENTICATION REQUIREMENTS


Before you begin transferring some data, RESIF datacenter operator must provide you with :

- Your node name
- Your node password (must be kept secret)

For each  data type you will transfer, you must tell RESIF datacenter  operator :
- The address (FQDN) of the machine you will be performing the transfer from.
- DNS aliases are known to cause problem while doing IP filtering. Take
care to provide the real name of your machine, not an aliased name.

There can be only one transferring machine per data type. You may use
a single machine for all data types.


## INSTALLATION

Resif Data Transfer  published on [PyPI](https://test.pypi.org/project/ResifDataTransfer/) and can be installed from there:
```
 pip install ResifDataTransfer
 ```

Then, you should be able to execute :
```
$ ResifDataTransfer -h
```


## CONFIGURATION


  By default, configuration file will be searched in install directory, eg:

/usr/lib/python3.6/site-packages/resif_data_transfer/ResifDataTransfer.conf

You may want to use an alternate configuration path (see -c option).

A template configuration is provided in ResifDataTransfer.conf.dist,
copy this file to create your own configuration file :
```
$ cd resif-data-transfer/
$ cp ResifDataTransfer.conf.dist ResifDataTransfer.conf
```
Edit according to your requirements.

For security reasons, configuration file must only be readable by file owner
and group. On Unix/Linux system, you may set configuration file permissions as:
```
$ chmod 600 ResifDataTransfer.conf
```
or
```
$ chmod o-rwx ResifDataTransfer.conf
```

## UPGRADES
todo
For safety, backup your current installation directory.

Download the new tarball and move it to your current installation
directory. E.g, if your installation is in /home/sysop/resif-data-transfer,
move the tarball to /home/sysop. Then, extract :

$ tar xvf resif-data-transfer.tar.gz

This will replace your previous installation. Your configuration and log
files will not be replaced.


## AFTER UPGRADING
to do
Run a test transfer (using -t) to check your configuration file.
Run a logbook dump (using -l) to check your logbook.



## BACKUPS

You should backup the following files:

  - Configuration file
  - General log file
  - Logbook file

You may want to rotate the general log file using a system tool
such as 'logrotate'. You should never edit/alter loogbook contents by hand.

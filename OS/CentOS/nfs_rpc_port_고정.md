# [CentOS] nfs rpc port 고정

원문 : https://www.systutorials.com/39625/fixing-ports-used-by-nfs-server/

The ports used by NFS server can be dynamically assigned by rpbind to any higher number. We need to fix the ports used by NFS server to configure firewall or port forwarding mechanism. The ports used by NFS server and how to fix these ports will be introduced in this post.

There are seven ports need to be taken care of for NFS server.

1. rpcbind‘s listening port

rpcbind listens on TCP and UDP port 111. It is the default port number and it doesn’t require special configuration.

2. nfsd‘s listening port

nfsd listens on TCP and UDP port 2049. It is also the default port number and it doesn’t require special configuration.

3. Fix ports for RQUOTAD_PORT, MOUNTD_PORT, LOCKD_TCPPORT, LOCKD_UDPPORT and STATD_PORT

These five ports should be configured to be fixed to avoid rpcbind assign random port for it.

Uncomment or add these lines to /etc/sysconfig/nfs:

```
RQUOTAD_PORT=875
LOCKD_TCPPORT=32803
LOCKD_UDPPORT=32769
MOUNTD_PORT=892
STATD_PORT=662
```
After restarting nfs and rpcbind, only these seven ports are needed for setting up NFS server.

The ports used by NFS RPC-based service can be listed by:
```
$ rpcinfo -p
```
This is a sample output of this command:
```
    program vers proto   port
    100000    2   tcp    111  portmapper
    100000    2   udp    111  portmapper
    100024    1   udp    662  status
    100024    1   tcp    662  status
    100011    1   udp    875  rquotad
    100011    2   udp    875  rquotad
    100011    1   tcp    875  rquotad
    100011    2   tcp    875  rquotad
    100003    2   udp   2049  nfs
    100003    3   udp   2049  nfs
    100003    4   udp   2049  nfs
    100021    1   udp  32769  nlockmgr
    100021    3   udp  32769  nlockmgr
    100021    4   udp  32769  nlockmgr
    100021    1   tcp  32803  nlockmgr
    100021    3   tcp  32803  nlockmgr
    100021    4   tcp  32803  nlockmgr
    100003    2   tcp   2049  nfs
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100005    1   udp    892  mountd
    100005    1   tcp    892  mountd
    100005    2   udp    892  mountd
    100005    2   tcp    892  mountd
    100005    3   udp    892  mountd
    100005    3   tcp    892  mountd
```
We can configure the firewall to only allow connections to these ports to enhance security. Please note that NFS is not secure enough and it need other mechanisms if you want to set up a SECURE NFS server.

Sample configuration files

Here is my configuration files for NFS:

/etc/sysconfig/nfs :
```
    # Define which protocol versions mountd
    # will advertise. The values are "no" or "yes"
    # with yes being the default
    #MOUNTD_NFS_V1="no"
    MOUNTD_NFS_V2="no"
    MOUNTD_NFS_V3="no"
    #
    #
    # Path to remote quota server. See rquotad(8)
    #RQUOTAD="/usr/sbin/rpc.rquotad"
    #RQUOTAD=no
    # Port rquotad should listen on.
    RQUOTAD_PORT=875
    # Optinal options passed to rquotad
    #RPCRQUOTADOPTS=""
    #
    # Optional arguments passed to in-kernel lockd
    #LOCKDARG=
    # TCP port rpc.lockd should listen on.
    LOCKD_TCPPORT=32803
    # UDP port rpc.lockd should listen on.
    LOCKD_UDPPORT=32769
    #
    #
    # Optional arguments passed to rpc.nfsd. See rpc.nfsd(8)
    # Turn off v2 and v3 protocol support
    #RPCNFSDARGS="-N 2 -N 3"
    # Turn off v4 protocol support
    #supportRPCNFSDARGS="-N 4"
    # Number of nfs server processes to be started.
    # The default is 8.
    #RPCNFSDCOUNT=8
    # Stop the nfsd module from being pre-loaded
    #NFSD_MODULE="noload"
    #
    #
    # Optional arguments passed to rpc.mountd. See rpc.mountd(8)
    #RPCMOUNTDOPTS=""
    # Port rpc.mountd should listen on.
    MOUNTD_PORT=892
    #
    #
    # Optional arguments passed to rpc.statd. See rpc.statd(8)
    #STATDARG=""
    # Port rpc.statd should listen on.
    STATD_PORT=662
    # Outgoing port statd should used. The default is port
    # is random
    #STATD_OUTGOING_PORT=2020
    # Specify callout program
    #STATD_HA_CALLOUT="/usr/local/bin/foo"
    #
    #
    # Optional arguments passed to rpc.idmapd. See rpc.idmapd(8)
    #RPCIDMAPDARGS=""
    #
    # Set to turn on Secure NFS mounts.
    #SECURE_NFS="yes"
    # Optional arguments passed to rpc.gssd. See rpc.gssd(8)
    #RPCGSSDARGS="-vvv"
    # Optional arguments passed to rpc.svcgssd. See rpc.svcgssd(8)
    #RPCSVCGSSDARGS="-vvv"
    # Don't load security modules in to the kernel
    #SECURE_NFS_MODS="noload"
    #
    # Don't load sunrpc module.
    #RPCMTAB="noload"
    #
```

/etc/exports :
```
    /lhome 10.0.0.1/24(rw)
    /lhome 10.0.1.1/24(rw)
    /lhome 143.89.135.171(rw)
```


Thx Kyg
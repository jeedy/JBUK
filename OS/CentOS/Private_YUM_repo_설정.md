# [CentOS] Private YUM repo 설정

외부와 네트워크 통신이 되지 않을 때, 사설 YUM repository 서버를 구축할 수 있다.

1. YUM repository를 ftp 서버로 구축(server)
1. YUM repository에 접속할 네트워크 설정(client)

/etc/yum.repos.d 디렉토리 이동 rhel5.repo 생성 (CentOS 5 기준)(client)
```bash
[root@rnd02 yum.repos.d]# pwd
/etc/yum.repos.d

[root@rnd02 yum.repos.d]# vim rhel5.repo
.
.
[Server]
baseurl=ftp://192.168.200.40/pub/rhel5/Server
enabled=1
gpgcheck=0

[root@rnd02 yum.repos.d]# yum -y update
Loaded plugins: rhnplugin, security
Repository 'Server' is missing name in configuration, using id
This system is not registered with RHN.
RHN support will be disabled.
Server                                                              | 1.3 kB     00:00
Server/primary                                                      | 905 kB     00:00
Server                                                                           3229/3229
Skipping security plugin, no data
Setting up Update Process
No Packages marked for Update

[root@rnd02 yum.repos.d]#

```
rhel5.repo 설정 파일 내 [Server] > Baseurl에는 OS의 내용이 들어가있는 주소와 디렉토리 경로를 명시해줘야 한다.



Thx Kyg
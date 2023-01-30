# 오라클 라이브러리 설치 및 oracle instant-client 설치방법

참고:
- https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-zip-files


```sh
(base) root@dd97dd996f3e:/opt/oracle# wget https://download.oracle.com/otn_software/linux/instantclient/216000/instantclient-basic-linux.x64-21.6.0.0.0dbru.zip
--2022-05-23 07:27:45--  https://download.oracle.com/otn_software/linux/instantclient/216000/instantclient-basic-linux.x64-21.6.0.0.0dbru.zip
Resolving download.oracle.com (download.oracle.com)... 23.45.52.112
Connecting to download.oracle.com (download.oracle.com)|23.45.52.112|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 78665919 (75M) [application/zip]
Saving to: ‘instantclient-basic-linux.x64-21.6.0.0.0dbru.zip’

(base) root@dd97dd996f3e:/opt/oracle# unzip instantclient-basic-linux.x64-21.6.0.0.0dbru.zip
(base) root@dd97dd996f3e:/opt/oracle# cd instantclient_19_15

(base) root@dd97dd996f3e:/opt/oracle/instantclient_19_15# sudo apt-get install libaio1
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  libaio1
0 upgraded, 1 newly installed, 0 to remove and 40 not upgraded.
Need to get 7,184 B of archives.
After this operation, 35.8 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu focal/main amd64 libaio1 amd64 0.3.112-5 [7,184 B]
Fetched 7,184 B in 1s (9,733 B/s)
debconf: delaying package configuration, since apt-utils is not installed
Selecting previously unselected package libaio1:amd64.
(Reading database ... 69938 files and directories currently installed.)
Preparing to unpack .../libaio1_0.3.112-5_amd64.deb ...
Unpacking libaio1:amd64 (0.3.112-5) ...
Setting up libaio1:amd64 (0.3.112-5) ...
Processing triggers for libc-bin (2.31-0ubuntu9.2) ...
(base) root@dd97dd996f3e:/opt/oracle/instantclient_19_15# sudo sh -c "echo /opt/oracle/instantclient_19_15 > /etc/ld.so.conf.d/oracle-instantclient.conf"
(base) root@dd97dd996f3e:/opt/oracle/instantclient_19_15# sudo ldconfig
(base) root@dd97dd996f3e:/opt/oracle/instantclient_19_15# export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_15:$LD_LIBRARY_PATH
(base) root@dd97dd996f3e:/opt/oracle/instantclient_19_15#
```


```python
!pip install cx_oracle

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir='/opt/oracle/instantclient_19_15')

dsn = cx_Oracle.makedsn("localhost", 1521, service_name = "dev") # 오라클 주소
connection = cx_Oracle.connect(user="kimjy", password="12345", dsn=dsn, encoding="UTF-8") # 오라클 접속

cur = connection.cursor() # 실행 결과 데이터를 담을 메모리 객체
sql='''
select * from employee
'''

for row in cur.execute(sql):
    print(row)

connection.close()
```
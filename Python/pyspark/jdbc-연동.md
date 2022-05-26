# pyspark(spark) 오라클 라이브러리 연동

## Spark에서 사용중인 java lib 폴더에 jdbc 라이브러리 복사


### 1. Mysql jdbc
```sh
$ wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-java-8.0.15.zip
$ unzip mysql-connector-java-8.0.15.zip
$ cd mysql-connector-java-8.0.15

$ cp ./mysql-connector-java-8.0.15.jar /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext

# 확인
$ cd /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext
...
-rw-r--r-- 1 root root 2134905 May 25 07:01 mysql-connector-java-8.0.15.jar
...

```

### 2. oracle jdbc
```sh
$ wget wget https://download.oracle.com/otn_software/linux/instantclient/1915000/instantclient-basic-linux.x64-19.15.0.0.0dbru.zip
$ unzip instantclient-basic-linux.x64-19.15.0.0.0dbru.zip
$ cd instantclient-basic-linux.x64-19.15.0.0.0dbru

$ cp ./ojdbc8.jar /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext

# 확인
$ cd /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext
...
-rw-r--r-- 1 root root 4465257 May 23 09:06 ojdbc8.jar
...

```

# Tomcat shell script to start and shutdown

## 디렉토리 구조

```bash
# 자바 설치위치
/sdb1/java

# 톰켓 설치위치
/sdb1/tomcat

# 어플리케이션 설치 위치
/sdb1/servers/tomcat-application
/sdb1/servers/tomcat-application/conf
/sdb1/servers/tomcat-application/env.sh
/sdb1/servers/tomcat-application/logs
/sdb1/servers/tomcat-application/start.sh
/sdb1/servers/tomcat-application/stop.sh
/sdb1/servers/tomcat-application/temp
/sdb1/servers/tomcat-application/webapps
/sdb1/servers/tomcat-application/work
```


## conf/env.sh

```bash
IPADDR=`ifconfig eth1 | awk '/inet.*Bcast/ {print $2}'| cut -f 2 -d':'`
DEFAULT_PORT=8000

PORT_OFFSET=0

let HTTP_PORT=$DEFAULT_PORT+80+$PORT_OFFSET
let HTTPS_PORT=$DEFAULT_PORT+443+$PORT_OFFSET
let AJP_PORT=$DEFAULT_PORT+9+$PORT_OFFSET
let SHUTDOWN_PORT=$DEFAULT_PORT+5+$PORT_OFFSET

let JMXREMOTE_PORT=$DEFAULT_PORT+10001+$PORT_OFFSET
let RMI_REGISTRY_PORT=$DEFAULT_PORT+10002+$PORT_OFFSET
let RMI_SERVER_PORT=$DEFAULT_PORT+10003+$PORT_OFFSET

export USER="jboss"
export ServerName="batch1"
export JAVA_HOME=/sdb1/java
export CATALINA_HOME=/sdb1/tomcat
export CATALINA_BASE=/sdb1/servers/$ServerName
export CATALINA_OPTS="-Denv.servername=$ServerName"
export JMX_OPTS="-Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.port=$JMXREMOTE_PORT -Dcom.sun.management.jmxremote.authenticate=false -Djava.rmi.server.hostname=$IPADDR -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.local.only=false"
export CATALINA_OPTS="$CATALINA_OPTS $JMX_OPTS"

export JAVA_OPTS="-server -DjvmRoute=$ServerName -Djava.awt.headless=true -server -Xms1024m -Xmx1024m -XX:NewSize=512m -XX:MaxNewSize=512m -Dfile.encoding=UTF-8"
export JAVA_OPTS="$JAVA_OPTS -XX:+DisableExplicitGC -XX:+UseParallelGC -Xloggc:$CATALINA_BASE/logs/gc.log -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=$CATALINA_BASE/logs"
#export JAVA_OPTS="$JAVA_OPTS -Djava.security.egd=file:/dev/./urandom"

export JAVA_OPTS="$JAVA_OPTS -Dtomcat.port.shutdown=$SHUTDOWN_PORT"
export JAVA_OPTS="$JAVA_OPTS -Dtomcat.port.http=$HTTP_PORT"
export JAVA_OPTS="$JAVA_OPTS -Dtomcat.port.https=$HTTPS_PORT"
export JAVA_OPTS="$JAVA_OPTS -Dtomcat.port.ajp=$AJP_PORT"

export JAVA_OPTS="$JAVA_OPTS -Drmi.registry.port=$RMI_REGISTRY_PORT"
export JAVA_OPTS="$JAVA_OPTS -Drmi.server.port=$RMI_SERVER_PORT"


############################### tomcat 8.0 removed option #################################
#### -XX:PermSize=256m -XX:MaxPermSize=256m ignoring option support was removed in 8.0 ####
###########################################################################################

```


## start.sh

```bash
#!/bin/sh
source ./env.sh

PID=`ps -ef | grep java | grep "=$ServerName " | awk '{print $2}'`

if [ e$PID != "e" ]
then
    echo PID : $PID
    echo "[$ServerName] Tomcat Server is already RUNNING..."
    exit;
fi

UNAME=`id -u -n`
if [ e$UNAME != "e$USER" ]
then
    echo "Use $USER account to start [$ServerName] Tomcat Server..."
    exit;
fi

cd $CATALINA_HOME/bin
./startup.sh

```


## shutdown.sh

```bash
#!/bin/sh
source ./env.sh

$CATALINA_HOME/bin/shutdown.sh
```
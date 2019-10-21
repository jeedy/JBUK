# JBoss 쓰레드풀 설정 방법
tags: 
Thread pool, maxThreads, jboss, connection pool, 

## 참고 자료
- https://waspro.tistory.com/355

## Thread pool 방식
1. unbounded-queue-thread-pool
2. bounded-queue-thread-pool
3. blocking-bounded-queue-thread-pool
4. queueless-thread-pool
5. blocking-queueless-thread-pool
6. scheduled-thread-pool


### 1) unbounded-queue-thread-pool
모든 요청에 대해 처리하고, 만약 max thread count를 초과할 경우 unbounded FIFO queue에서 대기하도록 하는 방식입니다. 

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <unbounded-queue-thread-pool name="ThreadPool">  
        <max-threads count="10" />  
        <keepalive-time time="30" unit="seconds"/>  
    </unbounded-queue-thread-pool>  
 </subsystem>
```

처리를 보장한다는 점에서 장점이 될 수 있으나 요청이 메모리에 계속 쌓이기때문에 OOME가 발생할 수 있습니다. 

### 2) bounded-queue-thread-pool 
초과되는 요청에 대해서 처리가 가능해질 때까지 요청을 reject(또는 discard)하는 모델입니다.

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <bounded-queue-thread-pool name="ThreadPool" blocking="true">  
        <queue-length count="500"/>  
        <core-threads count="5"/>  
        <max-threads count="10"/>  
        <keepalive-time time="30" unit="seconds"/>  
    </bounded-queue-thread-pool>  
</subsystem>
```

`max-threads` 의 값을 500으로 했을 시 `core-threads`는 500 보다 작거나 같아야 합니다. 
`core-threads` 를 지정하지 않는다면 내부적으로 `max-threads`와 같은 500으로 지정됩니다. 
다만 core-threads 기본적으로 요청 처리 실행을 준비하고 있는 준비된 스레드입니다. 
queue-length 는 부하가 일시적으로 높아졌을 경우 버퍼링 기능을 하는 것으로써 적정한 수치는 비즈니스 요건과 
애플리케이션 및 환경마다 다를 수 있으므로 비즈니스 시나리오에 기반한 성능 테스트 후 성능이 가능 높게 나오는 
수치로 결정하셔야 합니다.

core-threads 는 스레드 풀에서 실행을 준비하고 있는 기본 스레드 개수를 입니다. core-threads 값을 지정하지 않으면 
max-threads(maximum thread pool size)의 값과 동일하게 지정됩니다. 
core-threads 수치가 너무 크면 사용되지 않는 스레드가 발생하여 리소스 낭비가 발생하게 됩니다. 
수치가 너무 낮으면 thread 동시 실행성이 줄어들게 됩니다.

queue-length 는 실행가능한 스레드가 주어질 때까지 요청들이 대기하는 큐의 사이즈입니다. 
사이즈가 클수록 더 많은 메모리가 사용되고 큐가 채워지지 않는 만큼 리소스 낭비가 됩니다. 

### 3) blocking-bounded-queue-thread-pool 
구조적으로 초과되는 요청에 대해서 처리가 가능해질 때까지 block 시키는 모델입니다. 
초과되는 요청을 버리(discard)거나 reject하지 않는 모델입니다.

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <blocking-bounded-queue-thread-pool name="MyScheduler">  
        <max-threads count="1" />  
    </blocking-bounded-queue-thread-pool>  
</subsystem>
```

### 4) queueless-thread-pool
독립적인 thread들이 수행될때 사용하는 단순한 thread pool입니다. 또한 long-running task에 적합한 방식입니다. 
대기할 수 있는 thread의 queue가 존재하지않으며, max-thread를 초과할경우 reject하게 됩니다.

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <queueless-thread-pool name="MyExecutor">  
        <max-threads count="200" />  
    </queueless-thread-pool>   
</subsystem>
```

### 5) blocking-queueless-thread-pool
대기할수 있는 thread 의 queue가 존재하지않으며, 만약 max thread count를 초과할경우 block상태로 유지되며, 
수행중인 thread가 완료될때까지 처리하지않습니다.

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <blocking-queueless-thread-pool name="MyScheduler">  
        <max-threads count="1" />  
    </blocking-queueless-thread-pool>  
</subsystem>
```

### 6) scheduled-thread-pool
java.util.concurrent.ScheduledThreadPoolExecutor class에 기반하여, 특정 시간과 특정 간격에 수행될 필요성이 있는 thread를 처리하는 방식입니다. 
명령을 주기적으로 수행할 수 있는 thread pool을 생성해야 할 시 사용하는 모델이라고 볼 수 있습니다. 

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
    <scheduled-thread-pool name="MyScheduler">  
        <max-threads count="1" />  
    </scheduled-thread-pool>    
</subsystem>
```

## Test unit

그럼 이제 주요 방식인 4가지를 테스트해보겠습니다. 

1. unbounded-queue-thread-pool
2. bounded-queue-thread-pool
3. blocking-bounded-queue-thread-pool
4. queueless-thread-pool

### base settings & conditions

standalone-*.xml :
```xml
<subsystem xmlns="urn:jboss:domain:threads:1.1">
            <unbounded-queue-thread-pool name="ajp-thread-pool-1">
                <max-threads count="10"/>
                <keepalive-time time="30" unit="seconds"/>
            </unbounded-queue-thread-pool>
            <bounded-queue-thread-pool name="ajp-thread-pool-2">
                <core-threads count="5"/>
                <queue-length count="5"/>
                <max-threads count="10"/>
            </bounded-queue-thread-pool>
            <blocking-bounded-queue-thread-pool name="ajp-thread-pool-3" allow-core-timeout="true">
                <core-threads count="2"/>
                <queue-length count="2"/>
                <max-threads count="1"/>
                <keepalive-time time="60" unit="seconds"/>
            </blocking-bounded-queue-thread-pool>
            <queueless-thread-pool name="ajp-thread-pool-4">
                <max-threads count="10"/>
                <keepalive-time time="10" unit="seconds"/>
            </queueless-thread-pool>
        </subsystem>
...

 <subsystem xmlns="urn:jboss:domain:web:2.2" default-virtual-server="default-host" native="false">
            <connector name="ajp" protocol="AJP/1.3" scheme="http" socket-binding="ajp" executor="[thread pool name]"/>
...

```

- JMeter Thread Properties
Number of Threads(Users):10
Ram-Up Period(in seconds):6
Loop Count:20
호출도메인 : http://IP/jbtest/sleep.jsp (5초간의 sleep time을 갖는 jsp파일)

### 1) unbounded-queue-thread-pool
```bash

./jboss-cli.sh --controller=172.21.70.24:10049 --connect --command="/subsystem=threads/unbounded-queue-thread-pool=ajp-thread-pool-1:read-resource(include-runtime=true)"

{

    "outcome" => "success",

    "result" => {

        "active-count" => 10,

        "completed-task-count" => 0L,

        "current-thread-count" => 10,

        "keepalive-time" => {

            "time" => 30L,

            "unit" => "SECONDS"

        },

        "largest-thread-count" => 10,

        "max-threads" => 10,

        "name" => "ajp-thread-pool-1",

        "queue-size" => 25,

        "rejected-count" => 0,

        "task-count" => 12L,

        "thread-factory" => undefined

    }

}
```
- current-thread-count : 현재 max thread count까지 사용되고있는것을 확인할 수 있습니다.
- queue-size : FIFO queue가 계속 늘어나며,  block상태의 thread가 점점 늘어나지만, reject되는 thread는 없음을 알 수 있습니다. 
block이 될경우,  java.net.SocketException: Socket closed(response data를 받습니다. 


### 2) bounded-queue-thread-pool
```bash

./jboss-cli.sh --controller=172.21.70.24:10049 --connect --command="/subsystem=threads/bounded-queue-thread-pool=ajp-thread-pool-2:read-resource(include-runtime=true)"

{

    "outcome" => "success",

    "result" => {

        "allow-core-timeout" => false,

        "core-threads" => 5,

        "current-thread-count" => 10,

        "handoff-executor" => undefined,

        "keepalive-time" => undefined,

        "largest-thread-count" => 10,

        "max-threads" => 10,

        "name" => "ajp-thread-pool-2",

        "queue-length" => 5,

        "queue-size" => 5,

        "rejected-count" => 18,

        "thread-factory" => undefined

    }

}
```

- current-thread-count : 현재 max thread count까지 사용되고있는것을 확인할 수 있습니다.
- queue-size : 설정한 queue-length만큼 queue가 쌓인것을 확인할 수 있습니다.
- rejected-count : queue에서 처리가능한 thread를 제외하고 reject된 count수입니다. 점점 늘어나고 있는것을 확인할 수 있었습니다.
 reject될시, 502 Bad Gateway(response data)를 받게됩니다. 

따라서, max thread count가 찬 이후에는 queue-length만큼 thread가 대기하게 되며, 이후 요청은 reject됨을 알 수 있습니다.

> 추가적으로 bounded-queue-thread-pool 에서는 handoff executor를 설정할 수 있습니다. <br>
메인 ajp-thread-pool의 queue까지 가득찰 경우, handoff executor를 지정하게되면 또 하나의 thread pool을 사용할 수 있습니다.<br> 
하지만 이 추가적인 thread pool의 queue까지 가득찰 경우, 이후 요청은 모두 reject됩니다.

```xml
    <bounded-queue-thread-pool name="ajp-thread-pool-2">
        <core-threads count="5"/>
        <queue-length count="5"/>
        <max-threads count="10"/>
        <handoff-executor name="handoff-ajp-thread-pool-2"/>
    </bounded-queue-thread-pool>

    <bounded-queue-thread-pool name="handoff-ajp-thread-pool-2">
        <core-threads count="5"/>
        <queue-length count="5"/>
        <max-threads count="10"/>
    </bounded-queue-thread-pool>
```

### 3) blocking-bounded-queue-thread-pool
```bash
./jboss-cli.sh --controller=172.21.70.24:10049 --connect --command="/subsystem=threads/blocking-bounded-queue-thread-pool=ajp-thread-pool-3:read-resource(include-runtime=true)"

{

    "outcome" => "success",

    "result" => {

        "allow-core-timeout" => true,

        "core-threads" => 5,

        "current-thread-count" => 10,

        "keepalive-time" => {

            "time" => 10L,

            "unit" => "SECONDS"

        },

        "largest-thread-count" => 10,

        "max-threads" => 10,

        "name" => "ajp-thread-pool-3",

        "queue-length" => 5,

        "queue-size" => 5,

        "rejected-count" => 0,

        "thread-factory" => undefined

    }

}
```

- current-thread-count : 현재 max thread count까지 사용되고있는것을 확인할 수 있습니다.
- queue-size : queue는 모두 사용되는 상태로, block상태의 thread가 점점 늘어나지만, reject되는 thread는 없음을 알 수 있습니다.
block이 될경우,  java.net.SocketException: Socket closed.(response data...) 를 받습니다.


### 4) queueless-thread-pool
```bash
./jboss-cli.sh --controller=172.21.70.24:10049 --connect --command="/subsystem=threads/queueless-thread-pool=ajp-thread-pool-4:read-resource(include-runtime=true)"

{

    "outcome" => "success",

    "result" => {

        "current-thread-count" => 10,

        "handoff-executor" => undefined,

        "keepalive-time" => {

            "time" => 10L,

            "unit" => "SECONDS"

        },

        "largest-thread-count" => 10,

        "max-threads" => 10,

        "name" => "ajp-thread-pool-4",

        "queue-size" => 58,

        "rejected-count" => 58,

        "thread-factory" => undefined

    }

}
```

- current-thread-count : 현재 max thread count까지 사용되고있는것을 확인할 수 있습니다.
- queue-size/rejected-count: 동일하게 증가되는 현상을  확인할 수 있었습니다. 
*해당 부분은 jboss 6.4r기준 queue-size 에 대한 bug로, queue-size는 count되지않고 reject-count만 count되도록 patch를 진행중에 있습니다. 따라서, queue-size는 무시하고 reject-count만 확인하면 됩니다.* 
해당 방식은 단순 long running task를 위한 방식이기때문에, 충분한 max thread count를  산정하는것이 좋을것으로 판단됩니다.



## 결론
1) queue만 있는경우
    
    queue에 계속 쌓임>OOME발생가능성 높음

2) queue가 있고, non-block인 경우
    
    max-thread를 초과>queue에 담김>queue초과>reject 

3) queue가 있고, block인경우

    max-thread를 초과>queue에 담김>queue초과>block(thread lock)

4) queue가 없고, non-block인 경우

    max-thread를 초과>reject 

  | unbounded | bounded(non-blocking) | blocking-bounded | queueless
---|---|---|---
queue 유무 | O(FIFO) | O | O | X
reject 유무 | X | O | X | O
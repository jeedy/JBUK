# Redis Cluster (sharding) 셋팅방법


### 클러스터에 필요한 파라미터: 아래 파라미터들은 redis.conf 파일에 있고, 디폴트로 주석으로 되어 있다.
- cluster-enabled yes : yes로 하면 cluster mode로 시작한다. no로 하면 standalone mode로 시작한다.
- cluster-config-file nodes.conf : 이 파일은 클러스터의 상태를 기록하는 바이너리 파일이다. 클러스터의 상태가 변경될때 마다 상태를 기록한다.
- cluster-node-timeout 3000 : 레디스 노드가 다운되었는지 판단하는 시간이다. 단위는 millisecond이다.
- port open : 방화벽(firewall)을 사용하고 있다면 기본 포트에 10000을 더한 클러스터 버스 포트도 열려있어야 한다.  예를 들어 기본 포트로 7000번을 사용한다면 17000번 포트도 같이 열어야 한다.


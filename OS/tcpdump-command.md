# tcpdump 명령어 사용방법

> 본 command는 ROOT 권한이 있어야 한다.

A 서버에서 특정 B 서버로 호출하는 경우가 있는지를 확인해보고 싶어서 명령어를 찾던준에 알게되었다. 사용법은 간단하다


```
$ tcpdump -D
1.eth0
2.nflog (Linux netfilter log (NFLOG) interface)
3.nfqueue (Linux netfilter queue (NFQUEUE) interface)
4.eth1
5.any (Pseudo-device that captures on all interfaces)
6.lo

# 위 네트워크 인터페이스중에 하나 골라서 dump (*아래예제에서는 4.eth1)
$ tcpdump -nn -i eth1 port 4000
```


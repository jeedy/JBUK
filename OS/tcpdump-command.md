# tcpdump 명령어 사용방법

### 참고자료
- [tcpdump](./images/Tcpdump_description.pdf)

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

# 실시간 TCP DUMP 예시
```sh
# redis ()
#$ sudo tcpdump -nnnNxX -s 0 'src net 192.168.0.41 and dst port 6379 or src port 6379 and dst net 192.168.0.41'
[Redis:~$]$ sudo tcpdump -nnnNxX -s 0 -i any 'net 192.168.0.41'

# was (가정: 192.168.0.41)
[tomcat:WAS:~$]sudo tcpdump -nnnNxX -s 0 port 6379
```


### 번외

추후 알게되었지만 tcpdump를 이용하지 않고 netstat로 확인할 수 있다.

```
$ watch -n 1 "netstat -ntu | awk '{print \$5}' | cut -d: -f1 | sort | uniq -c | sort -n"
```



#
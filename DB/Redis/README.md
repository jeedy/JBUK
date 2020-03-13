# Redis

## 목차

1. [레디스 설치방법](./redis-server-install.md)
2. [레디스 GUI 클라이언트 프로그램 설치](./Redis-client-install.md)
3. [레디스 replication 구성 방법](./redis-replication-setting.md)
4. [레디스 클러스터링 구성 방법(미완)](./redis-cluster-setting.md)
5. [레디스 백업 및 성능 퍼포먼스 셋팅](./Redis-backup-performance-setting.md)

## :bomb: troubleshooting
### 1. 메모리 사용량 확인
참고
- https://zetawiki.com/wiki/Redis_INFO_MEMORY
- http://redisgate.kr/redis/server/memory.php (메모리에 대한 자세한 내용을 확인하고 싶을때)

#### 사용량 체크
info memory:
```bash
$ redis-cli info memory

used_memory:7780464             # (byte, 레디스의 메모리 사용량)
used_memory_human:7.42M         # (used_memory의 휴먼리더블 표현)
used_memory_rss:9510912         # (byte, OS에서 보이는 레디스 메모리 사용량)
used_memory_peak:10855912       # (byte, 메모리 최대 사용량)
used_memory_peak_human:10.35M   # (used_memory_peak의 휴먼리더블 표현)
used_memory_lua:33792           # (byte, 루아 엔진의 메모리 사용량)
mem_fragmentation_ratio:1.22    # (used_memory_rss 와 used_memory의 비율)
mem_allocator:jemalloc-3.2.0    # (메모리 할당자(컴파일시에 선택한 것))
```

#### 메모리 점검
memory doctor:
```bash 
127.0.0.1:6000> MEMORY doctor

```

*경우에 따라 다음과 같은 권고사항이 나옵니다.*

- 사용 메모리가 5MB 미만이면: 
Hi Sam, this instance is empty or is using very little memory, my issues detector can't be used in these conditions. Please, leave for your mission on Earth and fill it with some data. The new Sam and I will be back to our programming as soon as I finished rebooting.
사용 메모리가 5MB 미만이면 권고사항이 없습니다.
Peak is > 150% of current used memory? : mh->peak_allocated / mh->total_allocated) > 1.5 
- Peak memory: In the past this instance used more than 150% the memory that is currently using. The allocator is normally not able to release memory after a peak, so you can expect to see a big fragmentation ratio, however this is actually harmless and is only due to the memory peak, and if the Redis instance Resident Set Size (RSS) is currently bigger than expected, the memory will be used as soon as you fill the Redis instance with more data. If the memory peak was only occasional and you want to try to reclaim memory, please try the MEMORY PURGE command, otherwise the only other option is to shutdown and restart the instance.
Fragmentation is higher than 1.4? : mh->fragmentation > 1.4 
- High fragmentation: This instance has a memory fragmentation greater than 1.4 (this means that the Resident Set Size of the Redis process is much larger than the sum of the logical allocations Redis performed). This problem is usually due either to a large peak memory (check if there is a peak memory entry above in the report) or may result from a workload that causes the allocator to fragment memory a lot. If the problem is a large peak memory, then there is no issue. Otherwise, make sure you are using the Jemalloc allocator and not the default libc malloc. Note: The currently used allocator is malloc size.
Slaves using more than 10 MB each? : mh->clients_slaves / numslaves > (1024*1024*10) 
- Big slave buffers: The slave output buffers in this instance are greater than 10MB for each slave (on average). This likely means that there is some slave instance that is struggling receiving data, either because it is too slow or because of networking issues. As a result, data piles on the master output buffers. Please try to identify what slave is not receiving data correctly and why. You can use the INFO output in order to check the slaves delays and the CLIENT LIST command to check the output buffers of each slave.
Clients using more than 200k each average? : (mh->clients_normal / numclients(normal.clients - slave.clients) > (1024*200)
- Big client buffers: The clients output buffers in this instance are greater than 200K per client (on average). This may result from different causes, like Pub/Sub clients subscribed to channels bot not receiving data fast enough, so that data piles on the Redis instance output buffer, or clients sending commands with large replies or very large sequences of commands in the same pipeline. Please use the CLIENT LIST command in order to investigate the issue if it causes problems in your instance, or to understand better why certain clients are using a big amount of memory.
# influxDB

## select 
https://docs.influxdata.com/influxdb/v1.8/query_language/explore-data/

```sql
select time, server_timestamp, korean_time, * from "webtracking-V10-dev" where time>='2021-09-09 16:41:09' and time <= '2021-09-09 17:41:09' tz('Asia/Seoul')
```

## write
https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_reference/

## Retention Policy(만료, expire) 방법 
https://jhleeeme.github.io/influxdb-retention-policy/

```sh
$ influx

> use telegraf
> show retention policies
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true
> alter RETENTION POLICY "autogen" on "telegraf" DURATION 2h SHARD DURATION 1h
> show retention policies
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 2h0m0s   1h0m0s             1        true
```
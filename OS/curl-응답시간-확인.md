# curl를 이용한 응답시간 체크

> -w 옵션을 이용해서 여러 응답시간 체크가능하다.

- `%{time_namelookup}` : it took from the start until the name resolving was completed.
    - DNS 서버에서 도메인 찾는데 걸린 시간
- `%{time_connect}` : it took from the start until the TCP connect to the remote host (or proxy) was completed.
    - 서버 접속시간
- `%{time_appconnect}` : it took from the start until the SSL/SSH/etc connect/handshake to the remote host was - completed.
- `%{time_pretransfer}` : it took from the start until the file transfer was just about to begin. This includes all pre-transfer commands and negotiations that are specific to the particular protocol(s) involved.
    - 
- `%{time_redirect}` : it took for all redirection steps including name lookup, connect, pre-transfer and transfer before the final transaction was started. time_redirect shows the complete execution time for multiple redirections.
- `%{time_starttransfer}` : shows the time, in seconds, it took from the start until the first byte was just about to be transferred. This includes time_pretransfer and also the time the server needed to calculate the result.
    - 파일 전송시간
- `%{time_total}` : shows the total time, in seconds, that the full operation lasted. The time will be displayed with millisecond resolution.

예시)
```sh
curl -v -s -w 'time_total:%{time_total} time_namelookup:%{time_namelookup} time_connect:%{time_connect} time_appconnect:%{time_appconnect} time_pretransfer:%{time_pretransfer} time_redirect:%{time_redirect} time_starttransfer:%{time_starttransfer}' "https://tistory.com"
```
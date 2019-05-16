# hosts 파일 주소 위치 및 수정방법

참고
- https://storycompiler.tistory.com/118  위치와 수정 및 반영 참고

## 위치 /etc/hosts
```bash
$ cat /etc/hosts
127.0.0.1    localhost
127.0.1.1    storycompiler
```

## 수정 및 반영
```bash
$ vi /etc/hosts

..(내용수정)..

$ sudo /etc/init.d/networking restart
[ ok ] Restarting networking (via systemctl): networking.service.
```
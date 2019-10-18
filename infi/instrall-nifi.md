# Nifi 설치 방법

## 참고자료
-  https://nifi.apache.org/docs/nifi-docs/html/getting-started.html#downloading-and-installing-nifi (설치방법 및 실행)

## 다운로드 & 설치 
```bash
$ cd ~
$ wget http://apache.mirror.cdnetworks.com/nifi/1.9.2/nifi-1.9.2-bin.tar.gz
$ sudo mv nifi-1.9.2-bin.tar.gz /usr/local/
$ cd /usr/local/
$ sudo tar -zxvf nifi-1.9.2-bin.tar.gz
$ sudo chown -R ec2-user:ec2-user nifi-1.9.2/
```

## 실행
```bash
$ cd /usr/local/nifi-1.9.2/
# bin/nifi.sh run # 실행
$ bin/nifi.sh start # background 로 실행
...

```

## 종료
```bash
$ cd /usr/local/nifi-1.9.2/
$ bin/nifi.sh stop
...

```

## 리스타트
```bash
$ cd /usr/local/nifi-1.9.2/
$ bin/nifi.sh restart
...

```





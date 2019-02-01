# ssh 접속시 처음 접속하는 호스트 확인 생략, known_hosts 등록 방법

참고 사이트
- https://junho85.pe.kr/667 (ssh-keyscan 사용법, StrictHostKeyChecking command 사용법)


ssh로 특정 host 접속하려고 할때 아래와 같은 확인 메시지가 나온다.
```bash
$ ssh junho85.pe.kr
The authenticity of host 'www.myhostserver.com (111.111.111.xxx)' can't be established.
RSA key fingerprint is 2f:e1:a7:bd:e4:56:53:xx:xx:xx:xx:xx:xx:xx:xx:xx.
Are you sure you want to continue connecting (yes/no)?
```
Yes 체크 하지 않으면 ssh 접속 및 명령어 호출이 불가능한데, 배포를 위해 ant나 셀 스크립트를 통해 호출을 하려고 할때 실패하게 된다.

처음에 한번 체크해 주면 다음 부터는 안나오는 메시지라 기억하기 힘들기 때문에 만약 배포서버를 재구축할 경우 이런 문제를 놓치고 가게되고 이미 한번 그 경험이 있어 confirm 메시지를 무시(생략) 할수 있는 방법이 무엇이 있을까 찾아보게 되었다.

## ssh 옵션 StrictHostKeyChecking=no 이용하기

ssh 실행시 옵션을 이용하면 yes/no 물어보는 것을 생략하고 바로 해당 host 를 `known_hosts` 에 추가하고 실행한다.

```bash
$ ssh -o  StrictHostKeyChecking=no www.myhostserver.com whoami
```

실제 환경에서 핑커 프린트가 변경된 경우는 뭔가 이상이 있는 경우이기 때문에 StrictHostKeyChecking=no 옵션을 사용하는 방식은 `비추`하고 있다.

## ssh-keyscan 이용하여 여러 host 등록 하는 방법

다른 방법으로 사전에 미리 여러 서버들을 scan해서 `known_hosts` 에 추가하는 방법이다. (이 방법은 사실 ssh-keyscan을 사용하지 않고 셀 스크립트에서 `ssh -o StrictHostKeyChecking=no`를 for문으로 등록하는 방법과 비슷할 것같다.)

```
$ ssh-keyscan -t rsa host명 >> ~/.ssh/known_host
```

OR

```
$ ssh-keyscan -t rsa -f host명들 이들어있는 파일명 >> ~/.ssh/known_host
```

## (비추천) ssh 설정 바꾸기

이방식은 진짜 **비추천** 하지만 혹시 이렇게 셋팅해 사용하는 사이트를 관리해야할 때를 대비해 알아두면 좋을것 같다.

`~/.ssh/config` 설정에 다음 내용을 추가 해 주면 된다.
```bash
(in ~/.ssh/config)
Host *
    StrictHostKeyChecking no
```

이후 해당 파일 권한을 400(사용자 읽기 권한만) 으로 바꿔 준다.

```bash
$ sudo chmod 400 ~/.ssh/config
```

## about ssh

> SSH 서버는 접속을 시도하는 호스트의 키 지문(key fingerprint)을 저장합니다. 기본적으로 ECDSA 방식의 암호화 기술을 사용하기 때문에 호스트 공개키는 /etc/ssh/ssh_host_ecdsa_key.pub에 저장됩니다. ssh-keygen 명령으로 호스트 키 지문을 확인할 수 있습니다.

```
administrator@server001:~$ ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub
256 d9:ca:30:2b:6c:80:7a:41:ac:07:7e:ec:f2:ec:af:57 root@server01 (ECDSA)
```

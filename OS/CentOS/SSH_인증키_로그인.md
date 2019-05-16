# [CentOS] SSH 인증키 로그인

새로 설치된 CentOS 서버에 공개키를 넣었는데도 SSH 로그인 할 때 마다 비밀번호를 물어봤다. 아래는 삽질하면서 알게 된 내용이다.

우선 .ssh 디렉토라와 authorized_keys 파일의 권한을 확인해야 한다.
.ssh 는 `0700`, authorized_keys 는 `0600`으로 설정되어 있어야 한다.
내 경우에는 group이나 others에 더 높은 권한이 허용되어 있었는데 이게 문제인지는 모르겠으나 `0700`, `0600` 으로 권한 설정을 다시 하니 문제가 해결 됐다.

서버에서 공개키 기반 인증이 허용되어 있어야 한다. CentOS의 경우에는 /etc/ssh/sshd_config에 설정파일이 있는데
아래의 내용이 활성화되어 있는지 확인한다. 내 경우에는 모두 주석처리가 되어있었다.

```bash
$ vi /etc/ssh/sshd_config
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile     .ssh/authorized_keys

$ service sshd restart
```

주석을 풀고 sshd를 재기동한다.

처음에는 권한을 건드리지 않은 상태에서 주석만 풀고 재기동 했는데 작동이 안되었다. StackOverflow의 댓글을 읽다가 권한 설정을 다시 하니까
해결됐다는 글을 보고 나도 똑같이 해결했는데, 권한이 더 많은데도 왜 작동을 안했는지는 잘 모르겠다(보안상 권한이 너무 많아도 안되나?).

참고사항 : 이게 OS 또는 버전에 따라 조금씩 다른 것 같더군요. 설정에 영향이 있는 것일 수도 있구요.

일단 기본적으로 0700 ~/.ssh/, 0600 ~/.ssh/authorized_keys는 기본인데 어떤 경우는 ~/. 가 0700 이어야 동작하는 경우도 있었습니다.


Thx Kyg
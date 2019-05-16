# [CentOS] Password 만료 기간, 복잡도 설정

운영서버 보안을 위한 계정 패스워드의 주기적 변경이 필요하다.

```bash
$ vi /etc/login.defs
...
PASS_MAX_DAYS    99999
PASS_MIN_DAYS    0
PASS_MIN_LEN     5
PASS_WARN_AGE    7
...
...

[ [ 설명 ] ]
PASS_MAX_DAYS    90    // 패스워드 최대 사용 기간(90일)
PASS_MIN_DAYS    1     // 패스워드 최소 사용 기간(1일)
PASS_MIN_LEN     8     // 패스워드 길이(대소문자 구분 없음)
PASS_WARN_AGE    7     // 만료되기 전 알림 시기(7일 전부터)
```

```bash
$ vi /etc/pam.d/system-auth
password    requisite     pam_cracklib.so try_first_pass retry=3 type= minlen=8 dcredit=-1 ucredit=-1 lcredit=-1 ocredit=-1

- dcredit=-1      // 숫자
- ucredit=-1      // 대문자
- lcredit=-1      // 소문자
- ocredit=-1      // 서로 다른 문자
```

각 항목에서 값이 -1로 설정하면 해당하는 것을 반드시 포함시켜야 한다.
(즉, dcredit=-1은 패스워드에 숫자를 반드시 포함해야만 한다.)


Thx Kyg


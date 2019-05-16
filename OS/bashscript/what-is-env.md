# env

### 참고자료
- https://blog.gaerae.com/2015/10/what-is-the-preferred-bash-shebang.html

```bash
# 환경 변수 정보 출력
env

# 현재 환경을 무시하고 지정한 값을 사용
env -i HOSTNAME=test.com

# 지정한 변수 제거
env -u HOSTNAME

# env 이용한 bash 실행하기
/usr/bin/env bash --version
```
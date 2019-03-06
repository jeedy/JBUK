# awk

데이터를 조작하고 리포트를 생성하기 위해 사용하는 언어

### 참고자료
- https://zzsza.github.io/development/2017/12/20/linux-6/
- https://ra2kstar.tistory.com/153

```bash
# filename 에서 pattern 의 line 검색
$ awk 'pattern' filename

# filename 에서 모든 line 마다 {action} 실행
$ awk '{action}' filename

# filename 에서 pattern 의 line 에서 {action} 실행
$ awk 'pattern {action}' filename
```

```bash
$ cat awkfile
홍 길동 3324    5/11/96 50354
임 꺽정 5246    15/9/66 287650
이 성계 7654    6/20/58 60000
정 약용 8683    9/40/48 365000

$ awk '/길동/' awkfile
> 홍 길동	3324	5/11/96	50354

$ awk '{print $0}' awkfile
>
홍 길동 3324    5/11/96 50354
임 꺽정 5246    15/9/66 287650
이 성계 7654    6/20/58 60000
정 약용 8683    9/40/48 365000

$ awk '{print $1}' awkfile
>
홍
임
이
정

$ awk '/정/{print "\t안녕하세요? " $1, $2 "님!"}' awkfile
>
  안녕하세요? 임 꺽정님!
  안녕하세요? 정 약용님!

$ df | awk '$4 < 100000' : |을 이용해 파이프라인 생성
>
devfs			368       368       0   100%     638          0  100%   /dev
map -hosts	0         0         0   100%       0          0  100%   /net
map auto_home	0         0         0   100%       0          0  100%   /home
```

## 내부변수
변수명 | 내용
--- | ---
FILENAME | 현재 처리중인 파일명
FS | 필드 구분자로 디폴트는 공백
RS | 레코드 구분자로 디폴트는 새로운 라인
NF | 현재 레코드의 필드 개수
NR | 현재 레코드의 번호
OFS | 출력할 때 사용하는 FS
ORS | 출력할 때 사용하는 RS
$0 | 입력 레코드의 전체
$n | 입력 레코드의 n번째 필드


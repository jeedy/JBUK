# 연습

### 2019-01-16

- `i` 커서 위치 insert 모드. `ESC` 를 누르면 Normal 모드로 되돌아 온다.

- `a` 커서 뒤 insert 모드

- `o` 커서 다음줄에 insert 모드

- `x` 커서의 위치에 있는 문자를 지운다.

- `:wq` 저장 후 종료

- `dd` 현재 행 삭제 (그리고 복사, `p` 로 붙여넣기)

- `p` 붙여 넣기

- `hjkl` 커서 이동

- `:! ls` 셀 실행

- `:r! ls` 셀 명령어 출력내용 Editor에 가져와 뿌려주기

### 2019-02-21

- `vsp 파일명` 창 세로분리해서 파일 열기

- `Ctrl+w` 창 이동 , `:q` 창닫기

- `y` 복사

- `p` 붙여놓기

- `Ctrl + f` 한페이지 (forward) 스크롤,  `Ctrl + d` 반페이지 (down) 스크롤

- `Ctrl + b ` 한페이지 (back) 스크롤, `Ctrl + u` 반페이지 (up) 스크롤

### 2019-07-25
- `:set nu` 라인번호 나오게

- `CTRL+g`, `:f` 파일명 보기

- `u` undo 작업취소, `U` 현재줄에서 undo

- `CTRL+r` redo 다시 하기

- ':sh' 셀모드로 나가기 , `Ctrl +d` 복귀

- 'Ctrl+z` 셀모드로 나가기, `fg` 복귀

### 2020-01-13

#### sp, vsp 창 분리
```
가로형으로 분리
:sp 파일명

세로형으로 분리
:vsp 파일명

창닫기
:q

창이동
Ctrl + w

"Swap top/bottom or left/right split
Ctrl+W R

"Break out current window into a new tabview
Ctrl+W T

"Close every window in the current tabview but the current one
Ctrl+W o
```
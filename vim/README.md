# VIM

### 유용한 사이트
- https://nolboo.kim/blog/2016/11/15/vim-for-beginner/ 완전 초보를 위한 Vim
- http://www.mimul.com/pebble/default/2014/07/15/1405420918073.html 점진적으로 학습하기
- https://vim.rtorr.com/lang/ko/ Vim Cheat Sheet
- https://vim-adventures.com/  vim-adventures

## 쉘로 빠져나가기
```vim
:shell 또는 :sh

되돌아오기

exit
```


## :! 명령어 실행
```vim
:! ls
```

#### :r ! 명령어로 출력된 내용 editor에 가져와 뿌려주기
```vim
:r ! ls
```


## sp, vsp 창 분리
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

## 옵션
옵션 | 옵션 약어 | 기능 | 디폴트
---|---|---|---
autoindent | ai | 들여 쓰기 가능, 탭으로 들여 쓰기 범위 지정 | off
autoprint | ap | 줄이 바뀔 때 현재 줄을 화면상에서 출력 | on
errobells | ed | 명령 에러가 발생시 삑 소리나게 함 | off
number | nu | 줄 번호를 나타나게 함 | off
report | report | 편집시 메시지를 보낼 편집 변화 크기 지정 | 5
showmatch | sm | 가로 닫기 괄호를 사용할 때 일치하는 가로 열기 괄호를 보여줌 | off
wam | wam | 저장하지 않고 vi 종료할 때 경고 메시지를 뿌려 줌 | on
ignorecase | ic | 검색 패턴에 사용되는 대소문자 구별하지 않음 | on
tabstopp=n | ts=n | 탭 공백을 n 수 만큼 지정 | 8
wrapmargin=n | wm=n | 텍스트 오른쪽 여백을 n 수 만큼 지정 | 0



## 단축키
![이동단축키](./images/Vim_이동_단축키_white.jpg)

![명령어단축키](./images/Vim_명령어_단축키.jpg)

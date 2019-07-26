# JBUK

검색 사이트에 검색 되지 않은 나만의 이야기
배우고 경험한 내용을 형식에 얽매이지 않고 담아내는
블로그를 운영하는 것도 귀찮고 검색되어 나오는것도 귀찮음
내가 쓰고 내가 읽으려고 만듦 :dromedary_camel:

## Markdown 기본 문법

[Github markdown document 참조](https://guides.github.com/features/mastering-markdown/)

[이모지 라이브러리](https://www.webpagefx.com/tools/emoji-cheat-sheet/)

![이미지](./images/markdown-syntax-language.png)

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/3Wf29RiKp70/0.jpg)](http://www.youtube.com/watch?v=3Wf29RiKp70)


**굵은 글씨**

*기울림*

~~this~~

1. 목록
1. 목록

- 리스트
- 리스트

> 블럭
2줄 가능

```bash
$ echo '터미널 명령어 입력할때'
```

```java
String msg = "자바 코드 입력 할때";
Sysout.out.println(msg);
```

말머리 (#과 같은 효과)
======

----

## 로컬 설치 (git clone)
```bash
$ git clone https://github.com/jeedy/JBUK.git
$ cd JBUK
$ git remote set-url origin https://jeedy@github.com/jeedy/JBUK.git
```
이후 설정파일(.git/config)에서 
```
[user]
	name = jeedy
	email = kk59491@gmail.com
```
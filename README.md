# JBUK

일하면서 배우게된 내용을 기록 :dromedary_camel:

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
$ git clone -b revision --single-branch https://github.com/jeedy/JBUK.git
$ cd JBUK
$ git remote set-url origin https://jeedy@github.com/jeedy/JBUK.git
```
이후 설정파일(.git/config)에서 
```
[user]
	name = jeedy
	email = kk59491@gmail.com
```

## :bomb: troubleshooting
> 스터디 하면서 겪었던 문제 그리고 해결방법을 기록하자
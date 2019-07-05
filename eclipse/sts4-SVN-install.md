# STS 4.0 이상 SVN 설치방법


STS4.0버전을 깔고 SVN plugin을 설치하고

![플러그인 설치](./images/sts4-svn-plugin-install.PNG)
 
`svn://172.16.0.21:8888/sampleProject` 프로젝트를 연결하려고하면

```
    Can't create session
svn: Unable to connect to a repository at URL 'svn://172.16.0.21:8888/sampleProject'
Cannot negotiate authentication mechanism
```

이와같은 에러가 발생해서 연결이 안되는 경우가 있다. 이럴경우 svn 인터페이스를 한번 살펴보자

eclipse > window > preferences > Team > SVN :

![설정화면](./images/sts4-preferences-svn.PNG)

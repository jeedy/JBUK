# Travis CI 셋팅 및 SonarQube(SonarCloud) 연동

## Github - Travis CI - SonarCloud

Github에 특정 Branch 커밋될 때 마다 Travic CI 가 Hook 해서 빌드 후 SonarQube 가 소스 분석

## Travis CI 가입

https://travis-ci.com/
(https://travis-ci.org/ 이 주소도 있는데 이건 뭔지 모르겠음 위 주소와 연동안됨)

Github 계정을 이용해 가입 가능 (bitbuket으로도 가입 가능)

## SonarCloud 가입

https://sonarcloud.io

## github에서 Travis CI 빌드 방법

/.travis.yml 파일 하나만 생성해 주면 된다.(너무 간단)

```yml
language: java
jdk:
  - oraclejdk8
  - openjdk8
```

## Travis CI 빌드시 SonarQube Scanner 적용

/.travis.yml 파일에 소나큐브 옵션은 addon 하면 된다. 너무 간단한데 근데 sonarcloud 밑에 organiztion: , token:secure: 값은 어디서 보고 써야하는지 찾아봐야해서 기록해 놓는다.

- organization: https://sonarcloud.io/account/organizations > 페이지에 key 라고 써있는 값
- token:secure: https://sonarcloud.io/account/security/ > Generate Tokens > 토큰 생성(*생성된 토큰값 복사, 페이지 이동하면 토큰값 볼수없음)

```yml
language: java
jdk:
  - oraclejdk8
  - openjdk8

addons:
  sonarcloud:
    organization: "jeedy-github"
    token:
      secure: 0d0fa4bd03ee391368b059d92a7b5fd225c016cb
script:
  - mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install sonar:sonar
```




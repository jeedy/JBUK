# CentOS 에서 메이븐 설치

## 선행작업
CentOS에 JDK 설치

## 메이븐 다운로드
```bash
su -
cd /usr/lib/
root:/usr/lib# wget http://www-eu.apache.org/dist/maven/maven-3/3.5.3/binaries/apache-maven-3.5.3-bin.tar.gz
```

## 압축풀기
```bash
root:/usr/lib# sudo tar xzf apache-maven-3.5.3-bin.tar.gz
```

## 심볼릭링크(생략가능)
```bash
root:/usr/lib# sudo ln -s apache-maven-3.5.3 maven
```

## 환경설정
```bash
root:/usr/lib# vi /etc/profile.d/maven.sh
```

```bash
# setting environment in /etc/profile.d/maven.sh
export MAVEN_HOME=/usr/lib//maven
export PATH=${MAVEN_HOME}/bin:${PATH}
```

## 환경설정 적용
```bash
root:/usr/lib# source /etc/profile.d/maven.sh
```

## 확인
```bash
root:/usr/lib# mvn -version
```
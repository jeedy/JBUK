# ssl 인증기관 추가 방법

## 1. Java JDK 인증기관 추가 방법

### 1.1. 테스트방법
httpclient 같은 라이브러리를 통해 테스트 해볼수있는 URL주소(`https://global-root-g2.chain-demos.digicert.com/`)를 호출해본다.

자바의 인증서 저장소에 인증서를 추가하지 않으면 https 통신 중 SSLHandshakeException, PKIX Exception 등의 오류가 발생하게 된다.


### 1.2. (window) cmd 를 이용한 추가
예시) 
```sh
## 등록된 인증기관 리스트 확인
C:\Java\jdk1.7.0_79>keytool -keystore "C:\Java\jdk1.7.0_79\jre\lib\security\cacerts" -storepass changeit -list -v

## 추가
C:\Java\jdk1.7.0_79\jre\lib\security> keytool -import -keystore cacerts -file "DigiCertGlobalRootG2.crt" -alias "DigiCertGlobalRootG2"

키 저장소 비밀번호 입력: (changeit 입력)

소유자: CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US
발행자: CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US

...

이 인증서를 신뢰합니까? [아니오]:  y
인증서가 키 저장소에 추가되었습니다.
```

### 1.3. (linux) shell 를 이용한 추가
```sh
$ cd /jdk1.7.0_79/jre/bin
$ wget https://cacerts.digicert.com/DigiCertGlobalRootG2.crt
$ ./keytool -import -keystore ../lib/security/cacerts -file "DigiCertGlobalRootG2.crt" -alias "DigiCertGlobalRootG2"

키 저장소 비밀번호 입력: (changeit 입력)

소유자: CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US
발행자: CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US

...

이 인증서를 신뢰합니까? [아니오]:  y
인증서가 키 저장소에 추가되었습니다.

# 서버 재기동없이 바로 반영된다.

```

### 1.4. 어플을 이용한 추가
참고: https://advenoh.tistory.com/29



## 2. curl 어플리케이션 ssh 인증기관 추가
참고: https://www.lesstif.com/gitbook/curl-ca-cert-15892500.html

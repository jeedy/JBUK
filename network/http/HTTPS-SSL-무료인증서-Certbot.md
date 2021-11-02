# 무료 SSL 인증서 발급 및 자동갱신
tags: ssl, tls, https, Certbot, 443, linux, aws, Amazon Linux 2, tomcat, spring-boot


## (option) Certbot 설치 (for Amazon Linux2)
### 1. EPEL 리포지토리를 활성화
참고: https://aws.amazon.com/ko/premiumsupport/knowledge-center/ec2-enable-epel/

```sh
$ sudo amazon-linux-extras install epel -y

$ sudo yum-config-manager --enable epel
```

### 2. Certbot 설치
```sh
$ sudo yum install -y certbot
``` 


## 1. 인증키 발급 (Cerbot webroot)

Certbot 을 통해 인증키를 발급 받는 방법은 2가지 방식이 있다. 
- standalone : certbot 이 알아서 로컬에 80 서버를 띄워서 인증하는 방식, 간단하지만 단점은 로컬 80 port를 사용하는 서버는 shutdown 해야한다. 이 방식을 사용하게 되면 갱신할때 늘 서버를 shutdown해야한다.
- webroot : tomcat(또는 spring-boot) resource file들이 위치한 곳에 암호화된 파일을 올려 읽어들이는 방식, 초반에 셋팅이 좀 까다롭지만 하고 나면 shutdown 없이 갱신이 가능해진다.

### 1.1. standalone 방식으로 발급
참고: https://foxydog.tistory.com/63?category=809111

### 1.2. webroot 방식으로 발급
verification file이 생성될 위치를 `/usr/local/tomcat8.5/webapps/ROOT/WEB-INF/classes/static/`로 설정 한다.

```sh
# 인증서발급
$ sudo certbot certonly --webroot -w /usr/local/tomcat8.5/webapps/ROOT/WEB-INF/classes/static/ -d [도메인주소]

.... 
(이메일 주소 입력)
...
Waiting for verification...
Cleaning up challenges

# 인증서발급 확인
$ sudo certbot certificates
```
> 설정된 파일 위치는 `/etc/letsencrypt/renewal/[도메인주소].conf` 이다. 파일을 열어보면 갱신할때 필요한 정보들이 담겨있다.

## 2. 인증키 등록 (tomcat)
참고: https://trend21c.tistory.com/2172


conf/server.xml:
```xml
...

    <Connector port="443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true">
        <SSLHostConfig>
            <Certificate certificateKeyFile="/etc/letsencrypt/live/[도메인주소]/privkey.pem"
                         certificateFile="/etc/letsencrypt/live/[도메인주소]/cert.pem"
                         certificateChainFile="/etc/letsencrypt/live/[도메인주소]/chain.pem"
                         type="RSA" />
        </SSLHostConfig>
    </Connector>

...
```

> 주의 `org.apache.coyote.http11.Http11NioProtocol` 프로토콜을 이용하자

## 3. 인증키 자동 갱신
```sh
# 인증서 갱신 테스트
$ sudo certbot renew --dry-run
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/[도메인주소].conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Cert not due for renewal, but simulating renewal for dry run
Plugins selected: Authenticator webroot, Installer None
Simulating renewal of an existing certificate for [도메인주소]
Performing the following challenges:
http-01 challenge for [도메인주소]
Using the webroot path /usr/local/tomcat8.5/webapps/ROOT/WEB-INF/classes/static/ for all unmatched domains.
Waiting for verification...
Cleaning up challenges

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
new certificate deployed without reload, fullchain is
/etc/letsencrypt/live/[도메인주소]/fullchain.pem
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations, all simulated renewals succeeded:
  /etc/letsencrypt/live/[도메인주소]/fullchain.pem (success)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# 인증서 갱신 crontab
$ sudo su -
$ mkdir /root/script
$ vim /root/script/letsencrypt.sh
#!/bin/sh
certbot renew
:wq

$ crontab -e
01 00 */80 * * /root/script/letsencrypt.sh # 80일 마다 갱신

```
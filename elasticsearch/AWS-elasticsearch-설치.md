# 엘라스틱 설치

참고: 
- https://www.elastic.co/kr/downloads/elasticsearch 엘라스틱 다운로드 주소

## 0. vim 설치하기

> vim 은 Editor, properties 파일 수정을 위해 

```bash
$ sudo yum install vim-enhanced
..
$ sudo yum list installed | grep vim
...
```

## 1. Open JDK(java 1.8) 설치하기

참고: https://openjdk.java.net/install/

```bash
# 자바 패키지 검색
$ sudo yum search java-1.8 
==================================================== Name Matched: java-1.8 =====================================================
java-1.8.0-openjdk.x86_64 : OpenJDK Runtime Environment 8
java-1.8.0-openjdk.x86_64 : OpenJDK Runtime Environment 8
java-1.8.0-openjdk-src.x86_64 : OpenJDK Source Bundle 8
java-1.8.0-openjdk-demo.x86_64 : OpenJDK Demos 8
java-1.8.0-openjdk-devel.x86_64 : OpenJDK Development Environment 8
java-1.8.0-openjdk-javadoc.noarch : OpenJDK 8 API documentation
java-1.8.0-openjdk-headless.x86_64 : OpenJDK Headless Runtime Environment 8
java-1.8.0-openjdk-headless.x86_64 : OpenJDK Headless Runtime Environment 8
java-1.8.0-openjdk-javadoc-zip.noarch : OpenJDK 8 API documentation compressed in single archive
java-1.8.0-openjdk-accessibility.x86_64 : OpenJDK 8 accessibility connector

# 자바 런타임 버전 
$ sudo yum -y install java-1.8.0-openjdk

# or 자바 Develop kit 버전
# sudo yum -y install java-1.8.0-openjdk-devel
```

## 2. Download elasticsearch

> wget은 웹 파일 다운로드 어플리케이션

```bash
# 설치될 폴더로 이동
$ cd /usr/local/

# 만약 wget이 없다면...
$ sudo yum -y install wget
...

$ sudo wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.1.1-linux-x86_64.tar.gz
...

$ sudo tar -xzf elasticsearch-7.1.1-linux-x86_64.tar.gz
...

$ sudo chown -R ec2-user:ec2-user elasticsearch-7.1.1
...

$ cd elasticsearch-7.1.1

```

## 3. elasticsearch 설정

elasticsearch.yml:
```bash
...

cluster.name: kjy-cluster

...

network.host: 0.0.0.0

```

## 4. elasticsearch 실행
```bash
$ ./bin/elasticsearch

```

## :bomb: troubleshooting
### 1. Elasticsearch 설치 후 production mode로 실행시 bootstrap checks failed 에러 해결

참고 : https://github.com/higee/elastic/wiki/Elastic-Stack-%EC%84%A4%EC%B9%98-%EB%B0%8F-%ED%99%98%EA%B2%BD-%EC%84%A4%EC%A0%95.

> develop mode에서는 잘 동작하는 것을 확인하였다. 당연 로컬에서는.. 원격에 있는 PC 에 설치를 하여 URL을 불러 사용 하기 때문에 
  elasticsearch.yml 파일의 `network.host` 설정에 _global_로 변경 하고 실행 하는 순간 아래 같은 오류 발생 (Production mode)

```
ERROR: bootstrap checks failed
max file descriptors [4096] for elasticsearch process likely too low, increase to at least [65536]
max number of threads [1024] for user [space_home] likely too low, increase to at least [2048]
```

**에러관련 문서**
-  https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html
-  https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html


    1. max file descriptors 늘려주기
        - Mac OS 및 Linux만 해당 (Windows는 불필요)
        - Elasticsearch를 구동중인 사용자의 open files descriptors를 65536까지 올려야 함
        - RPM and Debian 패키지의 경우 default로 65536으로 설정되어 있으므로 이 설정이 불필요하다
        - 방법
            - 작업 전 확인 : `$ ulimit -a`
            - limits.conf 편집: 
            ```bash
            $ sudo vim /etc/security/limits.conf
            
            /etc/security/limits.conf:
            
            *        hard    nofile           65536
            *        soft    nofile           65536
            
            ```
            - 재접속 후 확인 : `$ ulimit -a`

    2. virtual memory areas 늘리기
        - Elasticsearch는 mmapfs 디렉토리에 index를 저장한다 (default 설정)
        - mmap counts에 대한 운영체제의 limit이 default로는 낮게 되어 있어서 높혀주지 않으면 out of memory 발생
        - 방법
            - 임시(재접속시 해제)
                - 작업 전 확인 : $ sudo sysctl -a | grep vm.max_map_count => 65530 (/proc/sys/vm/max_map_count)
                - 늘리기 : sudo sysctl -w vm.max_map_count=262144
                - 작업 후 확인 : $ sudo sysctl -a | grep vm.max_map_count => 262144
            
            - 영구적(재접속 후에도 효과 지속)
                - sysctl.conf 편집 :
                ```bash
                $ sudo vim /etc/sysctl.conf
                
                /etc/sysctl.conf:
                
                vm.max_map_count=262144
                ...
                
                ```
                - 재시작 : `$ sudo reboot`
                - 
                
                

 
 


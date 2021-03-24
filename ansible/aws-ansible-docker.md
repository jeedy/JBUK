# Ansible controller and Docker 셋팅 on AWS with centos7
tags: dev, ansible, local, docker, aws

개발자 환경을 구성하기 위한 셋팅, ansible로 docker instance 올려서 Local Host 내에 각종  instance들을 올리고 서로간에 통신을 할수 있는 network 구성을 해주는 방법이다.

> Redhat 은 설치 불가, docker 설치하려면 subscription manage 가입되어 있어야한다.

## 서비스 구성
1 lv (centos7) | 2 lv | 3 lv
|:--|:--|:--|
| Host(Controller) | ansible | |
| | docker | elastaicsearch-1 |
| | | elastaicsearch-2 |
| | | elastaicsearch-3 |
| | | kibana |
| | | prometheus |
| | | grafana |

## Workflow

### 0) `sudo sysctl -w vm.max_map_count=262144` on Contoller
Elasicsearch를 올리기 위한 설정. `vm.max_map_count` 값이 `65530` 으로 되어있다면 `262144` 값으로 수정하자, 만약 수정하지 않으면 ES는 정상적으로 올라가지 못하고 계속 재시작을 시도한다.

```bash
# vm.max_map_count 값 확인
$ cat /proc/sys/vm/max_map_count
65530

$ sudo sysctl -w vm.max_map_count=262144
# 영구적 설정
# /etc/sysctl.conf 파일안에 `vm.map_max_count=262144` 값 셋팅
```

### 1) `sudo yum update` on Controller
yum 업데이트. aws instance를 생성하면 가장 먼저 해줘야함.

```bash
$ sudo yum update -y
```

### 2) install git client on Controller
생략 가능하지만 ansible playbook을 git에서 다운받지 복사해서 가져오는 일은 없다.

```bash
$ sudo yum install git -y
```

### 3) install ansible on Controller
Ansible 설치. 
https://docs.ansible.com/ansible/2.9/installation_guide/intro_installation.html#installing-ansible-on-rhel-centos-or-fedora

```bash 
$ sudo yum install -y epel-release
# ansible 2.9 버전 확인을 위해 -y 뺏음
$ sudo yum install ansible
```

### 4) install python pip on Controller
`pip`는 python 에서 사용하는 패키지를 관리하기 쉽게 도와주는 installer 이고 centos7 에 기본으로 python2 가 깔려있으나 `pip`는 깔려있지 않다.   
`pip`를 설치하고 추가 패키지도 install 한다.

```bash
# pip 설치
$ sudo yum -y install python-pip

# get-pip 패키지 설치 (wheel, sudo 계정사용을 위한)
$ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
$ python get-pip.py

# python-netaddr 패키지 설치 (옵션, playbook 에서 사용할 수도 있다.)
$ sudo yum install python-netaddr -y

# python 에서 docker를 사용하기위한 패키지인듯
$ sudo pip install docker-py
```

### 5) install Docker engine on Controller
centos 내에 docker를 올리기 위해선 까다로운 설치과정이 필요.
> 참고로 redhat은 유료 서비스 가입해야 설치할 수 있다.

```bash
$ sudo yum install -y yum-utils
$ sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
$ sudo yum install docker-ce docker-ce-cli containerd.io
$ sudo systemctl start docker
$ sudo systemctl enable docker
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```

### 6) git Clone example-playbook source on Controller
운영시 playbook은 가능한 git으로 올려서 다운받아 실행하는 방식으로 진행한다.

```bash
$ git clone https://jeedy@github.com/ansible/example-playbook.git

$ cd example-playbook
```

### 7) Run Ansible playbook on Controller
```bash
# centos 사용자를 docker 그룹 사용자로 변경한다.(기존에 centos 그룹으로 되어있음) 
$ newgrp docker

$ cd ~/cd example-playbook
$ ansible-playbook playbook.yml

# 인스턴스 확인
$ docker ps -a
```

### extra) AWS CLI 2 설치 및 s3 폴더 복사
액세스 키ID 생성방법 참조: https://twofootdog.tistory.com/36

```bash
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ yum install unzip -y
$ unzip awscliv2.zip
$ aws --version
$ aws configure
AWS Access Key ID [None]: [엑세스 키 ID]
AWS Secret Access Key [None]: [비밀 엑세스 키]
Default region name [None]: ap-northeast-2
Default output format [None]: [공백 enter]

# aws s3 ls   	# 내 계정의 s3 버킷 리스트
# aws s3 ls [버킷명] # 내 버킷 내 파일 리스트

# 업로드
# aws s3 cp [source파일명] s3://[destination버킷명]/[destination파일명]

# 다운로드 
# aws s3 cp s3://[source버킷명]/[source파일명] [destination파일명] 

```
# Ansible(엔서블)
tags: ansible, elasticsearch, docker, kibana, ssh, amazon linux, aws

결국 ssh 연결을 통해 셀 명령어를 사용하는 것이기 때문에 node 운영체제의 선택은 중요한 요소, 운영체제에 따라 필요할 경우 버전에 따른 playbook 작성을 해야한다.

## 용어
1. controller: ansible이 인스톨된 서버를 controller 서버라고 한다.
2. node or 호스트(host): controller 서버에서 컨트롤하는 서버를 node라고 한다.

## ansible 옵션
- `-b` : root 권한으로 실행
- `-m` : 사용할 모듈, 주로 `command`, `ping` 를 사용한다. 
    - `-m command`(디폴트) : command 모듈을 사용해 임의의 커맨드를 실행<br/>
    예시) `ansible all -m command -a uptime`, `ansible all -a uptime`
    - `-m ping` : ping 모듈, node 서버가 정상인지 확인<br/>
    예시) `ansible all -m ping`
- `ansible localhost -m setup` : 로컬 변수 확인

## :bomb: troubleshooting
### 1. Amazon linux(AWS) 에서 ansible 설치시 유의사항
참고: https://aws.amazon.com/ko/blogs/infrastructure-and-automation/automate-ansible-playbook-deployment-amazon-ec2-github/

블로그에 나오는 내용으로는 설치가 불가능하다. 위 aws 매뉴얼을 참고해서 설치를 진행했다. 
```sh
# yum repository 추가
$ sudo amazon-linux-extras install epel

# asible 설치
$ sudo yum install ansible -y

# git 설치(option)
$ sudo yum install git -y
```

### 2. Controller 에서 node 서버 접근하려면 ssh 접속이 가능해야한다.
```sh
# 키생성
[ec2-user@controller-ip]$ ssh-keygen

# 키복사 to node 서버 (*Permission denied (publickey,gssapi-keyex,gssapi-with-mic) 발생할 수 있음)
[ec2-user@controller-ip]$ ssh-copy-id ec2-user@node1-ip
```
> ssh id 복사 과정에서 Permission denied (publickey,gssapi-keyex,gssapi-with-mic).  에러 날 수 있음.



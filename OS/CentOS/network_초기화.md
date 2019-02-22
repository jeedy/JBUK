# [CentOS] Network 초기화

네트워크 설정 정보가 꼬일 때, 이전 설정 정보를 모두 지우고 다시 설정하는 방법이 있다.

### 아래 파일들을 삭제

1. /etc/sysconfig/networking/profiles/default/*       # 모든 파일
1. /etc/sysconfig/networking/devices/*                # 모든 파일
1. /etc/sysconfig/network-scripts/ifcfg-eth*          # 경로에서 ifcfg-eth로 시작하는 파일을 삭제
1. /etc/udev/rules.d/70-persistent-net.rules          # 네트워크 카드 정보


### 재 부팅
```bash
$ reboot
```

### 재 부팅한 후에는 /etc/udev/rules.d/70-persistent-net.rules 파일을 열어보면 네트워크 카드가 보인다.

```bash
 $ cat /etc/udev/rules.d/70-persistent-net.rules
 ```

### 네트워크 카드 정보가 추가되어 있는 것이 확인된다.

```bash
$vi /etc/sysconfig/network-scripts/ifcfg-eth0

DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.0.100
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
BOOTPROTO=static
DNS1=166.126.63.1
DNS2=168.126.63.2
USERCTL=no
```

### 네트워크 서비스를 재시작하면 완료.
```bash
$ service network restart
```


Thx Kyg

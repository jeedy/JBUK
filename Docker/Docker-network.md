# 도커 네트워크(network)

## 도커 네트워크 구조

컨테이너 내부에 ifconfig 입력하면 도커 엔진은 컨테이너에 내부 IP를 순차적으로 할당하며, 이 IP는 컨테이너를 재 시작할 때마다 변경 될 수 있습니다. 이 내부 IP는 도커가 설치된 호스트, 즉 내부 망에서만 쓸 수 있는 IP이므로 외부와 연결될 필요가 있습니다. 이 과정은 컨테이너를 시작할 때마다 호스트에 veth... 라는 네트워크 인터페이스를 생성함으로써 이뤄집니다.

```bash
root@9f5b8e00bf24:/$ ifconfig
eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:03
          inet addr:172.17.0.3  Bcast:172.17.255.255  Mask:255.255.0.0

          ...

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
```

## 브리지(bridge)

브리지 네트워크는 컨테이너를 생성할때 자동으로 연결되는 docker0 브리지를 활용하도록 설정돼 있습니다.
이 네트워크는 172.17.0.x IP 대역을 컨테이너에 순차적으로 할당합니다. `$ docker network inspect bridge` 명령어를 이용하면 네트워크의 자세한 정보를 살펴 볼 수 있습니다.

### Custom 브리지 생성 그리고 사용

브리지 타입의 네트워크를 생성하면 도커는 IP 대역을 차례대로 할당합니다. 다음 예시에서는 172.18 대역의 내부IP가 할당됐습니다.

```bash
$ docker network create --driver bridge

$ docker run -it --name mynetwork_container \
--net mybridge \
ubuntu:14.04

$ root@mynetwork_container:/$ ifconfig
eth0    Link encap:Ethernet     HWaddr 02:42:ac:12:00:12
        inet addr: 172.18.0.2   Bcast:0.0.0.0   Mask:255.255.0.0
...
```

네트워크의 서브넷, 게이트웨이, IP 할당 범위 등을 임의의로 설정하려면 `--subnet, --ip-range, --gateway`(--subnet과 --ip-range는 같은 대역대이어야 한다.)

```bash
$ docker network create --driver=bridge \
--subnet=172.72.0.0/16 \
--ip-range=172.72.0.0/24 \
--gateway=172.72.0.1 \
my_custom_network
```

## 호스트(host)

네트워크를 호스트로 설정하면 호스트의 네트워크 환경을 그대로 쓸 수 있습니다.

```bash
$ docker run -it --name network_host \
--net host \
ubuntu:14.04
```

컨테이너 내부에서 네트워크 환경을 확인하면 호스트와 같은 것을 알 수 있습니다. 호스트 머신에서 설정한 호스트 이름도 컨테이너가 물려받기 때문에 컨테이너의 호스트 이름도 무작위 16진수가 아닌 도커 엔진이 설치된 호스트 머신의 호스트 이름으로 설정됩니다.
**컨테이너의 네트워크를 호스트 모드로 설정하면 컨테이너 내부의 애플리케이션을 별도의 포트 포워딩 없이 바로 서비스 할 수 있습니다.**

## 논(none)
none은 아무런 네트워크를 사용하지 않는 것을 뜻합니다.
--net 옵션으로 none을 설정한 컨테이너 내부에서 네트워크 인터페이스를 확인(ifconfig)하면 로컬호스트를 나타내는 lo외에는 존재지 않은 것을 알 수 있습니다.
```bash
$ docker run -it --name network_none \
--net none \
ubuntu:14.04
```

## 컨테이너(container)

`--net container:[다른 컨테이너의 ID]` 옵션은 다른 컨테이너의 네트워크 환경을 공유할 수 있습니다.
공유되는 속성은 내부 IP, 네트워크 인터페이스의 맥(MAC) 주소 등입니다. --net 옵션의 값으로 container:[다른 컨테이너의 ID]와 같이 입력합니다.
```bash
$ docker run -it -d --name network_container_1 ubuntu:14.04
2fc4...

$ docker run -it -d --name network_container_2 \
--net container:network_container_1 \
ubuntu:14.04

eb1521e...
```

> -i, -t, -d옵션을 함께 사용하면 컨테이너 내부엣 셸을 실행하지만 내부도 들어가지 않으며 컨테이너도 종료되지 않는다.

다른 컨테이너의 네트워크 환경을 공유하면 내부 IP를 새로 할당받지 않으며 호스트에 veth로 시작하는 가상 네트워크 인터페이스도 생성되지 않는다. network_container_2 컨테이너의 네트워크와 관련된 사항은 전부 network_container_1과 같게 설정됩니다.

```bash
$ docker exec network_container_1 ifconfig
eth0    Link encap:Ethernet     HWaddr 02:42:ac:11:00:03
        inet addr:172.17.03     Bcast:0.0.0.0   Mask:255.255.0.0
        inet6   addr: fe80:42:acff:fe11:3/64    Scope:Link
...

$ docker exec network_container_2 ifconfig
HWaddr 02:42:ac:11:00:03
        inet addr:172.17.03     Bcast:0.0.0.0   Mask:255.255.0.0
        inet6   addr: fe80:42:acff:fe11:3/64    Scope:Link
...
```

두 컨테이너의 정보가 완전히 같다.
~ 위 방법으로 다수의 컨테이너를 띄우면 외부에서 접근할때 어떻게 로드밸런싱이 되는가?

## 오버레이(overlay)

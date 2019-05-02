# 네트워크 계층별 프로토콜(Layer Protocol)

참고
- https://needjarvis.tistory.com/158?category=619248

## 레이어별 프로토콜 개념

네트워크 프로토콜을 설명하기 위해서는 우선 OSI 7 Layer와 TCP/IP의 4 Layer를 이해하고 있어야 한다.
특히 OSI 7 Layer를 이해하고 있으면, 해당 위치에 어느 프로토콜이 존재하는 것만으로 해당 프로토콜의 역할이 쉽게 이해가 되기 때문이고,
각각의 계층별로 데이터를 전송하는 방식이 다르기 때문이기도 하다.

OSI(Open Systems Interconnction) 7 Layer는 ISO(국제표준기구)에서 만든 네트워크를 7계층으로 만든 모델이고, 프로토콜(Protocol, 통신규약)은
상호간의 접속이나 전달방식, 통신방식, 주고받을 자료의 형식, 오류 검출 방식, 코드 변환방식, 전송속도 등에 대하여 이미 정해진 약속이기 때문에
레이어별 프로토콜은 한마디로 OSI 7 계층의 계층간에 존재하는 네트워크 통신을 위한 규약을 뜻한다.

## OSI 7 Layer별 프로토콜 구조

![OSI 7 Layer별 프로토콜 구조](./images/osi-7layer-protocol.jpg)

## OSI와 TCP/IP 프로토콜의 구조

![OSI TCP/IP 프로토콜 구조](./images/osi-7layer-tcpip-4layer.jpg)

- TCP/IP는 OSI 7 Layer를 4개로 단순화 하여 구현
- TCP/IP는 3(Session layer),4(Transport layer)계층을 중심으로 한 통신 프로토콜의 계층 집합

## OSI 7 Layer별 주요 프로토콜 설명

### 1. 응용 계층(Application Layer)

#### HTTP(HyperText Trasfer Protocol)
- WWW(Wrold Wide Web) 상에서 정보를 주고 받을 수 있는 프로토콜
- 주로 HTML 문서를 주고 받는 데에 쓰이고, TCP와 UDP를 사용하며, 80번 포트 사용

#### SMTP(Simple Mail Trasfer Protocol)
- 인터넷에서 이메일을 보내고 받기 위해 이용되는 프로토콜, TCP 포트번호 25번 사용

#### FTP(File Transfer Protocol)
- 컴퓨터 간 파일을 전송하는데 사용되는 프로토콜(데이터 전달: 20번 포트, 제어정보 전달: 21번 포트)

#### TELNET
- 인터넷이나 로컬 영역 네트워크 연결에 쓰이는 네트워크 프로토콜, IETF STD 8로 표준화
- 보안문제로 사용이 감소하고 있으며, 원격제어를 위해 SSH로 대체

### 2. 표현 계층(Presentation Layer)

#### SSL(Secure Socket Layer)
- 네트워크 레이어의 암호화 방식, HTTP 뿐만 아니라, NNTP, FTP 등에도 사용
- 인증, 암호화, 무결성 보장하는 프로토콜

#### ASCII(Amerian Standard Code for Information Interchange)
- 문자를 사용하는 많은 장치에서 사용되며, 대부분의 문자 인코딩이 아스키에 기반
- 7비트 인코딩, 33개의 출력 불가능한 제어 문자들과 공백을 비롯한 95개의 출력 가능한 문자

### 3. 세션 계층(Session Layer)

#### NetBIOS
- 네트워크의 기본적인 입출력을 정의한 규약

#### RPC(Remote Procedure Call)
- Windows 운영 체제에서 사용하는 원격프로시저 호출 프로토콜

#### WinSock(Windows Socket)
- 유닉스 등에서 TCP/IP 통신시 사용하는 Socket을 Windows에서 그대로 구현한 것

### 4. 전송 계층(Transport Layer)

#### TCP(Transmission Control Protocol)
- 전송 제어 프로토콜, 네트워크의 정보전달을 통제하는 프로토콜
- 데이터의 전달을 보증하고 보낸 순서대로 받게 해줌
- 3 Way Handshaking와 4 Way Handshaking 등을 활용한 신뢰성 있는 전송이 가능

#### UDP(User Datagram Protocol)
- 비연결성이고 신뢰성이 없으며, 순서화되지 않은 Datagram 서비스 제공
- 신뢰성이 낮은 프로그램에 적합 (*실시간 동영상 스트리밍)

### 5. 네트워크 계층(Network Layer)

#### IP(Internet Protocol)
- 패킷 교환 네트워크에서 정보를 주고 받는데 사용하는 정보 위주의 규약
- 호스트의 주소지정과 패킷 분할 및 조립 기능을 담당

#### ICMP(Internet Control Message Protocol)
- TCP/IP 에서 IP 패킷을 처리할 때 발생되는 문제(오류 보고)를 알림
- 진단 등과 같이 IP계층에서 필요한 기타 기능들을 수행하기 위해 사용되는 프로토콜

#### IGMP(Internet Group Management Protocol)
- IP 멀티캐스트를 실현하기 위한 통신 프로토콜
- PC가 멀티 캐스트로 통신할 수 있다는 것을 라우터에 통지하는 규약

> 멀티 캐스트(multicast) 란 한 번의 송신으로 메시지나 정보를 목표한 여러 컴퓨터에 동시에 전송하는 것을 말한다. (참고: https://ko.wikipedia.org/wiki/%EB%A9%80%ED%8B%B0%EC%BA%90%EC%8A%A4%ED%8A%B8)

### 6. 데이터 링크 계층(Data Link Layer)

#### Ethernet
- 비연결성(connectionless)모드, 전송속도 10Mbps 이상, LAN 구현 방식을 말함

#### HDLC(High-Level Data-Link Control)
- 고속 데이터 전송에 적합하고, 비트 전송을 기본으로 하는 범용의 데이터 링크 전송 제어 절차

#### P2P(Point-to-Point Protocol)
- 전화선 같이 양단간 비동기 직렬 링크를 사용하는 두 컴퓨터간의 통신을 지원하는 프로토콜

### 7. 물리 계층(Physical Layer)

#### RS-232
- 보통 15m이하 단거리에서 38400bps 까지 전송을 위한 직렬 인터페이스

#### X.25 / X.21
- X.25는 패킷교환망, X.21은 회선교환망에 대한 엑세스 표준
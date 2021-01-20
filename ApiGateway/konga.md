# Konga - Kong Admin GUI Manager
tags: API, gateway

## https://github.com/pantsel/konga

## 개요

## service 등록 방법
![service 등록](./images/Konga-add-service.png)

> 용어설명<br>
    - upstream server : 목적지 서버


- Protocol: upstream server 프로토콜 입력
- Host: upstream server 도메인주소
- Port: upstream server 사용 포트
- Path: upstream server path (기본값으로 '/')

## Route 등록 방법
![route 등록](./images/Konga-add-route.png)

- Paths: 1 path 값 (예제: /acc)
- Method: Route 가능하게 할 method 설정
- Strip Path : yes로 해야 /acc 빼고 upstream server로 호출


## Authorization(Basic-Auth) 셋팅 방법
### 1. Consumer 등록
1. Dashboard > CONSUMERS 메뉴 클릭 > Consumer 등록 버튼 클릭
1. username 입력 후 sumbmit 버튼 클릭

![Consumer 등록](./images/Konga-add-consumer.png)

### 2. Consumer Basic Auth 키 등록
- Consumer 상세페이지 > Credentials 탭 클릭 > Basic Auth 메뉴 클릭 > CREATE CREDENTIALS 버튼 클릭
- username, password(**password 반드시 기억해놓자**) 입력 후 submit 버튼 클릭

![Consumer Basic Auth 키등록](./images/Konga-add-basicauth-consumer.png)

### 3. Route 상세페이지 > Plugins 메뉴 > ADD PLUGIN 버튼 > Authentication > Basic Auth ADD PLUGIN

![Route Basic Auth plugin 연결](./images/Konga-add-basicauth-route.png)

### 4. Route 연결 확인
![Route 연결 확인](./images/Konga-list-basicauth-route.png)


### 5. 접속테스트
![접속 테스트](./images/Konga-test-basicauth-postman.png)


## ACL(Access Control List, 접근 제어 목록) group 셋팅 방법
Router(또는 Service)에 Basic-Auth 만 등록하게 되면 Basic-Auth가 발급된 Consumer는 모든 API 사용이 가능하다. 각 Consumer 마다 사용할 수 있는 API를 control 하려면 ACL Plugin 으로 관리하면 된다.

### 1. Route 상세페이지 > Plugins 메뉴 > ADD PLUGIN 버튼 > Security > Acl ADD PLUGIN
- allow 영역에 `Acl 그룹명`(그냥 텍스트)을 입력하고 엔터
- 여러 Acl 그룹을 등록할 수 있다.

![Route Acl plugin 연결](./images/Konga-add-acl-route.png)

### 2. Consumer에 Acl group 등록하기
- 위 route에서 Acl plugin에 등록된 `Acl 그룹명`을 입력한다.
![consumer Acl group에 등록](./images/Konga-add-aclgroups-consumer.png)

### 3. Acl group에 등록된 Consumer만 해당 Router를 이용 가능해진다.


## !중요! cors plugin 셋팅
cors plugin을 설치하지 않고 `curl` 이나 `postman` 에서 **OPTIONS** method로 호출하면 response status 가 `200` 으로 주지만 브라우저 호출하면 `401`을 response 한다.
그렇기 때문에 반드시 plugin을 셋팅해야 한다.

> CORS, Preflight, 인증 처리 란?<br>
브라우저에서 A-server 로 Ajax 통신을 하려할때 METHOD: OPTIONS 으로 preflight를 호출해 Request를 던저도 될지 A-server에게 확인 절차를 거친다.

### 1. Route > Methods 항목에 OPTIONS 추가

반드시 들어가 있어야 한다. 들어가 있지 않으면 cors error 발생

![라우트에 OPTIONS 메소드 등록](./images/Konga-cors-route.png)

### 2. Route(또는 service) > Plugins > Security > Cors ADD plugin

디폴트 값이 안들어가 있어도 response 200 떨어진다. (이 플러그인을 사용하지 않으면 Respose 401 error 떨어짐)

![라우트에 cors plugin 등록한다.](./images/Konga-cors-route-corsplugin.png)

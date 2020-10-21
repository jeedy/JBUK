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

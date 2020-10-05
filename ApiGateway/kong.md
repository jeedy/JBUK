# Kong - API Gateway 
tags: API, gateway

## https://konghq.com/

## 느낌점
spring cloud gateway와 다른점은 직접 소스로 구현을 할 필요가 없는 솔류션으로 보인다.
GUI 어드민 페이지도 제공해 페이지에서 직접 컨트롤하고 지표도 뽑아 볼수있다. 

개발자가 직접 설치하는 것이 아닌 인프라 영역에 가까운 솔류션, 엄블렐라(API umbrella)도 마찬가지이다. 


## 참고자료
1. https://medium.com/@keendev/kong%EC%9C%BC%EB%A1%9C-%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98-1-824f5ae4606b (2016년글이지만 사용방법과 kong의 설치 및 구동방식을 대략적으로 이해 가능하다)

1. https://study-develop.tistory.com/39 (kong & konga 설치하기)

1. https://ibks-platform.tistory.com/378 (kong 설치)
1. https://ibks-platform.tistory.com/379 (konga 설치)

## 개요
엔진은 무료로 사용가능한것 같다. 그러나 gui는 유료모델인것 같다. 그러나 [konga](https://github.com/pantsel/konga) 라는 오픈소스로 gui 를 사용할 수 있다.

2018년도에 1.0버전 릴리스하게 된다. 주 기반언어는 Lua language.

client로는 T telekom(도이치 텔레콤, 독일), 익스피디아, 제너럴 일렉트릭, 시스코, AXA 프랑스의 보험 금융 그룹, 삼성, 파파존스, 나스닥 등등..

## kong enterprise vs community
https://konghq.com/subscriptions/

### 공통제공
- 모든 아키텍처 (모놀리스, 마이크로 서비스, 서비스 메시 등)에서 작동하는 경량 API 게이트웨이 (*Lightweight API gateway that works with any architecture (monolith, microservices, service mesh and more))
- Kubernetes 수신 컨트롤러 (*Kubernetes Ingress Controller)
- 기본 트래픽 제어 플러그인 (*Basic traffic control plugins)
- gRPC 지원 (*gRPC support)
- 기본 인증 (HMAC, JWT 키 인증, 제한된 OAuth 2.0 포함) (*Basic authentication (includes HMAC, JWT Key Auth, limited OAuth 2.0))
- 서드파티 분석 (*Third-party analytics)
- 게이트웨이 및 Kubernetes의 선언적 구성 (CI / CD 파이프 라인에 Kong 구성 파일을 추가 할 수 있음) (*Declarative configuration of gateway and Kubernetes (enables adding Kong config file to your CI/CD pipeline))
- GitOps 용 Git 동기화 (*Git sync for GitOps)

### Enterprise Only
- 고급 트래픽 제어 플러그인 (고 가용성 속도 제한, 고급 서비스 라우팅, 분산 캐싱)
- GraphQL 및 Kafka 지원
- Kong 클러스터, 플러그인, API 및 소비자를 관리하기위한 Admin GUI 및 작업 공간 
- 자율 모니터링 및 이상 감지 (Kong Immunity)
- 클러스터 상태 모니터링 (Kong Vitals)
- 감사 로그
- 비주얼 서비스 맵
- 고급 인증 (전체 OAuth 2.0, OpenID Connect, Vault, 상호 TLS 및 향상된 암호화 포함)
- 클러스터 상태 모니터링 (Kong Vitals)
- Kong Studio 통합을 통한 엔드 투 엔드 API 사양 및 디자인
- 24x7x365 전문가 지원
- 기타 등등...


#### postgresql URIs
```
postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
```
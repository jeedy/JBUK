# API 게이트 웨이

## 목차
1. [kong](/ApiGateway/kong.md)
1. [umbrella](/ApiGateway/umbrella.md)
1. [tyk](/ApiGateway/tyk.md/)
1. [zuul](/Java/Spring/Zuul/README.md)
1. [spring cloud gateway](/Java/Spring/cloud-gateway/README.md)

### API gateway 비교
http://uengine.org/TheOpenCloudEngine.github.io-blog/api-gateway/2017/07/24/apt-gw-1.html

### 1. KONG
mashape라는 회사에서 개발 및 사용하는 솔루션

특징
- NGINX + Cassandra 조합으로 lua Script로 프로그래밍
- MIT 라이센스
- Docker 지원
- Plug-in 형태의 기능 지원

### 2. API Umbrella
미국 정부(일개?)에서 사용하다고 되어 있으며, 따로 개발 및 관리 주체가 없는 것으로 보임

특징
- NGINX + node.js + varnish + MongoDB + Redis + Elastic Search 조합이며, Ruby on - Rails로 개발한 포털 제공
- MIT 라이센스


### 3. tyk.io
다른 서비스와 달리 구글(의 3명 엔지니어)가 개발한 최신 프로그래밍 언어 golang으로 메인 Functionality가 개발 되었다는 것이 굉장히 매력적이다. 거의 매일 업데이트가 되고 있으며, 사용자 요청을 적극적으로 반영하기 때문에 향후 발전 가능성이 굉장히 높다.

특징
- MongoDB + Redis + NGINX 조합으로 golang으로 프로그래밍
- MPL v2.0 라이센스
- API Documentation을 위한 Swagger 지원
- 사용자 및 API Key 인증/권한 관리가 매우 좋음
- Docker 지원

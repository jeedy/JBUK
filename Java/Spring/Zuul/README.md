# API Gateway - spring cloud zuul
tags: API, gateway, spring, cloud, zuul, MSA, Microservice Architecture, Netflix

## 참고 자료
 - https://woowabros.github.io/r&d/2017/06/13/apigateway.html (배민 API GATEWAY - spring cloud zuul 기본개념 및 적용기)
 - https://supawer0728.github.io/2018/03/11/Spring-Cloud-Zuul/ (zuul 구현방법)
 - https://coding-start.tistory.com/123 (zuul 구현방법)
 
 - https://www.it-swarm.dev/ko/spring-boot/zuul%EC%9D%84-%EC%9D%B8%EC%A6%9D-%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4%EB%A1%9C-%EC%82%AC%EC%9A%A9/824448727/(zuul 인증 게이트웨이 구현)
 - https://www.baeldung.com/spring-security-zuul-oauth-jwt
 - https://github.com/shuaicj/zuul-auth-example
 - https://sarc.io/index.php/cloud/1747-zuul(초간단하게 zuul  만들어보자, filter부분은 아래 참조)
 - https://daddyprogrammer.org/post/4401/spring-cloud-msa-gateway-routing-by-netflix-zuul/ (간단하게 zuul 라우팅 &filter)
 - https://velog.io/@city7310/%EB%B0%B1%EC%97%94%EB%93%9C%EA%B0%80-%EC%9D%B4%EC%A0%95%EB%8F%84%EB%8A%94-%ED%95%B4%EC%A4%98%EC%95%BC-%ED%95%A8-5.-%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%9D%B8%EC%A6%9D-%EB%B0%A9%EC%8B%9D-%EA%B2%B0%EC%A0%95 (Authorization 해더에 대한 내용)

 - https://medium.com/@yesesyo/%EA%B0%80%EB%B3%8D%EA%B2%8C-%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B5%AC%EC%B6%95%ED%95%B4%EB%B3%B4%EA%B8%B0-3-e7e638776109 (zuul 구현방법, 허용한 IP 대역대만 필터링)

 - https://velog.io/@tlatldms/%EC%84%9C%EB%B2%84%EA%B0%9C%EB%B0%9C%EC%BA%A0%ED%94%84-MSA-%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98-API-Gateway-%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC-%EA%B2%B0%EC%A0%95 (spring-cloud-gateway 내용)

- https://velog.io/@tlatldms/%EC%84%9C%EB%B2%84%EA%B0%9C%EB%B0%9C%EC%BA%A0%ED%94%84-JWT-%EC%9D%B8%EC%A6%9D-%EC%84%9C%EB%B2%84%EC%99%80-Spring-Cloud-Gateway-Spring-Security-%EC%A0%81%EC%9A%A9%ED%95%B4%EC%84%9C-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0-0%ED%8E%B8 (spring cloud gateway 와 security jwt 방법)

- https://spring.io/guides/gs/gateway/ (spring cloud gateway 가이드)
- https://springboot.cloud/26 (spring cloud gateway에 대한 설명)

- https://kingbbode.tistory.com/47 (zuul vs spring cloud gateway, 왜 spring cloud gateway를 새로 만들었나?)

- https://medium.com/@niral22/spring-cloud-gateway-tutorial-5311ddd59816(spring cloud gateway tutorial)

- https://cloud.spring.io/spring-cloud-gateway/reference/html/#gateway-how-it-works (spring cloud gateway 공식 문서)

## vs NetFlix
- gateway 로서의 역활
    - netflix 는 Zuul
    - spring 은 cloud-gateway
- 로드밸런싱
    - netflix는 riborn
    - spring은 cloud-discovery


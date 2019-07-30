# SpringBoot

## :bomb: troubleshooting
1. spring boot에서 기본 sessionid `session`을 `JSESSIONID`로 수정하는 방법

    `application.properties` 파일에 `server.servlet.session.cookie.name`에 `JSESSIONID`을 입력한다.
    
    application.properties:
    ```properties
    server.port = 80
    server.contextPath=/
    server.servlet.session.cookie.name=JSESSIONID
    
    ... 
    ``` 

2. Spring boot 에서 JSP 사용하기
    1) Spring-boot-start-web 에 포함된 tomcat은 JSP 엔진을 포함하지 않는다.  jasper 및 jstl 을 의존성에 포함시켜줘야 JSP파일 구동이 가능하다.
    
    pom.xml:    
    ```xml
    <dependency>
        <groupId>org.apache.tomcat.embed</groupId>
        <artifactId>tomcat-embed-jasper</artifactId>
        <scope>provided</scope>
    </dependency>
    
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>jstl</artifactId>
    </dependency>
    ```
    
    2) JSP파일은 Spring boot 기본 template 폴더 안에서 작동하지 않는다.
     
    http://docs.spring.io/spring-boot/docs/current/reference/html/boot-features-developing-web-applications.html#boot-features-jsp-limitations
        
    application.properties:
    ```properties
    spring.mvc.view.prefix=/WEB-INF/jsp/
    spring.mvc.view.suffix=.jsp
    ```
    
    3) 컨트롤러에 추가 해 준 뒤에 src/main/webapp/WEB-INF/jsp/index.jsp 를 만들어 넣으면 localhost/ 에 접속했을 때 index.jsp를 정상적으로 불러올 수 있다.
    indexController:
    ```java
    @RequestMapping("/")
        public String index(){
        return "index";
     }
    ```
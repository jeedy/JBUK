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
    
3. get method 방식으로 @PathVariable 값에 '.' 이 들어갈 경우 Error 406 에러와 서버에 "org.springframework.web.HttpMediaTypeNotAcceptableException: Could not find acceptable representation"와 같은 에러가 발생할 경우

WebMvcConfiguration 셋팅하는 소스에서 `configurer.favorPathExtension(false);` 값을 셋팅한다.
참고 URL
- https://stackoverflow.com/questions/22329393/springmvc-inconsistent-mapping-behavior-depending-on-url-extension
- https://stackoverflow.com/questions/23578742/spring-does-not-ignore-file-extension
```java
@Configuration
public class WebMvcConfig extends WebMvcConfigurationSupport {
    @Override
    public RequestMappingHandlerMapping requestMappingHandlerMapping() {
        return new ApiVersionRequestMappingHandlerMapping("api/v");
    }
    
    @Override
    protected void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry
        .addResourceHandler("swagger-ui.html")
        .addResourceLocations("classpath:/META-INF/resources/");
        
        registry
        .addResourceHandler("/webjars/**")
        .addResourceLocations("classpath:/META-INF/resources/webjars/");
        
        super.addResourceHandlers(registry);
    }
    
    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/jsp/");
        resolver.setSuffix(".jsp");
        resolver.setViewClass(JstlView.class);
        registry.viewResolver(resolver);
    }

    /**
     * /api/v1/privia/memberinfo/hisnext@naver.com 과 같은 '.' 이 들어간 @PathVariable 값을 받기 위해선 아래 셋팅이 필요하다. 
     */
    @Override
    protected void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer.favorPathExtension(false);
    }
}
```

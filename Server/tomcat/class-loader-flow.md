# 톰켓 클래스 로드 순서

## Tomcat 4,5 버전 클래스 로드 순서 (7 버전은 아래)
참고 사이트 
- https://linuxism.ustd.ip.or.kr/611 (tomcat 클래스 로드 순서)


Tomcat 에서 ClassLoader 의 상하구조는 다음 그림과 같습니다.

```
              Bootstrap
                  |
               System
                  |
               Common
              /        \
          Catalina     Shared
                       /     \
                  Webapp1   Webapp2 ...
```

그런데 class 를 찾는 순서는 Tomcat version 에 따라 순서가 다르다는 것을 발견했습니다.

 

Tomcat 4.x Class 를 찾는 순서

/WEB-INF/classes of your web application
/WEB-INF/lib/*.jar of your web application
Bootstrap classes of your JVM
System class loader classses (described above)
$CATALINA_HOME/common/classes
$CATALINA_HOME/common/endorsed/*.jar
$CATALINA_HOME/common/lib/*.jar
$CATALINA_HOME/shared/classes
$CATALINA_HOME/shared/lib/*.jar
Tomcat 5.x Class 를 찾는 순서

Bootstrap classes of your JVM
System class loader classses (described above)
/WEB-INF/classes of your web application
/WEB-INF/lib/*.jar of your web application
$CATALINA_HOME/common/classes
$CATALINA_HOME/common/endorsed/*.jar
$CATALINA_HOME/common/lib/*.jar
$CATALINA_BASE/shared/classes
$CATALINA_BASE/shared/lib/*.jar
문제는 환경변수에 CLASSPATH 로 설정된 jar 와 context 의 WEB-INF/lib 밑의 jar 중에서 어떤 jar 를 먼저 찾는가 입니다.

CLASSPATH 에서 jar 를 읽어오는 ClassLoader 는 System class loader 입니다.

 

따라서 4.x 에서는 WEB-INF/lib 밑의 jar 가 CLASSPATH 로 설정된 jar 보다 먼저 읽히고

5.x 에서는 CLASSPATH 로 설정된 jar 가 WEB-INF/lib 밑의 jar 보다 먼저 읽힙니다.

 
## tomcat 7 이라면?

https://tomcat.apache.org/tomcat-7.0-doc/class-loader-howto.html



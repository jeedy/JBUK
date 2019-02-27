# Maven 변수를 선언하고 사용하는 다양한 방법

Maven-Spring 환경에서 아래와 같은 pom.xml의 project 변수들은 pom파일 내에서는 아래와 같이 사용 할 수 있습니다.

```
${java.version}
```

그러나 pom파일 뿐만 아니라 java나 프로퍼티 파일에서 써야 할 경우가 생깁니다. 특히 build timestamp같은 경우는 많은곳에서 사용합니다.

## maven pom.xml에서 변수 선언

pom.xml :
```xml
<properties>
    <!-- Generic properties -->
    <jdk-version>1.8</jdk-version>
    <deploy.path>deploy</deploy.path>
    <maven.test.skip>false</maven.test.skip>
    <deploy-path>deploy</deploy-path>

    <!-- Web -->
    <jsp.version>2.1</jsp.version>
    <jstl.version>1.2</jstl.version>
    <servlet.version>3.1.0</servlet.version>

    <!-- Spring -->
    <spring-framework.version>4.1.0.RELEASE</spring-framework.version>
    <!-- Logging -->
    <logback.version>1.1.2</logback.version>
    <slf4j.version>1.7.5</slf4j.version>

    <!-- Test -->
    <junit.version>4.11</junit.version>
    <mockito.version>1.9.5</mockito.version>

    <timestamp>${maven.build.timestamp}</timestamp>
    <maven.build.timestamp.format>yyyy-MM-dd HH:mm</maven.build.timestamp.format>
 </properties>
```


## Java에서 Properties를 이용해 Maven 변수 사용하기

메이븐 빌드시 `src/main/resources` 안에 *.properties 파일에 변수값을 치환해 자바에서 사용하는 방법이다.

pom.xml:
```xml
<resources>
   <resource>
      <directory>src/main/resources</directory>
      <filtering>true</filtering>
   </resource>
</resources>
```

이렇게 되면 resource내의 폴더 내 프로퍼티 파일에서 아래와 같이 변수를 쓸수가 있습니다. 그러면 프로퍼티 파일에서 xml설정등을 이용해서 자바에서 변수를 쓸수가 있습니다.

src/main/resources/xxxx.properties

```properties
version=${pom.version}
build.date=${timestamp}
```

## Java에서 System.getProperty를 이용해 가져오기

이 외에도 플러그인에 systemProperty를 집어 넣어서 자바 코드에서접 직접 System.getProperty(“timestamp”); 와 같이 호출 하는 방법이 있습니다.

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>exec-maven-plugin</artifactId>
    <version>${maven.exec.plugin.version}</version>
    <executions>
        <execution>
            <goals>
                <goal>java</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <mainClass>${exec.main-class}</mainClass>
        <systemProperties>
            <systemProperty>
                <key>timestamp</key>
                <value>${timestamp}</value>
            </systemProperty>
        </systemProperties>
    </configuration>
</plugin>
```

## webapp 디렉토리 내부에서 사용하기

html, jsp, javascript, css 등의 webapp 파일에서 maven 변수값을 받으려면 `maven-war-plugin`플러그인 을 사용해야 합니다. Maven에서 war 패키징을 할 때 프로퍼티를 할당해 줍니다.

pom.xml:
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <version>2.6</version>
    <configuration>
        <webappDirectory>${deploy.path}</webappDirectory>
        <webXml>${basedir}/src/main/resources-${env}/properties/web.xml</webXml>
        <webResources>
            <resource>
                <filtering>true</filtering>
                <directory>${basedir}/src/main/webapp</directory>
                <includes>
                    <include>**/*.jsp</include>
                    <include>**/*.js</include>
                </includes>
            </resource>
            <resource>
                <filtering>false</filtering>
                <directory>${basedir}/src/main/webapp</directory>
                <excludes>
                    <exclude>**/*.jsp</exclude>
                    <include>**/*.js</include>
                </excludes>
            </resource>
        </webResources>
    </configuration>
</plugin>
```

webapp 폴더내의 모든 resource에서 쓸것이 아니라면 쓸 파일들만 filter를 true로해 주고 나머지는 false로 설정해 놓는 것이 좋습니다. 이렇게 설정해주면 아래와 같이 파일 내부에서 변수를 사용할 수 있습니다.

```jsp
<link rel="stylesheet" type="text/css" href="/resources/css/common.css?${timestamp}">
```

참고: https://vnthf.github.io/blog/Spring-Maven-Propertie-%EB%B3%80%EC%88%98-%EC%93%B0%EA%B8%B0/


### jsp 에서 maven 변수(build.timestamp) 사용하기

결국 간단히 jsp페이지에서 pom.xml 변수를 받아 쓰는 방법은

pom.xml:
```xml
...
<properties>
    <java-version>1.7</java-version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>

    <!-- Web -->
    <jsp.version>2.2</jsp.version>
    <jstl.version>1.2</jstl.version>
    <servlet.version>2.5</servlet.version>

    <!-- build timestamp : use static resources -->
    <build.timestamp>${maven.build.timestamp}</build.timestamp>
    <maven.build.timestamp.format>yyyyMMddHHmmss</maven.build.timestamp.format>
</properties>
...
<build>
    <defaultGoal>install</defaultGoal>
    <directory>${basedir}/target</directory>
    <finalName>project-name</finalName>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-war-plugin</artifactId>
            <version>2.6</version>
            <configuration>
                <webappDirectory>${deploy.path}</webappDirectory>
                <webResources>
                    <resource>
                        <filtering>true</filtering>
                        <directory>${basedir}/src/main/webapp/</directory>
                        <includes>
                            <include>**/*.jsp</include>
                        </includes>
                    </resource>
                </webResources>
            </configuration>
        </plugin>
        ...
    </plugins>
</build>
```

위 처럼 pom.xml를 선언하고

xxx.jsp:
```html
<link rel="stylesheet" type="text/css" href="/css/common.css?${build.timestamp}">
```

위처럼 href 안에 dummy parameter를 붙여주면 maven 패키징시에 변수가 치환된다.


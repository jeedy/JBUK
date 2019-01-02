# 데이터베이스 정보 (user, password) 암호화 방법

외부에 데이터 베이스 접근 정보가 노출되지 않도록 암호화하는 방법을 설명한다. jasypt 암호화 방식이 있으나 RSA 개인키, 공개키를 이용한 방식으로 셋팅하는 방법을 설명한다.

핵심은 BasicDataSource를 상속받아 setPassword 하는 부분에서 복호화시켜 Datasource 가 생성되도록 수정하는 것이다. 이것을 응용하면 Spring, maven 상관없이 암호화 방법만 선택해 적용이 가능하다.

## 적용방법

1. jasypt 암호화 라이브러리를 통한 적용
    - http://monibu1548.github.io/2017/02/09/jasypt/
    - https://www.mynotes.kr/jasypt-%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-jdbc-%EC%95%94%ED%98%B8%ED%99%94-%EB%B0%A9%EB%B2%95/
    - http://www.jasypt.org/spring31.html
    - http://www.egovframe.go.kr/wiki/doku.php?id=egovframework:rte:fdl:encryption_decryption

2. RSA 암호화 키를 이용한 방법 (채택)
    - http://jo.centis1504.net/?p=30
    - http://www.nexpert.net/438
    - https://d2.naver.com/helloworld/227016
    - https://www.holaxprogramming.com/2017/06/12/encryption-with-rsa/
    - http://nine01223.tistory.com/101
    - https://www.mkyong.com/java/java-asymmetric-cryptography-example/

## workspace spec

- ava1.7
- Spring 3.1
- oracle
- ~~maven~~
- ~~jasypt~~
- openssl RSA


## 1. 개인키, 공개키 생성 (http://jo.centis1504.net/?p=30)

SSL 처럼 RSA 암호화를 이용해 인코딩 한다. 기본적인 RSA에 대한 사전지식이 필요하다.

java 공개키는 X509 표준, 개인키는 PKCS8 표준
pkcs8 을 사용하려면 der변환(암호화된 인코딩)이 필요하다.

RSA 참고
- https://www.holaxprogramming.com/2017/06/12/encryption-with-rsa/
- https://www.mkyong.com/java/java-asymmetric-cryptography-example/


```bash
#개인키(privateClient.key) 생성 후에 소스상에서 사용하기 위해 DER 파일 형식으로 변환이 필요(privateClient-PKCS8.der) 키 변환
#개인키(privateClient.key)를 이용해 공개키(publicClient.der) 생성
# in windows console

# 2048 비트 RSA 개인 키(원본) 생성
openssl genrsa -out privateClient.key 2048

# 개인 키를 PKCS # 8 형식(소스상 사용키)으로 변환 - 원본 개인키로 소스상에서 사용시 에러발생 그래서 DER 형식으로 변환사용 필요.
openssl pkcs8 -topk8 -inform PEM -outform DER -in privateClient.key -out privateClient-PKCS8.der -nocrypt

# DER 형식으로 공개 키(소스상 사용키) 부분을 출력-
openssl rsa -in privateClient.key -pubout -outform DER -out publicClient.der
```

## 2. 원본개인키(privateClient.key), 공개키(publicClient.der), 개인키(privateClient8.der) src/main/resource/keyPair 디렉토리 밑에 복사

## 3. DecryptDataSource.java 생성

BasicDataSource를 상속받아 setPassword 메소드에서 암호화된 패스워드 코드를 디코딩해서 입력되도록 수정한다.

### 참고 자료
https://www.mynotes.kr/jasypt-%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-jdbc-%EC%95%94%ED%98%B8%ED%99%94-%EB%B0%A9%EB%B2%95/

```java
package com.hyundaicard.privia.common.decrypt;

import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Security;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.sql.SQLFeatureNotSupportedException;
import java.util.logging.Logger;

import javax.crypto.Cipher;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.dbcp.BasicDataSource;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.jasypt.encryption.pbe.StandardPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.EnvironmentStringPBEConfig;
import org.springframework.core.io.ClassPathResource;
import org.springframework.util.FileCopyUtils;

public class DecryptDataSource extends BasicDataSource {

    private static final String ENCRYPTED_VALUE_PREFIX = "ENC(";
    private static final String ENCRYPTED_VALUE_SUFFIX = ")";

    public Logger getParentLogger() throws SQLFeatureNotSupportedException {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public void setPassword(String password) {
        // Input database password value with decrypt password value
        super.setPassword(decryptor(password));
    }

    /*@Override
    public synchronized void setUrl(String url) {
        // TODO Auto-generated method stub
        super.setUrl(decryptor(url));
    }

    @Override
    public void setUsername(String username) {
        // TODO Auto-generated method stub
        super.setUsername(decryptorJasypt(username));
    }*/

    public String decryptor(String param) {
        if (isEncryptedValue(param)) {
            try {
                PrivateKey privateClientKey = (PrivateKey) getKey("keyPair/privateClient8.der", "private");
                return decryptText(getInnerEncryptedValue(param), privateClientKey);
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            return param;
        }

        return null;
    }

    public static Object getKey(final String filename, final String flag) throws Exception {
        ClassPathResource classPathResource = new ClassPathResource(filename);

        byte[] keyBytes = FileCopyUtils.copyToByteArray(classPathResource.getInputStream());

        KeyFactory kf = KeyFactory.getInstance("RSA");
        if ("public".equals(flag)) {
            // https://docs.oracle.com/javase/8/docs/api/java/security/spec/X509EncodedKeySpec.html
            X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
            return kf.generatePublic(spec);
        } else if ("private".equals(flag)) {
            // https://docs.oracle.com/javase/8/docs/api/java/security/spec/PKCS8EncodedKeySpec.html
            PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(keyBytes);
            return kf.generatePrivate(spec);
        }
        return null;

    }

    public static String encryptText(final String msg, final PublicKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return Base64.encodeBase64String(cipher.doFinal(msg.getBytes("UTF-8")));
    }

    public static String decryptText(final String msg, final PrivateKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, key);
        return new String(cipher.doFinal(Base64.decodeBase64(msg.getBytes("UTF-8"))), "UTF-8");
    }

    /** Jasypt를 이용한 경우
    public String decryptorJasypt(final String param) {
        if (isEncryptedValue(param)) {
            Security.addProvider(new BouncyCastleProvider());

            EnvironmentStringPBEConfig environmentStringPBEConfig = new EnvironmentStringPBEConfig();
            // environmentStringPBEConfig.setAlgorithm("PBEWithMD5AndTripleDES");
            // environmentStringPBEConfig.setProvider(new BouncyCastleProvider());

            environmentStringPBEConfig.setAlgorithm("PBEWITHSHA256AND128BITAES-CBC-BC");
            environmentStringPBEConfig.setProviderName("BC");
            environmentStringPBEConfig.setPasswordEnvName("ASOG_ENCRYPTION_KEY");

            StandardPBEStringEncryptor encryptor = new StandardPBEStringEncryptor();
            encryptor.setConfig(environmentStringPBEConfig);

            return encryptor.decrypt(getInnerEncryptedValue(param));
        } else {
            return param;
        }

    }
    */

    public static boolean isEncryptedValue(final String value) {
        if (value == null) {
            return false;
        }
        final String trimmedValue = value.trim();
        return (trimmedValue.startsWith(ENCRYPTED_VALUE_PREFIX) && trimmedValue.endsWith(ENCRYPTED_VALUE_SUFFIX));
    }

    private static String getInnerEncryptedValue(final String value) {
        return value.substring(ENCRYPTED_VALUE_PREFIX.length(), (value.length() - ENCRYPTED_VALUE_SUFFIX.length()));
    }

    public static void main(String[] args) {
        /** Jasypt를 이용한 암호화화
       Security.addProvider(new BouncyCastleProvider());

        EnvironmentStringPBEConfig environmentStringPBEConfig = new EnvironmentStringPBEConfig();
        // environmentStringPBEConfig.setAlgorithm("PBEWithMD5AndTripleDES");
        environmentStringPBEConfig.setProviderName("BC");
        environmentStringPBEConfig.setAlgorithm("PBEWITHSHA256AND128BITAES-CBC-BC");
        // environmentStringPBEConfig.setPasswordEnvName("ASOG_ENCRYPTION_KEY");
        environmentStringPBEConfig.setPassword("enctype1234");

        StandardPBEStringEncryptor encryptor = new StandardPBEStringEncryptor();
        encryptor.setConfig(environmentStringPBEConfig);

        String encPassword1 = encryptor.encrypt("passwd1");
        System.out.println("passwd1 enc/dec");
        System.out.println(encPassword1);
        System.out.println(encryptor.decrypt(encPassword1));
        */

        PublicKey pKey;
        try {
            pKey = (PublicKey) getKey("keyPair/publicClient.der", "public");

            String encPassword1 = encryptText("passwd1" , pKey);
            System.out.println("passwd1 enc/dec");
            System.out.println(encPassword1);

            String encPassword2 = encryptText("passwd2" , pKey);
            System.out.println("passwd2 enc/dec");
            System.out.println(encPassword2);

        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
```

## 4. DecryptDataSource.main() 메소드를 이용해 암호화된 패스워드 생성

## 5. resource/db.properties  password에  위 암호화된 패스워드 코드 입력
```bash
# JDBC
COMMON.driverClass=oracle.jdbc.driver.OracleDriver
COMMON.url=jdbc:oracle:thin:@192.168.0.1:4000:odindev
COMMON.username=test
COMMON.password=ENC(....암호화된 패스워드 코드...)
....

```

## 6. Datasource 빈 설정 xml(database-context.xml) 에 datasource class 소스 변경
```xml
<bean id="testDataSoruce"                        class="com.hyundaicard.privia.common.decrypt.DecryptDataSource" destroy-method="close">
    <property name="driverClassName"             value="${COMMON.driverClass}" />
    <property name="url"                         value="${COMMON.url}" />
    <property name="username"                    value="${COMMON.username}" />
    <property name="password"                    value="${COMMON.password}" />
    <property name="maxActive"                   value="${COMMON.maxActive}" />
    <property name="maxIdle"                     value="${COMMON.maxIdle}" />
    <property name="minIdle"                     value="${COMMON.minIdle}" />
    <property name="maxWait"                     value="-1" />
    <property name="initialSize"                 value="${COMMON.initialSize}" />
    <property name="poolPreparedStatements"      value="true" />
    <property name="maxOpenPreparedStatements"   value="100" />
    <property name="testOnBorrow"                value="true" />
    <property name="testOnReturn"                value="false" />
    <property name="testWhileIdle"               value="false" />
    <property name="validationQuery"             value="SELECT 1 from dual" />
</bean>
```

## 7. pom.xml 에 관련 라이브러리 추가 (단, jasypt라이브러리를 사용할 경우만)
```xml
<!-- https://mvnrepository.com/artifact/org.jasypt/jasypt -->
<dependency>
    <groupId>org.jasypt</groupId>
    <artifactId>jasypt-spring31</artifactId>
    <version>1.9.2</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.bouncycastle/bcprov-jdk15 -->
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15</artifactId>
    <version>1.46</version>
</dependency>

<dependency>
    <groupId>commons-codec</groupId>
    <artifactId>commons-codec</artifactId>
    <version>1.7</version>
    <scope>provided</scope>
</dependency>
```

## 번외. Spring 없이 pure java 로 구현해야할 경우
DecryptDataSource.getKey() 메소드 에서 `keyPair/privateClient8.der` 파일을 가져오는 부분만 java 에서 제공하는 라이브러리로 처리하면 됨.

```java
public class DecryptDataSource extends BasicDataSource {

// ...(생략)...
    
    public static Object getKey(final String filename, final String flag) throws Exception {
        URL url = System.class.getResource("/"+filename);   // ※ 중요 파일주소 앞에 '/'를 붙여주지 않으면 파일위치를 못찾음.
        byte[] keyBytes = Files.readAllBytes(new File(url.toURI()).toPath());
        
        KeyFactory kf = KeyFactory.getInstance("RSA");
        if ("public".equals(flag)) {
            // https://docs.oracle.com/javase/8/docs/api/java/security/spec/X509EncodedKeySpec.html
            X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
            return kf.generatePublic(spec);
        } else if ("private".equals(flag)) {
            // https://docs.oracle.com/javase/8/docs/api/java/security/spec/PKCS8EncodedKeySpec.html
            PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(keyBytes);
            return kf.generatePrivate(spec);
        }
        return null;

    }

// ...(생략)...
    
//    public static void main(String[] args) {
//        BasicDataSource dataSource = new DecryptDataSource();
//        dataSource.setPassword("ENC(d5hLo0d+EBq64vo6eYu/gD3iScdQSYp5qXWnFVweoRK3xSU5R+x4+DFkqnqtLZ6Gg0lUWbxlqOgjCNxi/NKNkybcU6poO9q/lO8cXS3jqIfxWDVzq0+wsdkzlANTR2pc674P06n4Vcy9AYDcvk2+nI47LQ91x+63754C43g6iKYglSyN7PhwRg8sA2Elp6IprjVw/xaL8qgtlkBnDqkNA/ZbiOrv+hWdzX1JBX9IaHD+/j8VNhMs+tdYVzgETJ1jpLkz4tgLvcQk19+0xIpDuZ44MstWNsXDYnuOUL72gZL8YmS2+mrIvMCsSWaN38umz/RNVVotIy3JZESJjoZbBQ==)");
//    }

}
```
# 순수 자바에서 로깅방법

두가지 방법이 있는데, 특별한 properties 설정없이 사용할 수 있는 방법이다.

1. 하나는 `java.util` 패키지에서 제공하는 Logger 를 이용하는 방법
1. 하나는 apache `commons-logging` 라이브러리에서 제공하는 Log, LogFactory를 이용하는 방법

둘다 로깅되는 내용은 같은 것으로 봐선 결국 `commons-logging` 라이브러리도 `java.util.Log`를 사용하기 때문인 것으로 추측된다.

- 변수 logger는 apache `commons-logging` 를 이용한 방법
- 변수 logger2는 `java.util` 패키지를 이용한 방법

개인적인 의견으로 완전한 pure java로 개발할 일은 많지 않고 최소한의 몇가지 라이브러리를 가져다 쓸텐데,
결국 그 라이브러리들은 apache `commons-logging`를 dependency 하기 때문에,
그리고 추후 log4j, SLF4J 와 같은 logging 라이브러리들과 조합하기 위해선 apache `commons-logging`를 사용하는 것으로 추천한다.

여튼 소스는
```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.junit.Assert;
import org.junit.Test;

public class TestDBManager {

    private static final Log logger = LogFactory.getLog( TestDBManager.class );
    private static final Logger logger2 = Logger.getLogger( TestDBManager.class.getName() );

    @Test
    public void 데이터베이스_접속_확인() throws Exception{
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        Map<String, String> result = new HashMap<String, String>();

        try {

            StringBuilder query = new StringBuilder();

            query.append("select DUMMY from dual");
            // 모듈체크
            conn = DBManager.getInstance().getDataSource(true).getConnection();
            ps = conn.prepareStatement(query.toString());
            rs = ps.executeQuery();
            result = DBManager.getRsToMap(rs);
            logger.info(result.toString());
            logger2.info(result.toString());
            Assert.assertNotNull(result);
        } finally {
            DBManager.freeConnection(conn, ps, rs);
//            BasicDataSource datasource = (BasicDataSource)DBManager.getInstance().getDataSource(true);
//            datasource.close();
        }

    }
}
```

```
1월 04, 2019 9:50:37 오전 com.hyundaicard.privia.payment.utils.TestDBManager 데이터베이스_접속_확인
정보: {DUMMY=X}
1월 04, 2019 9:50:37 오전 com.hyundaicard.privia.payment.utils.TestDBManager 데이터베이스_접속_확인
정보: {DUMMY=X}

```
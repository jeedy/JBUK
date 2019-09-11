# 마이바티스

## :bomb: troubleshooting
### 1. parameterType에 들어갈 VO class에 inner class를 선언해서 사용하는 경우 `static`으로 반드시 선언해야한다.

일반 inner class로 선언해서 사용하는 경우:  
> o.s.w.s.m.m.a.ExceptionHandlerExceptionResolver - Resolved [org.mybatis.spring.MyBatisSystemException: nested exception is org.apache.ibatis.executor.ExecutorException: No constructor found in com.priviatravel.api.travel.coupon.model.GetCouponInfoResVO$CouponUseScopeResVO matching [java.math.BigDecimal, java.math.BigDecimal, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String]] 

```java
import java.util.List;

import org.apache.ibatis.type.Alias;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
@ApiModel(value = "GetCouponInfoResVO", description = "쿠폰 정보 조회")
public class GetCouponInfoResVO {
    
    @ApiModelProperty(notes = "쿠폰 번호", required = true)
    private long no;

    @ApiModelProperty(notes = "쿠폰 발급 일자", required = true)
    private String issueDate;
    
    @ApiModelProperty(notes = "사용범위", required = false)
    private List<CouponUseScopeResVO> useScopes;
    
    @Data
    @ApiModel(value = "GetCouponInfoResVO.CouponUseScopeResVO", description = "쿠폰 사용범위 조회(통합어드민참조)")
    public static class CouponUseScopeResVO{
        @ApiModelProperty(notes = "순번", required = true)
        private int seq;
        
        @ApiModelProperty(notes = "범위코드1", required = false)
        private String scop1;
        @ApiModelProperty(notes = "범위코드2", required = false)
        private String scop2;
    }
}
```

#### 덤. inner class를 `resultType` 값으로 사용한는 방법
inner class는 '.' 대신 '$' 으로 표현해줘야한다. 

CouponMapper.xml: 
```xml
 <select id="getUseScopes" parameterType="long" resultType="com.api.coupon.model.GetCouponInfoResVO$CouponUseScopeResVO">
 ... 
 <select>
```
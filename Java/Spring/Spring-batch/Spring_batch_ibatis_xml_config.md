# Spring Batch IBATIS XML 설정 방법

## Quarts(스케줄러) 셋팅방법

task-context.xml
```xml
<bean class="org.springframework.scheduling.quartz.SchedulerFactoryBean">
    <property name="applicationContextSchedulerContextKey" value="applicationContext"/>
    <property name="triggers">
        <list>
            <ref bean="common.customer.triger"/>
            <ref bean="travel.event.coupon.triger"/>
            ...
        </list>
    </property>
</bean>
<import resource="classpath:batch/schedule/*-schd.xml"/>
```

classpath:batch/schedule/event-schd.xml
```xml
<bean id="travel.event.coupon.triger" class="org.springframework.scheduling.quartz.CronTriggerBean">
    <property name="jobDetail">
        <bean class="org.springframework.scheduling.quartz.JobDetailFactoryBean">
            <property name="group" value="privia-travel-batch"/>
            <property name="jobClass" value="com.hyundaicard.privia.batch.common.supports.JobLauncherDetails"/>
            <property name="jobDataAsMap">
                <map>
                    <entry key="appProps" value-ref="appProps"/>
                    <entry key="jobLocator" value-ref="jobRegistry"/>
                    <entry key="jobLauncher" value-ref="jobLauncher"/>
                    <entry key="jobName" value="travel.event.coupon.job"/>
                </map>
            </property>
        </bean>
    </property>
    <property name="cronExpression" value="0 3,33 * * * ?"/>
</bean>
...
```

## JOB 셋팅방법

travel.event.coupon.job
```
<batch:job id="travel.event.coupon.job" parent="parentCommonJob">
    <batch:description>
    <![CDATA[
        @subject   배치 테스트
        @since     2019-02-20
        @description
            배치테스트를 위한 Job
    ]]>
    </batch:description>

    <batch:step id="travel.event.coupon.select.step" next="travel.event.sms.select.step">
        <batch:tasklet>
            <batch:chunk reader="bean.travel.event.coupon.step.select" writer="bean.travel.event.coupon.step.insert" commit-interval="500"/>
        </batch:tasklet>
    </batch:step>

    <batch:step id="travel.event.sms.select.step">
        <batch:tasklet>
            <batch:chunk reader="bean.travel.event.sms.step.select" writer="bean.travel.event.sms.step.insert" commit-interval="500"/>
        </batch:tasklet>
    </batch:step>

</batch:job>

<bean id="bean.travel.event.coupon.step.select" class="com.hyundaicard.privia.batch.travel.event.item.CouponMybatisReader" scope="step">
    <description>발송 대상 추출</description>
    <property name="sqlSessionFactory" ref="sfForOracleHCCTVT"/>
    <property name="queryId" value="travel.event.selectCouponTarget"/>
    <property name="pageSize" value="100000"/>
    <property name="parameterValues">
        <map>
            <entry key="timestamp" value="#{jobParameters['current_datetime']}"/>
        </map>
    </property>
</bean>
<bean id="bean.travel.event.coupon.step.insert" class="com.hyundaicard.privia.batch.travel.event.item.EventItemCouponWriter" scope="step">
    <description>쿠폰 자동발급</description>
    <property name="sqlSessionFactory" ref="sfForOracleHCCTVT"/>
    <property name="statementId" value="travel.event.insertCouponTarget"/>
    <property name="assertUpdates" value="false"/>
</bean>
<bean id="bean.travel.event.sms.step.select" class="com.hyundaicard.privia.batch.travel.event.item.CouponMybatisReader" scope="step">
    <description>쿠폰발급자 추출</description>
    <property name="sqlSessionFactory" ref="sfForOracleHCCTVT"/>
    <property name="queryId" value="travel.event.selectSmsTarget"/>
    <property name="pageSize" value="100000"/>
    <property name="parameterValues">
        <map>
            <entry key="timestamp" value="#{jobParameters['current_datetime']}"/>
        </map>
    </property>
</bean>
<bean id="bean.travel.event.sms.step.insert" class="org.mybatis.spring.batch.MyBatisBatchItemWriter" scope="step">
    <description>문자발송</description>
    <property name="sqlSessionFactory" ref="sfForOracleHCCTVT"/>
    <property name="statementId" value="travel.event.insertSmsTarget"/>
    <property name="assertUpdates" value="false"/>
</bean>
```

## JOB IBATIS reader/wirter 셋팅

## JOB Tasklet 구현 방법

### Basic Tasklet

### MybatisTasklet


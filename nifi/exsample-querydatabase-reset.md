# Reset "Component State" of QueryDatabaseTable processor
이번 예제는 Nifi Proccessor API도 같이 활용, processor 사용방법 뿐만 아니라 Nifi rest-api 사용 방법까지 같이 설명한다.

이 예제를 참고로 해서 Processor 들을 자동으로 컨트롤 하고 싶을때 참고하면 좋다.
## Overview
QueryDatabaseTable 에서 쿼리를 할경우 "Component State" 에 마지막으로 가져온 primary key 값을 기록하고 있다.

이는 중복 row를 가져오지 않기 위함이나 때때로 초기화가 필요한 순간도 있다. curl 를 통해  nifi rest-API를 직접 호출해서 초기화하는 방법도 있지만 crontab 방식으로 매일 특정시간에 자동으로 초기화해주는 프로세스를 만들 필요가 있을때 사용한다.


> nifi rest-API
https://nifi.apache.org/docs/nifi-docs/rest-api/index.html

## Overview
QueryDatabaseTable 가 `start` 상태라면 `stop` 상태로 변경해 줘야 `state` 값 삭제가 가능하다. 그렇기 때문에 processor를 `stop` 시키는 API 호출이 우선시 되어야 한다. 
그런데 `stop` 시키는 API에 들어가는 parameter 값에  현재 processor의 `revision` 정보를 필요로 한다. 그렇기 때문에 현재 `revision` 정보를 가져오기 위한 API 호출이 제일 처음 시작한다. 

> GET/processors/{id}

호출 하면 response 값으로 `revision` 값을 주고 이 값만 재사용해서 컨트롤 하면된다.
```json
{
    "revision": {
	    "clientId": "value",
	    "version": 0,
	    "lastModifier": "value"
	},
    "id": "value",
    "uri": "value",
    "position": {…},
    "permissions": {…},
    "bulletins": [{…}],
    "disconnectedNodeAcknowledged": true,
    "component": {…},
    "inputRequirement": "value",
    "status": {…},
    "operatePermissions": {…}
}
```


> PUT/processors/{id}/run-status


![전체view](./images/nifi-querydatabase-reset-workflow-overview.png)

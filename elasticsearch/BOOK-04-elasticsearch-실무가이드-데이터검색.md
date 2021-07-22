# 04 _데이터 검색

문서는 색인시 설정한 분석기에 의해 **분석 과정을 거쳐 토큰으로 분리**되는데, 이러한 **분석기는 색인 시점에 사용할수도 있지만 검색 시점에 사용하는 것도 가능하다.**    
특정 문장이 검색어로 요청되면 분석기를 통해 분석된 토큰의 일치 여부를 판단해서 그 결과에 **점수(Score)** 를 매긴다.   
\- p148

엘라스틱 서치는 관계형 데이터베이스와 다르게 페이징된 해당 문서만 선택적으로 가져오는 것이 아니라 모든 데이터를 읽게 된다. 예를 들어, 예제와 같이 5건씩 페이징한 검색 결과의 2페이지를 요청하더라도 총 10건의 문서를 읽어야만 한다.  
\- p163

## 4.2. Query DSL 이해하기

### 4.2.2. Query DSL 쿼리와 필터

#### 필터 컨텍스트
- `Yes/No` 로 판단 할 수 있는 수준의 조건 검색시 필터 컨텍스트를 이용.
- 연관성 관련 계산을 하지 않음.
- 엘라스틱서처 레벨에서 처리, 상대적으로 빠름
- 예시) "create_year" 필드 값이 2018년인지 여부, "status" 필드에 "use" 라는 코드 포함 여부

필터 컨텍스트 Query DSL 예시: 
```json
POST movie_search/_search
{
    "query": {
        "bool": {
            "must":[
                {
                    "match_all": {}
                }
            ],
            "filter": {
                "term": {
                    "repGenreNm": "다큐멘터리"
                }
            }
        }
    }
}
```

#### 쿼리 컨텍스트
- 전문 검색 시 사용
- 분석기에 의한 분석 수행, 연관성 관련 score 계산, 루씬 레벨에서 분석 과정을 거침, 상대적으로 느림
- 예시) "Harry Potter" 같은 문장 분석

쿼리 컨텍스트 Query DSL 예시:
```json
POST movie_search/_search
{
    "query": {
        "match": {
            "movieNm": "기묘한 가족"
        }
    }
}
```

### 4.2.3. Query DSL의 주요 파라미터

#### Multi Index 검색
- 쉼표(`,`) 를 이용해 다수의 인덱스에서 검색할 수 있다.
```sh
POST movie_search,movie_auto/_search
```
- 익덱스명을 와일드카드(`*`)를 이용해 검색할 수 있다.
```sh
POST log-2020-*/_search
```

#### 쿼리 결과 페이징
기본값은 from 0, size 5로 설정되어있다.    
엘라스틱서치는 DB와 다르게 페이징된 해당문서만 선택적으로 가져오는 것이 아니라 모든 데이터를 읽게 된다. 예를들어, 5건씩 페이징한 검색 결과의 2페이지를 요청하더라도 총 10건의 문서를 읽어야만 한다.


#### 쿼리 결과 정렬
기본적으로 `_score`를 통해 정렬하지만 특정 필드로 정렬하고 싶을때 사용한다.   
아래 예제에선 `prdYear` 를 정렬한후 동일한 값일 경우 `_score` 로 정렬해 오도록 한다.
```sh
POST movie_search/_search
{
    "query": {
        "term": {
            "repNationNm": "한국"
        }
    },
    "sort": {
        "prdYear": {
            "order":"asc"
        },
        "_score": {
            "order":"desc"
        }
    }
}
```

#### _source 필드 필터링
검색시 `_source` 파라미터를 추가해 특정 필드만 가져오도록 할 수 있다.    
검색결과 용량이 줄어든다는 뜻은 네트워크 사용량이 줄어든다는 뜻이다.(_source에 담긴 데이터가 적으면 별차이 없겠지만 양이 많다면 속도와 트래픽양이 의미있는 수치로 줄어든다.)
```sh
POST movie_search/_search
{
    "_source": [
        "movieNm"
    ],
    "query": {
        "term": {
            "repNationNm": "한국"
        }
    }
}
```

#### 범위검색
예제참조
```sh
POST movie_search/_search
{
    "query": {
        "range": {
            "prdYear": {
                "gte": "2016",
                "lte": "2017"
            }
        }
    }

}
```

#### operator 설정
엘라스틱서치는 검색시 문장이 들어올 경우 기본적으로 `OR` 연산.    
`AND` 연산을 이용하고 싶을 경우 사용한다.
```sh
POST movie_search/_search
{
    "query": {
        "match": {
            "movieNm": {
                "query": "자전차왕 엄복동",
                "operator": "and"
            }
        }
    }
}
```

#### minimum_should_match 설정
문서의 결과에 포함될 텀의 최소 개수를 지정, 아래와 같이 작성한다면 텀의 갯수와 `minimum_should_match`의 개수가 일치하기 때문에 AND 연산과 동일한 효과를 낼 수 있다.
```sh
POST movie_search/_search
{
    "query": {
        "match": {
            "movieNm": {
                "query": "자전차왕 엄복동",
                "minimum_should_match": 2
            }
        }
    }
}
```

#### fuzziness 설정
레벤슈타인(Levenshtein) 편집 거리 알고리즘을 기반으로 문서의 필드값을 여러 번 변경하는 방식으로 동작한다. 유사한 검색 결과를 위해 허용 범위의 텀으로 변경해 가며 문서를 검색한다.    
`Fly High`를 검색하고 싶은데 사용자가 `Fli High`라고 입력했다면 검색이 안되야 하겠지만 `Fuzziness` 값을 1을 주고 검색 했다면 검색이 가능하다.

#### boost 설정
검색시 가능 많이 사용하는 파라미터중 하나이다. 이 파라미터는 관련성이 높은 필드나 키워드에 가중치를 더 줄 수 있게 해준다.
```sh
POST movie_search/_search
{
    "query": {
        "multi_match": {
            "query": "Fly",
            "fields": ["movieNm^3", "movieNmEn"]
        }
    }
}
```
> `Fly` 라는 단어를 `movieNm`과 `movieNmEn`이라는 두 개의 필드에서 조회한다. 만약 `movieNm` 이 일치하는 문서가 있다면 그 문서에 스코어 가중치 값이 3을 곱하게 된다.


## 4.3. Query DSL 의 주요쿼리

### 4.3.1. Match All Query
모든 문서를 검색

### 4.3.2. Match Query
텍스트, 숫자, 날짜 등이 포함된 문장을 형태소 분석을 통해 텀으로 분리한 후 이 텀들을 이용해 검색 질의를 수행한다.
```sh
POST movie_search/_search
{
    "query": {
        "match": {
            "movieNm": "그대 장미"
        }
    }
}
```
> "그대 장미" 라는 검색어를 "그대", "장미" 라는 2개의 텀으로 분리한다. 이후 별도의 `operator` 필드가 지정돼 있지 않기 때문에 두개의 텀을 OR 연산을 이용해 검색을 수행한다.

### 4.3.3. Multi Match Query
단일 필드가 아닌 여러 개의 필드를 대상으로 검색해야 할 때 사용하는 쿼리
```sh
POST movie_search/_search
{
    "query": {
        "multi_match": {
            "query": "가족",
            "fields": ["movieNm", "movieNmEn"]
        }
    }
}
```

### 4.3.4. Term Query
Match Query의 경우에는 텍스트에 대한 형태소 분석을 통해 검색을 수행하지만 Term Query의 경우 검색어를 하나의 텀으로 처리하기 때문에 필드에 텀이 정확히 존재하지 않은 경우 검색이 되지 않는다. 따라서 영문의 경우에는 대소문자가 다를 경우 검색되지 않으므로 특히 주의해야 한다.

### 4.3.5. Bool Query
- must : 반드시 조건에 만족하는 문서
- must_not : 반드시 만족하지 않는 문서
- should : OR 조건
- filter : 조건을 포함하고 있는 문서를 출력, `must` 와 비슷하다고 생각하겠지만 소코어에 영향을 주지 않는다.

### 4.3.6. Query String
내장된 쿼리 분석기를 이용하는 질의를 작성한다. 


### 4.3.7. Prefix Query
접두어 검색

### 4.3.8. Exists Query
컬럼에 값이 있는 문서만 검색 하고 싶을때

### 4.3.9. Wildcard Query
첫글자에 와일드카드를 사용하지 말자, 전체 문서를 검색해서 부하가 심하게 발생한다.

와일드카드 사용예시
```sh
POST movie_search/_search
{
    "query": {
        "wildcard": {
            "typeNm": "장?"
        }
    }
}
```


### 4.3.10. Nested Query
join 이라는 말로 혼동이 되는데, DB join 과는 다른 개념이다. Object 필드안에 검색을 이용할때 사용한다. 자세한건 내용은 `3.3.11. Nested 데이터 타입` 편 에서 다루고 있다.






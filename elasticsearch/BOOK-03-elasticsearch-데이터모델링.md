# 3. 데이터 모델링

## 3.1. 매핑 api 이해하기

### 매핑 정보를  생성할 때 고려사항
- 문자열을 분석할 것인가?
- _source에 어떤 필드를 정의할 것인가?
- 날짜 필드를 가지는 필드는 무엇인가?
- 매핑에 정의되지 않고 유입되는 필드는 어떻게 처리할 것인가?

> 실무에서는 다양한 이유로 `동적 매핑`을  거의 사용하지 않는다.


### 3.1.1. 매핑 인덱스 만들기
아래는 movie를 입력하기 위한 매핑정보, 검색 대상은 "영화제목" 필드이므로 분석 가능하도록 `text` 타입으로 정의한다. 나머지 필드는 보여주기만 할 것이기 때문에 특성에 따라 integer 타입, keyword 타입으로 설정한다. 

> 검색이라는 `text` 타입, 보여주기만 하면 되는 필드는 integer, keyword 같은 타입으로 선언하면 된다.

Create index mapping:
```
PUT movie_search
{
    "settings":{
        "number_of_shards":5
        ...
    }
}


response:
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "movie_search"
}
```

### 3.1.2. 매핑 확인
Get index mapping:
```
GET movie_search/_mapping

response:
{
  "movie_search" : {
    "mappings" : {
      "properties" : {
        "audiCnt" : {
          "type" : "integer",
          "null_value" : 0
        },
        "companies" : {
          "properties" : {
            "companyCd" : {
              "type" : "keyword"
            },
            "companyNm" : {
              "type" : "keyword"
            }
          }
        },
        "directors" : {
          "properties" : {
            "peopleNm" : {
              "type" : "keyword"
            }
          }
        },
        "genreAlt" : {
          "type" : "keyword"
        },
        "movieCd" : {
          "type" : "keyword"
        },
        "movieNm" : {
          "type" : "text",
          "analyzer" : "standard"
        },
        "movieNmEn" : {
          "type" : "text",
          "analyzer" : "standard"
        },
        ...( 생략)
      }
    }
  }
}

```


### 3.1.3. 매핑 파라미터
매핑 파라미터는 색인할 필드의 데이터를 어떻게 저장할지에 대한 다양한 옵션을 제공한다.

#### analyzer
해당 필드의 데이터를 형태소 분석하겠다는 의미의 파라미터다. 색인과 검색 시 지정한 분석기로 형태소 분석을 수행한다. `text 데이터 타입의 필드는 analyzer 매핑 파라미터를 기본적으로 사용해야 한다.` 별도의 분석기를 지정하지 않으면 `Standard Analyzer`로 형태소 분석을 수행한다. 

#### normalizer
normalizer 매핑 파라미터는 term query에 분석기를 사용하기 위해 사용된다. 
> 예를 들어 keyword 데이터 타입의 경우 원문을 기준으로 문서가 색인되기 때문에 cafe, Cafe, Café 는 서로 다른 문자로 인식된다. 
하지만 해당 유형을 분석기에 `asciifolding`과 같은 필터를 사용하면 같은 데이터로 인식되게 할 수 있다.

#### boost
필드에 가중치를 부여한다.
> 해당기능은 루씬 7.0버전부터 색인 시 boost 설정 기능이 제거됐다.

#### coerce
색인 시 자동 변환을 허용할지 여부를 설정하는 파라미터다. 예를 들어 `"10"`과 같은 숫자 형태의 문자열이 integer 타입의 필드에 들어온다면 엘라스틱서치는 자동으로 형변환을 수행해서 정상적으로 처리한다. 하지만 coerce 설정을 미사용으로 변경한다면 색인에 실패할 것이다.

#### copy_to
매핑 파라미터를 추가한 필드의 값을 지정한 필드로 복사한다. 예컨대 `keyword 타입의 필드에 copy_to 매핑 파라미터를 사용해 다른 필드로 값을 복사하면 복사된 필드에서는 text 타입을 지정해 형태소 분석을 할 수도 있다.`

또한 여러 개의 필드 데이터를 하나의 필드에  모아서 전체 검색 용도로 사용하기도 한다. 이를 통해 과거에 존재하던 `_all` 컬럼과 동일한 기능을 제공할 수 있다.

참고: https://www.elastic.co/guide/en/elasticsearch/reference/current/copy-to.html
```
PUT my_index
{
  "mappings": {
    "properties": {
      "first_name": {
        "type": "text",
        "copy_to": "full_name" 
      },
      "last_name": {
        "type": "text",
        "copy_to": "full_name" 
      },
      "full_name": {
        "type": "text"
      }
    }
  }
}

PUT my_index/_doc/1
{
  "first_name": "John",
  "last_name": "Smith"
}

GET my_index/_search
{
  "query": {
    "match": {
      "full_name": { 
        "query": "John Smith",
        "operator": "and"
      }
    }
  }
}
```


#### fielddata
fielddata는 엘라스틱서치가 힙 공간에 생성하는 메모리 캐시다. 과거에는 fielddata를 많이 사용했지만 반복적인 메모리 부족 현상과 잦은 GC로 현재는 거의 사용되지 않는다. 최신 버전의 엘라스틱서치는  `doc_values` 라는 새로운 형태의 캐시를 제공하고 있으며, test 타입의 필드를 제외한 모든 필드는 기본적으로 `doc_values` 캐시를 사용한다.

fielddata를 사용해야만 하는 경우도 있다. text 타입의 필드는 

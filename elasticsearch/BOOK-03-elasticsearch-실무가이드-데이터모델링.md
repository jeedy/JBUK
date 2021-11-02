# 3. 데이터 모델링

- [3.1. 매핑 api 이해하기](#31----api-----)
  * [매핑 정보를  생성할 때 고려사항](#------------------)
  * [3.1.1. 매핑 인덱스 만들기](#311-----------)
  * [3.1.2. 매핑 확인](#312------)
  * [3.1.3. 매핑 파라미터](#313--------)
    + [analyzer :star::star:](#analyzer--star--star-)
    + [search_analyzer :star::star:](#search-analyzer--star--star-)
    + [normalizer :star::star:](#normalizer--star--star-)
    + [boost](#boost)
    + [coerce](#coerce)
    + [properties :star::star::star:](#properties--star--star--star-)
    + [fields :star::star::star:](#fields--star--star--star-)
    + [copy_to :star::star:](#copy-to--star--star-)
    + [index :star:](#index--star-)
    + [fielddata](#fielddata)
    + [doc_values](#doc-values)
    + [dynamic](#dynamic)
    + [enabled](#enabled)
    + [format](#format)
    + [ignore_above :star:](#ignore-above--star-)
    + [ignore_malformed](#ignore-malformed)
    + [norms](#norms)
    + [null_value](#null-value)
    + [position_increment_gap](#position-increment-gap)
    + [similarity](#similarity)
    + [store](#store)
    + [term_vector](#term-vector)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

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

#### analyzer :star::star:
해당 필드의 데이터를 형태소 분석하겠다는 의미의 파라미터다. 색인과 검색 시 지정한 분석기로 형태소 분석을 수행한다. `text 데이터 타입의 필드는 analyzer 매핑 파라미터를 기본적으로 사용해야 한다.` 별도의 분석기를 지정하지 않으면 `Standard Analyzer`로 형태소 분석을 수행한다. 

#### search_analyzer :star::star:
일반적으로는 색인과 검색 시 같은 분석기를 사용한다. 만약 다른 분석기를 사용하고 싶은 경우 search_analyzer를 설정해서 검색 시 사용할 분석기를 별도로 지정할 수 있다.

#### normalizer :star::star:
`normalizer` 매핑 파라미터는 `term query`에 분석기를 사용하기 위해 사용된다. 
> 예를 들어 keyword 데이터 타입의 경우 원문을 기준으로 문서가 색인되기 때문에 cafe, Cafe, Café 는 서로 다른 문자로 인식된다. 
하지만 해당 유형을 분석기에 `asciifolding`과 같은 필터를 사용하면 같은 데이터로 인식되게 할 수 있다.

#### boost
필드에 가중치를 부여한다.
> 해당기능은 루씬 7.0버전부터 색인 시 boost 설정 기능이 제거됐다.

#### coerce
색인 시 자동 변환을 허용할지 여부를 설정하는 파라미터다. 예를 들어 `"10"`과 같은 숫자 형태의 문자열이 integer 타입의 필드에 들어온다면 엘라스틱서치는 자동으로 형변환을 수행해서 정상적으로 처리한다. 하지만 coerce 설정을 미사용으로 변경한다면 색인에 실패할 것이다.

#### properties :star::star::star:
오브젝트(Object) 타입이나 중첩(Nested) 타입의 스키마를 정의할 때 사용되는 옵션으로 필드의 타입을 매핑한다. 오브젝트 필드 및 중첩 필드에는 `properties`라는 서브 필드가 있다. 이 `properties`는 `object` 나 `nested`를 포함한 모든 데이터 타입이 될 수 있다.

#### fields :star::star::star:
다중 필드(multi_field) 를 설정할 수 있는 옵션이다. 필드 안에 또 다른 필드의 정보를 추가할 수 있어 같은 string 값을 각각 다른 분석기로 처리하도록 설정할 수 있다.

```sh
PUT movie_search_mapping
{
  "settings": {
    "number_of_shards": 6,
    "number_of_replicas": 1,
    "index": {
      "max_ngram_diff": 50,
      "analysis": {
        "filter": {
          "suggest_filter": {
            "type": "ngram",
            "min_gram": 1,
            "max_gram": 50
          }
        },
        "tokenizer": {
          "jaso_search_tokenizer": {
            "type": "jaso_tokenizer",
            "mistype": true,
            "chosung": false
          },
          "jaso_index_tokenizer": {
            "type": "jaso_tokenizer",
            "mistype": true,
            "chosung": true
          },
          "my_ngram_tokenizer": {
            "type": "ngram",
            "min_gram": "1",
            "max_gram": "10"
          }
        },
        "analyzer": {
          "my_ngram_analyzer": {
            "tokenizer": "my_ngram_tokenizer"
          },
          "suggest_search_analyzer": {
            "type": "custom",
            "tokenizer": "jaso_search_tokenizer"
          },
          "suggest_index_analyzer": {
            "type": "custom",
            "tokenizer": "jaso_index_tokenizer",
            "filter": [
              "suggest_filter"
            ]
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "search_string": {
        "type": "text",
        "fields": {
          "ngram": {
            "type": "text",
            "analyzer": "my_ngram_analyzer"
          },
          "jaso": {
            "type": "text",
            "analyzer": "suggest_index_analyzer"
          }
        }
      },
      "id": {
        "type": "long"
      }
    },
    "name": {
      "type": "text",
      "analyzer": "standard",
      "search_analyzer": "standard",
      "index": true,
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      },
      "copy_to": "search_string"
    },
    "name_en": {
      "type": "text",
      "analyzer": "standard",
      "search_analyzer": "standard",
      "index": true,
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      },
      "copy_to": "search_string"
    }
  }
}
```

#### copy_to :star::star:
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
#### index :star:
해당 필드값을 색인할지 결정한다. 기본값은 `true` 이며, `false`로 변경하면 해당 필드는 색인하지 않는다.
```sh
PUT test
{
  "mappings": {
    "doc": {
      "properties": {
        "name": {
          "type": "text",
          "index": false
        }
      }
    }
  }
}
```

#### fielddata
fielddata는 엘라스틱서치가 힙 공간에 생성하는 메모리 캐시다. 과거에는 fielddata를 많이 사용했지만 반복적인 메모리 부족 현상과 잦은 GC로 현재는 거의 사용되지 않는다. 최신 버전의 엘라스틱서치는  `doc_values` 라는 새로운 형태의 캐시를 제공하고 있으며, test 타입의 필드를 제외한 모든 필드는 기본적으로 `doc_values` 캐시를 사용한다.

> fielddata를 사용해야만 하는 경우도 있다. text 타입의 필드는 기본적으로 분석기에 의해 형태소 분석이 되기 때문에 집계나 정렬 등의 기능을 수행할 수 없다. 하지만 부득이하게 text 타입의 필드에서 집계나 정렬을 수행하는 경우도 있을 것이다. 이렇한 경우에 한해 fielddata를 사용할 수 있다. 하지만 fielddata는 메모리에 생성되는 캐시이기 때문에 최소한으로만 사용해야 한다는 사실에 주의해야 한다. 기본적으로 비활성화돼 있다.

```json
PUT movie_search_mapping/_mapping/_doc
{
  "properties": {
    "nationAltEn": {
      "type": "text",
      "fielddata": true
    }
  }
}
```

#### doc_values
엘라스틱서치에서 기본으로 사용하는 캐시, text 타입을 제외한 모든 타입은 doc_values 캐시를 사용한다. 루씬을 기반으로 하는 캐시 방식이다. 과거 `fielddata`를 사용했으나 현재는 모두 doc_values를 사용한다. 

필드를 정렬, 집계할 필요가 없고 스크립트에서 필드 값에 액세스할 필요가 없다면 디스크 공간 절약을 위해 doc_values 를 비활성화할 수도 있다. 한 번 비활성화된 필드는 인덱스를 재색인하지 않는 한 변경이 불가능하다.


#### dynamic
매핑 필드를 추가할 때 동적으로 생성할지, 말지 결정한다.

> https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic.html

```sh
curl -X PUT "localhost:9200/my-index-000001?pretty" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "dynamic": false, 
    "properties": {
      "user": { 
        "properties": {
          "name": {
            "type": "text"
          },
          "social_networks": {
            "dynamic": true, 
            "properties": {}
          }
        }
      }
    }
  }
}
'
```

*동적생성 필드 처리 옵션*
  - true : 새로 추가되는 필드를 매핑에 추가한다.
  - false : 새로 추가되는 필드를 무시한다. 해당 필드는 색인되지 않아 검색할 수 없지만 _source에는 표시된다.
  - strict : 새로운 필드가 감지되면 예외가 발생하고 문서 자체가 색인되지 않는다.

#### enabled
검색 결과에는 포함하지만 색인은 하고 싶지 않은 경우 사용


#### format
날짜 포멧 설정한다.

```sh
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "date": {
        "type":   "date",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

> *빌트인 formats*   
https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats


#### ignore_above :star:
필드에 저장되는 문자열이 지정한 크기를 넘어서민 `빈 값`으로  색인된다.

#### ignore_malformed
해당 필드에 잘못된 데이터 타입이 들어와 예외가 발생해도 해당 문서를 색인 한다.

#### norms
문서의 _score 값 계산에 필요한 정규화 인수를 사용할지 여부 설정. 기본값 `true`.     _score 계산이 필요없거나 단순 필터링 용도로 사용하는 필드는 비활성화해서 디스크 공간을 절약할 수 있다.

#### null_value
null_value를 설정하면 문서의 값이 null 일 경우 `null_value`에 셋팅된 값으로 저장한다.

#### position_increment_gap
배열(Array) 형태의 데이터를 색인할 때 검색의 정확도를 높이기 위해 제공하는 옵션이다.
필드 데이터 중 단어와 단어 사이의 간격(slop) 을 허용할지를 설정한다. 기본값은 `100` 이다. 검색시 단어와 단어 사이의 간격을 기준으로 일치하는 문서를 찾는 데 필요하다.

#### similarity
유사도 측정 알고리즘을 지정한다.

*유사도 측정 알고리증 종류*
- BM25 : Okapi BM25 알고리즘이다. 엘라스틱서치의 기본 유사도 측정 알고리즘이다.
- classic : TF/IDF 알고리즘, 문서 내 용의의 개수와 전체 용어의 개수를 이용해 유사도 계산
- boolean : 복잡한 수학적 모델을 사용하지 않고 단순히 boolean 연산으로 유사도를 측정한다. score는 검색어 일치 여부에 따라 결정되며, 검색 결과의 일치 여부에 따라 쿼리의 가중치(boost)에 사용된 점수로만 유사도를 계산한다.

#### store
필드의 값을 저장해 결색 결과에 값을 포함하기 위한 매핑 parameter.

#### term_vector
루씬에서 분석된 용어의 정보를 포함할지 여부를 결정하는 매핑 parameter.


## 3.2. 메타 필드

### 3.2.1. _index
인덱스 명

### 3.2.2. _type
ES 최신버전부터는 `_doc` 으로 통일, 컨트롤할 일이 없다 신경쓰지말자. 

### 3.2.3. _id
문서 식별하는 유일한 키

### 3.2.4. _uid
특수한 식별자키 `#`태그를 사용해 `_type`과 `_id` 조합으로 사용한다. 시스템에서 사용하기 때문에 알고만 있자.

### 3.2.5. _source
문서 원본데이터, _reindex API나 스크립트 사용시에 해당 메타필드를 활용할 수 있다.
```sh
POST /_reindex
{
  "source": {
    "index":"movie_search",
    "query": {
      "match":{
        "movieCd": "20173282"
      }
    }
  },
  "dest":{
    "index":"reindex_movie"
  },
  "script":{
    "source":"ctx._source.prdYear++"
  }
}
```
> `script` 필드안에 스크립트 작성 시 `ctx._source.prdYear`를 이용해 데이터에 접근하고 있다.


## 3.3. 필드 데이터 타입
- Keyword, text: 문자열 타입
- date, long, double, integer, boolean, ip: 일반 타입
- 객체 또는 중첩문과 같은 JSON 계층의 특성 타입
- geo_point, geo_shape: 특수한 타입

### 3.3.1. Keyword 데이터 타입
Keyword 데이터 타입은 말 그대로 키워드 형태로 사용할 데이터에 작합한 데이터 타입이다. 별도의 분석기를 거치지 않고 원문 그대로 색인하기 때문에 `특정 코드`나 `키워드` 등 정형화된 콘텐츠에 주로 사용한다.    
ES 의 일부기능은 형태소 분석을 하지 않아야만 사용이 가능한데 이 경우에도 Keyword 타입이 사용된다.

*keyword 타입으로 선언되어야할 항목*
- 검색 시 필터링되는 항목
- 정렬이 필요한 항목
- 집계(Aggregation) 해야 하는 항목

> 만약 `elastic search` 라는 문자열을 keyaword 타입으로 설정되면 `elastic` 이나 `search` 라는 질의로는 절대 검색되지 않는다. 정확히 `elastic search`라고 질의해야만 검색된다.

*keyword 데이터 타입의 주요 파라미터*
- boost: 필드의 가중치로, 검색 결과 정렬에 영향을 준다. 기본값은 `1.0`으로 1보다 크면 `socore`가 높게 오르고, 적으면 낮게 오른다. 이를 이용해 검색에 사용된 키워드와 문서 간의 유사도 스코어 값을 계산할 때 필드의 가중치 값을 얼마나 더 줄 것인지를 판단한다.
**(5.0 버전 이후 부터 index 시 boost 값을 주는 것은 Deprecate 되었다.)**
- doc_values: 필드를 메모리에 로드해 캐시로 사용한다. 기본값은 `true` 다.
- index: 해당 필드를 검색에 사용할지를 설정한다. 기본값은 `true` 다.
- null_value: 기본적으로 엘라스틱서치는 데이터의 값이 없으면 필드를 생성하지 않는다. 데이터의 값이 없는 경우 `null_value` 필드에 넣은 값으로 대체할지를 설정한다.
- store: 필드 값을 필드와 별도로 _source에 저장하고 검색 가능하게 할지를 설정한다. 기본값은 `false` 다.

### 3.3.2. Text 데이터 타입
Text 데이터 타입을 이용하면 색인 시 지정된 분석기가 데이터를 문자열 데이터로 인식하고 이를 분석한다. 기본 분석기는 `Standard Analyzer`를 사용한다. 영화 제목이나 영화의 설명글과 같이 문장의 형태의 데이터에 사용하기 적합한 타입이다.

> 실무에서는 keyword, text 타입 둘다 지정해서 사용한다.

*사용예제*
```json
...
"name": {
    "type": "text",
    "analyzer": "standard",
    "search_analyzer": "standard",
    "index": true,
    "fields": {
      "keyword": {
        "type": "keyword",
        "ignore_above": 256
      }
    },
    "copy_to": "search_string"
  },

...
```

*Text 데이터 타입의 주요 파라미터*
- analyzer:  인덱스와 검색에 사용할 형태소 분석기를 선택한다. 기본값은 `Standard Analyzer` 다.
- boost: 필드의 가중치로, 검색 결과 정렬에 영향을 준다. **(5.0 버전 이후 부터 index 시 boost 값을 주는 것은 Deprecate 되었다.)**
- fielddata: 정렬, 집계, 스크립트 등에서 메모리에 저장된 필드 데이터를 사용할지 설정한다. 기본값은 `false` 다
- index: 해당 필드를 검색에 사용할지 설정한다. 기본값은 `true` 다
> https://www.elastic.co/guide/en/elasticsearch/reference/7.13/text.html 참고

### 3.3.3. Array 데이터 타입
데이터는 대부분 1차원으로 표현되지안 2차원으로 존재하는 경우도 있을 것이다. 예를 들어, 영화 데이터에 `subtitleLang` 필드가 있고 해당 필드에는 개봉 영화의 언어 코드 데이터가 들어있다고 가정해 보자. 언어의 값으로 영어(en)와 한국(ko)라는 두 개의 데이터를 입력하고 싶을 경우 Array 데이터 타입을 사용해야 한다.    
Array 타입은 문자열이나 숫자처럼 일반적인 값을 지정할 수 있지만 객체 형태로도 정의 할 수 있다. 한가지 주의할 점은 Array 타입에 저장되는 값은 모두 같은 타입으로만 구성해야 한다는 점이다.

> 주의! Array는 data type 이 아니다. mapping에서 따로 type을 선언하는 것이 아니고 어떤 data type이든 Array 형태로 저장이 가능하다. 한가지 예로 tags 필드는 `text` 데이터 타입 으로 선언했지만 Array 형태로 저장 가능하다.
(lists 필드도 json 객체 타입으로 선언했지만 Array 형태로 저장된다.)

document 및 index 생성:
```json
PUT my-index-01/_doc/1
{
  "message": "some arrays in this document...",
  "tags":  [ "elasticsearch", "wow" ], 
  "lists": [ 
    {
      "name": "prog_list",
      "description": "programming list"
    },
    {
      "name": "cool_list",
      "description": "cool stuff list"
    }
  ]
}
```

매핑정보 확인:
```json
GET my-index-01/_mapping
{
  "my-index-01" : {
    "mappings" : {
      "properties" : {
        "lists" : {
          "properties" : {
            "description" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "message" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "tags" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}
```

### 3.3.4. Numeric 데이터 타입
- long
- integer
- short
- byte
- double
- float
- half_float

### 3.3.5. Date 데이터 타입
기본 포멧 `yyyy-MM-ddTHH:mm:ssZ`, Data  타입은 다음과 같이 크게 세가지 형태를 제공한다. 세 가지 중 어느 것을 사용해도 내부적으로 `UTC의 밀리초` 단위로 변환해 저장한다.

- 문자열이 포함된 형식: "2018-04-20", "2018/04.20", "2018-04-20 10:50:00", "2018/04/20 10:50:00"
- ISO_INSTANT 포멧: "2018-04-20T10:50:00Z"
- 밀리초: 1524449145579

### 3.3.6. Range 데이터 타입
- integer_range
- float_range
- long_range
- double_range
- date_range
- ip_range

### 3.3.7. Boolean 데이터 타입
- true, "true"
- false, "false"

### 3.3.8. Geo-Point 데이터 타입

맵핑 선언: 
```json
PUT movie_text/_mapping/_doc
{
  "properties": {
    "check": {
      "type": "boolean"
    }
  }
}
```

데이터 입력:
```json
PUT movie_search_datatype/_doc/3
{
  "title": "해리포터와 마법사의 돌",
  "filmLocation":{
    "lat": 55.4155828,
    "lon": -1.7081091
  }
}
```

### 3.3.9. IP 데이터 타입
IP 주소를 저장하는데 사용, IPv4나 IPv6 모두 지정할 수 있다.

### 3.3.10. Object 데이터 타입
Array 데이터 형태로 저장된 리스트(이하 "Object 형태의 입력 참조")는 검색시(이하 "Object 형태의 입력 및 검색") `OR` 조건을 통해서 검색된다.

Object 형태의 입력 및 검색: 
```json
PUT movie_search_datatype/_doc/7
{
  "title": "해리포터와 마법사의 돌",
  "companies": [
    {
      "companyCd": "1",
      "companyName":"워너브라더스"
    },{
      "companyCd": "2",
      "companyName":"Heyday Films"
    }
  ]
}

GET movie_search_datatype/_search
{
  "query":{
    "bool": {
      "must": [
        {
          "match": {
            "companies.companyName": "워너브라더스"
          }
        }
        ,{
          "match": {
            "companies.companyCd": "2"
          }
        }
      ]
    } 
  }
}
```

### 3.3.11. Nested 데이터 타입
Object 안에 Array 형태로 기록된 정보를 `AND` 조건으로 검색이 가능하게 함

데이터 입력 및 검색:
```json
PUT movie_search_datatype2
{
  "mappings": {
    "properties": {
      "companies_nested": {
        "type": "nested"
      }
    }
  }
}

PUT movie_search_datatype2/_doc/8
{
  "title": "해리포터와 마법사의 돌",
  "companies_nested": [
    {
      "companyCd": "1",
      "companyName":"워너브라더스"
    },{
      "companyCd": "2",
      "companyName":"Heyday Films"
    }
  ]
}

GET movie_search_datatype2/_search
{
  "query":{
    "bool": {
      "must": [
        {
          "match": {
            "companies.companyName": "워너브라더스"
          }
        }
        ,{
          "match": {
            "companies.companyCd": "2"
          }
        }
      ]
    } 
  }
}
```


## 3.4. 엘라스틱서치 분석기
(pass..)
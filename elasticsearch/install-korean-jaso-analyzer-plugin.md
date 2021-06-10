# 검색어 자동완성 플러그인 설치 및 쿼리

참고
- https://www.skyer9.pe.kr/wordpress/?p=1101 (Elasticsearch 자동완성 구현하기)

## Install Korean Jaso Analyzer plugin 설치
1. Korean Jaso Analyzer git clone: https://github.com/jeedy/elasticsearch-jaso-analyzer

```sh
$ git clone https://github.com/netcrazy/elasticsearch-jaso-analyzer.git

```

1. 소스 수정

    git에서 clone 받은 파일은 바로 사용할 수 없다. 설치하려는 ES 버전에 맞춰 metadata를 수정해줘야한다.

    수정되어야할 파일
    - build.gradle
    - src/main/resources/plugin-descriptor.properties

```sh
$ cd elasticsearch-jaso-analyzer
# ES version 수정
$ vim ./build.gradle
$ vim ./src/main/resources/plugin-descriptor.properties
```

1.  grandle build 및 배포
소스 빌드하고 결과물을 ES서버에 복사한다.
```sh
$ gradle build buildPluginZip

$ scp -i ~/.ssh/id_rsa ./build/distributions/jaso-analyzer-plugin-7.10.2-plugin.zip ec2-user@172.17.0.2:/home/ec2-user
```

1. plugin 설치
```sh
# ES 서버 접속
$ ssh -i ~/.ssh/id_rsa ec2-user@172.17.0.2

# ES가 설치된 디렉토리로 이동
$ cd /usr/lib/elasticsearch

$ sudo bin/elasticsearch-plugin install file:///home/ec2-user/jaso-analyzer-plugin-7.10.2-plugin.zip
-> Installing file:///home/ec2-user/jaso-analyzer-plugin-7.10.2-plugin.zip
-> Downloading file:///home/ec2-user/jaso-analyzer-plugin-7.10.2-plugin.zip
[=================================================] 100%?? 
-> Installed jaso-analyzer

# ES를 재기동, 직접 restart 를 해도 되고 사용하는 process control tool를 이용하면 된다.
$ supervisorctl restart elasticsearch
```


## Indexing mapper
```sh
$ curl --location --request PUT 'http://172.17.0.2:9200/hotel_auto_complete?pretty' --data-raw '이하 json 참조'

```

--data-raw:
```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
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
            "filter": ["suggest_filter"]
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
      },
      // (...이하 생략)
    }
  }
}
```

## query
```sh
curl --location --request POST 'http://172.17.0.2:9200/hotel_auto_complete/_search?pretty' --data-raw '이하 json 참조' 
```

--data-raw:
```json
{
    "from": 0,
    "size": 30,
    "query": {
        "script_score": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "search_string.jaso": {
                                    "query": "그랜드",
                                    "analyzer": "suggest_search_analyzer"
                                }
                            }
                        },
                        {
                            "match": {
                                "search_string.jaso": {
                                    "query": "하얏트",
                                    "analyzer": "suggest_search_analyzer"
                                }
                            }
                        },
                        {
                            "match": {
                                "search_string.jaso": {
                                    "query": "리젠시",
                                    "analyzer": "suggest_search_analyzer"
                                }
                            }
                        }
                    ],
                    "should": [
                        {
                            "match": {
                                "search_string.ngram": {
                                    "query": "그랜드",
                                    "analyzer": "my_ngram_analyzer"
                                }
                            }
                        },
                        {
                            "match": {
                                "search_string.ngram": {
                                    "query": "하얏트",
                                    "analyzer": "my_ngram_analyzer"
                                }
                            }
                        },
                        {
                            "match": {
                                "search_string.ngram": {
                                    "query": "리젠시",
                                    "analyzer": "my_ngram_analyzer"
                                }
                            }
                        }
                    ]
                }
            },
            "script": {
                "lang": "painless",
                "source": "params.month*doc['segment.default.monthly'].value + params.leadTime*doc['segment.default.lt10'].value + params.profit*doc['segment.default.profit'].value + params.priceship*doc['priceship'].value + params.promotion*doc['promotion'].value",
                "params": {
                    "month": 100,
                    "leadTime": 10,
                    "profit": 0.001,
                    "priceship": 0.5,
                    "promotion": 1000
                }
            }
        }
    }
}
```




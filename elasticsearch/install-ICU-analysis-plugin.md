# 검색어 오타 교정

참고
- https://danawalab.github.io/elastic/2020/05/21/Elasticsearch-SuggestApi.html (엘라스틱서치 오타교정 API 만들어보기)

## ICU Analysis Plugin 설치
ES에서 지원하는 plugin 이므로 소스 다운로드나  빌드 없이 바로 설치 가능하다.

```sh
# ES 서버 접속
$ ssh -i ~/.ssh/id_rsa ec2-user@172.17.0.2

# ES가 설치된 디렉토리로 이동
$ cd /usr/lib/elasticsearch

$ sudo bin/elasticsearch-plugin install analysis-icu
-> Installing analysis-icu
-> Downloading analysis-icu from elastic
[=================================================] 100%?? 
-> Installed analysis-icu

# ES를 재기동, 직접 restart 를 해도 되고 사용하는 process control tool를 이용하면 된다.
$ sudo supervisorctl restart elasticsearch
```

## Indexing mapper
```sh
$ curl --location --request PUT 'http://172.17.0.2:9200/spell-check?pretty' --data-raw '이하 json 참조'

```

--data-raw:
```json
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "index": {
            "analysis": {
                "filter": {
                    "my_filter": {
                        "mode": "decompose",
                        "name": "nfc",
                        "type": "icu_normalizer"
                    }
                },
                "analyzer": {
                    "nfd_analyzer": {
                        "filter": [
                            "lowercase"
                        ],
                        "char_filter": [
                            "nfd_normalizer"
                        ],
                        "tokenizer": "standard"
                    }
                },
                "char_filter": {
                    "nfd_normalizer": {
                        "mode": "decompose",
                        "name": "nfc",
                        "type": "icu_normalizer"
                    }
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    },
                    "spell": {
                        "type": "text",
                        "analyzer": "nfd_analyzer"
                    }
                }
            }
        }
    }
}
```

## query
```sh
curl --location --request POST 'http://172.17.0.2:9200/spell-check/_search?pretty' --data-raw '이하 json 참조' 
```

--data-raw:
```json
{
    "suggest": {
        "my-suggestion": {
            "text": "쟈전거",
            "term": {
                "field": "title.spell",
                "string_distance": "jaro_winkler"
            }
        }
    }
}
```




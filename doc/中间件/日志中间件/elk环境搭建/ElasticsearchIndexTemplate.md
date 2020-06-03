## [初探 Elasticsearch Index Template（索引模板)](https://www.jianshu.com/p/1f67e4436c37)
```java
{
  "order": 0,
  "template": "sample_info*",
  "settings": {
    "index": {
      "number_of_shards": "64",
      "number_of_replicas": "1"
    }
  },
  "mappings": {
    "info": {
      "dynamic_templates": [
        {
          "string_fields": {
            "mapping": {
              "analyzer": "only_words_analyzer",
              "index": "analyzed",
              "type": "string",
              "fields": {
                "raw": {
                  "ignore_above": 512,
                  "index": "not_analyzed",
                  "type": "string"
                }
              }
            },
            "match_mapping_type": "string",
            "match": "*"
          }
        }
      ]，
    "properties": {
        "user_province": {
          "analyzer": "lowercase_analyzer",
          "index": "analyzed",
          "type": "string",
          "fields": {
            "raw": {
              "ignore_above": 512,
              "index": "not_analyzed",
              "type": "string"
            }
          }
        }
      }
    }
  },
  "aliases": {}
}
```

* 上述模板定义，看似复杂，拆分来看，主要为如下几个部分：
```text
{
  "order": 0,                               // 模板优先级
  "template": "sample_info*",               // 模板匹配的名称方式
  "settings": {...},                        // 索引设置
  "mappings": {...},                        // 索引中各字段的映射定义
  "aliases": {...}                          // 索引的别名
}
```

* 模板优先级
```text
根据order顺序、template合并
```

* 索引模板的匹配

* setting 部分
```text
 setting 部分一般定义的是索引的主分片、拷贝分片、刷新时间、自定义分析器等。常见的 setting 部分结构如下：
"settings": {
    "index": {
      "analysis": {...},                // 自定义的分析器
      "number_of_shards": "32",         // 主分片的个数
      "number_of_replicas": "1",        // 主分片的拷贝分片个数
      "refresh_interval": "5s"          // 刷新时间
    }
  }
```
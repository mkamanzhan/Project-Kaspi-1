# -*- coding: utf-8 -*-
es_index_name = 'project_kaspi_1'

es_models = ["Venue"]

es_mappings = {
    "Venue": {
        "properties" : {
            "name" : {
                "type" : "string",
                "analyzer" : "new_analyzer",
                "search_analyzer": "new_search_analyzer"
            },
            "address" : {
                "type" : "string",
                "analyzer" : "new_analyzer",
                "search_analyzer": "new_search_analyzer"
            },
            "category" : {
                "type" : "string",
                "analyzer" : "new_analyzer",
                "search_analyzer": "new_search_analyzer"
            },
            "tips" : {
                "type" : "string",
                "analyzer" : "new_analyzer",
                "search_analyzer": "new_search_analyzer"
            }
        } 
    }
}



es_ind_settings = {
    "settings": {
        "analysis" : {
            "analyzer" : {
                "new_analyzer" : {
                    "type" : "custom",
                    "tokenizer" : "standard",
                    "filter" : ["my_stopwords", "asciifolding", "lowercase", "worddelimiter", "ngram_filter"]
                },
                "new_search_analyzer" : {
                    "type" : "custom",
                    "tokenizer" : "keyword",
                    "filter" : ["my_stopwords", "asciifolding", "lowercase", "worddelimiter"]
                }
            },
            "filter" : {
                "my_stopwords" : {
                    "type" : "stop",
                    "ignore_case" : True,
                    "stopwords" : ["ул.","р.","пр.","мкр.","просп.","көш.","по","вверх", "для", "на", "то", "у", "в"]
                },
                "snowball" : {#dostaet koren slov
                    "type" : "snowball",
                    "language" : "Russian"
                },
                "stemmer" : {#tozhe dostaet koren slov
                    "type" : "stemmer",
                    "language" : "russian"
                },
                "worddelimiter" : {#izbavlyaetsya ot tochek i prochih
                    "type" : "word_delimiter"
                },
                "ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 3,
                    "max_gram": 20
                }
            }
        }
    }
}

model_es_indices = {
    "Venue": {
        "index_name": "project_kaspi_1",
        "type": "venue"
    }
}



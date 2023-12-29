import json
from collections import OrderedDict
import requests

template_search_url = "https://data.bytedance.net/new_coralng_api/v2/search/template-search"
header = {
    "Content-Type": 'application/json',
    "Authorization": "Basic YWRtaW46YWRtaW4="
}


class DataSearchEngine:
    def __init__(self, top_k=5):
        self.name = 'engine'
        self.top_k = top_k
        self.contents = OrderedDict()

    def search(self, query, business_line="", intention='FIND_TABLE_HIVE_TABLE'):
        search_result = self.template_search(query, business_line, intention)
        return search_result

    def template_search(self, query, business_line, intention="FIND_TABLE_HIVE_TABLE"):
        post_dict = {
            "cid": 0,
            "query": query,
            "limit": 2500,
            "offset": 0,
            "templateName": "CORAL_LLM",
            "attributeValuesMap": {
                "businessLine": [
                    business_line
                ],
                "typeName": ["HiveTable"]
            },    "searchIntention": intention,
        }
        post_dict = json.dumps(post_dict)
        r1 = requests.post(template_search_url, data=post_dict, headers=header)
        res = json.loads(r1.text)
        entities = res['data']['searchDocuments']
        rank = 1
        result_list = []
        for item in entities:
            result = {}
            data = item['entity']['embeddingMetaDataInfo']
            for key in data:
                if key == "hitTermsAnalyzeResult":
                    column_data = data['hitTermsAnalyzeResult']
                    for column_key in column_data:
                        result[column_key] = column_data[column_key]
                else:
                    if key not in result:
                        result[key] = data[key]
            result['rank'] = rank
            rank = rank + 1
            result_list.append(result)
        return result_list

    def search_with_body(self, post_dict):
        post_dict = json.dumps(post_dict)
        r1 = requests.post(template_search_url, data=post_dict, headers=header)
        res = json.loads(r1.text)
        entities = res['data']['searchDocuments']
        rank = 1
        result_list = []
        for item in entities:
            result = {}
            data = item['entity']['embeddingMetaDataInfo']
            for key in data:
                if key == "hitTermsAnalyzeResult":
                    column_data = data['hitTermsAnalyzeResult']
                    for column_key in column_data:
                        result[column_key] = column_data[column_key]
                else:
                    if key not in result:
                        result[key] = data[key]
            result['rank'] = rank
            rank = rank + 1
            result_list.append(result)
        sorted_lst = sorted(result_list, key=lambda x: x['relevanceScore'], reverse=True)
        return result_list[:20]


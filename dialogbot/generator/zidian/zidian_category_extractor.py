import json

import requests


def add_text_to_category(category_dict_l1, category_dict_l2, doc):
    if "business_category" in doc:
        for category in doc['business_category']:
            if "category_name_l1" not in category:
                continue
            l1 = category["category_name_l1"]
            if l1 not in category_dict_l1:
                category_dict_l1[l1] = ""
            category_dict_l1[l1] = category_dict_l1[l1] + " " + doc['property_name_cn']
            if "category_name_l2" not in category:
                continue
            l2 = l1 + "-" + category['category_name_l2']
            if l2 not in category_dict_l2:
                category_dict_l2[l2] = ""
            category_dict_l2[l2] = category_dict_l2[l2] + " " + doc['property_name_cn'] + doc['desc']


def search_zidian(url, headers, body):
    post_dict = json.dumps(body)
    r1 = requests.post(url, data=post_dict, headers=headers)
    res = json.loads(r1.text)
    return res['data']['items']


def save_to_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)


url = "https://zidian.bytedance.net/databook/api/asset/search"
headers = {
    "Cookie": "sessionid=mfc7yi2lpd957woy4v50bl7zbitd0fyu; titan_passport_id=cn/bytedance/830860dd-8a73-496c-87d2-04a5c41ac28b;",
    "Content-Type": "application/json"}
category_dict_l1 = {}
category_dict_l2 = {}
for i in range(50):
    body = {
        "business_category_lv1_id": [],
        "entity_name": [],
        "property_tags": [],
        "refresh_period": [],
        "property_type": 0,
        "property_name": "",
        "field_names": "",
        "ps": 100,
        "pn": i + 1,
        "is_abtest": True,
        "project_key": "webcast",
        "order_type": "corr",
        "business_category_lv1_name": [],
        "business_category_lv2_name": []
    }
    data = search_zidian(url, headers, body)
    for doc in data:
        add_text_to_category(category_dict_l1, category_dict_l2, doc)
save_to_json("data/category_dict_l1.json", category_dict_l1)
save_to_json("data/category_dict_l2.json", category_dict_l2)
print("done")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yaml
import copy
import pymongo
from bson import ObjectId

with open('sa.yml') as f:
    config = yaml.safe_load(f)

mongo = config['mongo']
db = pymongo.MongoClient(mongo['uri'])[mongo['db']]
print('使用的MongoDB: ', mongo['uri'])
custom_rules = db['custom_rules']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Data(BaseModel):
    id: str


class UpdateConf(BaseModel):
    url: str
    method: str
    rule_name: str
    exp: str
    extract_method: str
    crawl_name: str
    current_callback: str
    output: str
    extract_type: str
    crawl_id: int
    content_type: str
    id_to_update: str


@app.get('/api')
def index():
    """
    测试接口是否正常。始终返回

    ```python
    {"success": true, "msg": ""}
    ```

    """
    return {'success': True, 'msg': ''}


def update_info(infoConfig):
    update_form = {}
    if infoConfig.url is not None:
        update_form['rules.url'] = infoConfig.url
    if infoConfig.rule_name is not None:
        update_form['name'] = infoConfig.rule_name
    if infoConfig.method is not None:
        update_form['rules.method'] = infoConfig.method
    if infoConfig.crawl_id is not None:
        crawl_id = infoConfig.crawl_id
        if infoConfig.output is not None:
            update_form[f'parse.crawl.{crawl_id}.output'] = True if infoConfig.output.lower() == 'true' else False
        if infoConfig.extract_type is not None:
            update_form[f'parse.crawl.{crawl_id}.extract'] = infoConfig.extract_type
        if infoConfig.extract_method is not None:
            update_form[f'parse.crawl.{crawl_id}.extract_method'] = infoConfig.extract_method
        if infoConfig.content_type is not None:
            update_form[f'parse.crawl.{crawl_id}.type'] = infoConfig.content_type
        if infoConfig.crawl_name is not None:
            update_form[f'parse.crawl.{crawl_id}.name'] = infoConfig.crawl_name
        if infoConfig.current_callback is not None:
            update_form[f'parse.crawl.{crawl_id}.current_callback'] = infoConfig.current_callback
        if infoConfig.exp is not None:
            update_form[f'parse.crawl.{crawl_id}.exp'] = infoConfig.exp
    if not update_form:
        return {'success': False, 'msg': '没有字段会被更新，请检查字段名是否拼写错误。'}
    update_many = custom_rules.update_many
    update_many({'_id': ObjectId(infoConfig.id_to_update)}, {'$set': update_form}, upsert=False)
    return {'success': True, 'msg': ''}


def delete_seed(rule_id_list):
    print('>>>>>', rule_id_list)
    update_many = custom_rules.update_many
    update_many({'_id': {'$in': [ObjectId(x) for x in rule_id_list]}}, {'$set': {'removed': True}}, upsert=False)
    return {'success': True, 'msg': ''}


@app.get('/api/search')
def search():
    query = {'removed': {'$ne': True}}
    rows = custom_rules.find(query)
    datas = []
    for row in rows:
        row['_id'] = str(row['_id'])
        for i in range(len(row['parse']['crawl'])):
            pre = copy.deepcopy(row)
            pre['parse']['crawl'] = row['parse']['crawl'][i]
            pre['crawl_id'] = i
            datas.append(pre)
    return datas


@app.post('/api/delete')
def delete(data: Data):
    _id = data.id
    delete_seed([_id])
    return {'success': True, 'msg': ''}


@app.post('/api/update1')
def test(data: UpdateConf):
    print(data)
    result = update_info(data)
    return result

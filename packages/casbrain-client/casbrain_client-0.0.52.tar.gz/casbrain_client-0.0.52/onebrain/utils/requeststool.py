import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from onebrain.utils.configtool import OnebrainConfig
num = 0
class RequestsTool():
    TOKEN = None
    def __init__(self, token=None ):
        self.headers = {}
        if token:
            RequestsTool.TOKEN = token
        else:
            of = OnebrainConfig()
            tk = of.get_token()
            RequestsTool.TOKEN = tk

    def set_token(self, token):
        if token:
            self.headers['authorization'] = token

    def _get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'content-type': 'application/json;charset=utf-8'
        }
        if RequestsTool.TOKEN:
            headers['authorization'] = RequestsTool.TOKEN
        for (k, v) in self.headers.items():
            headers[k] = v
        return headers

    def _get_upload_headers(self,data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            "Content-Type": data.content_type
        }
        if RequestsTool.TOKEN:
            headers['authorization'] = RequestsTool.TOKEN
        for (k, v) in self.headers.items():
            headers[k] = v
        return headers

    def _get_url(self, api):
        if api.startswith("http"):
            return api
        else:
            of = OnebrainConfig()
            server = of.get_server()
            if server == None:
                return api
            print(server)
            return server + api

    def add_header(self, key, value):
        self.headers[key] = value

    def get(self, url, params=None):
        response = requests.get(self._get_url(url) , headers=self._get_headers(), params=params)
        self._checkLogin(response.json())
        if 'Authorization' in response.headers:
            token = response.headers['Authorization']
            if token:
                oc = OnebrainConfig()
                oc.set_token(token)
        return response.json()
    

    def post(self, url, data=None):
        response = requests.post(self._get_url(url), headers=self._get_headers(), json=data)
        self._checkLogin(response.json())
        if 'Authorization' in response.headers:
            token = response.headers['Authorization']
            if token:
                oc = OnebrainConfig()
                oc.set_token(token)
        return response.json()

      

    def put(self, url, data=None):
        response = requests.put(self._get_url(url), headers=self._get_headers(), json=data)
        self._checkLogin(response.json())
        if 'Authorization' in response.headers:
            token = response.headers['Authorization']
            if token:
                oc = OnebrainConfig()
                oc.set_token(token)
        return response.json()
    def upload(self, url, data=None):
        response = requests.post(self._get_url(url), headers=self._get_upload_headers(data), data=data)
        self._checkLogin(response.json())
        global num
        num = num + 1
        if num % 100 == 0:
            num = 0
            if 'Authorization' in response.headers:
                token =response.headers['Authorization']
                if token:
                    oc = OnebrainConfig()
                    oc.set_token(token)
        return response.json()
          

    def delete(self, url):
        response = requests.delete(self._get_url(url), headers=self._get_headers())
        self._checkLogin(response.json())
        if 'Authorization' in response.headers:
            token = response.headers['Authorization']
            if token:
                oc = OnebrainConfig()
                oc.set_token(token)
        return response.json()
  

    def _checkLogin(self,re):
        if 'httpCode' in re:
            if re['httpCode'] == 401:
                  raise Exception("没有登录")        

def _test_get(token):
    r = RequestsTool(token)
    _url = " https://api.platform.baai.ac.cn/api/1/project"
    _param = {
        "current": 1,
        "size": 10
    }
    data = r.get(_url, _param)
    print(data)

def _test_post(token):
    r = RequestsTool(token)
    _url = " https://api.platform.baai.ac.cn/api/1/project"
    data = {
        "description": "test",
        "name": "test1",
        "engine": "1",
        id: "4b16c36cff93f3d3f4b71000dbd4fdd0"
    }
    re = r.post(_url, data)
    print(re)

def _test_put(token):
    r = RequestsTool(token)
    _url = " https://api.platform.baai.ac.cn/api/1/project"
    data = {
        "description": "test33333",
        "name": "test333331",
        "engine": "1",
        "id": "4b16c36cff93f3d3f4b71000dbd4fdd0"
    }
    in_json = json.dumps(data)

    re = r.put(_url, in_json)
    print(re)
def _test_delete(token):
    r = RequestsTool(token)
    _url = " https://api.platform.baai.ac.cn/api/1/project/183bc297d6dc29e598416af72459acd0"
    r.delete(_url)

if __name__ == "__main__":

    apiUrl = "/api/1/file/upload?type=dataset&uuid=bfe9b8f8b3ab62ce876069fa71b1eead"
    m = MultipartEncoder(
        fields={'filename': 'test01',
                'version': '10001',
                'file': ('test01.xlsx', 'SDSADASdas',
                                    'application/octet-stream')})


    print('aaa==='+m.content_type)
    r= RequestsTool()
    re = r.upload(apiUrl, data=m)
    print(re)


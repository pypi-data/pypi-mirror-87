import configparser
from onebrain.utils.config import BASE_DIR
INI_FILE ="/.onebrain.ini"
ONEBRAIN = "ONEBRAIN"

def write_config(dic):
    config = configparser.ConfigParser()
    config.add_section(ONEBRAIN)
    for key in dic:
        if dic[key]:
            config.set(ONEBRAIN, key, dic[key])
    config.write(open(BASE_DIR+INI_FILE, "w"))


def read_config():
    config = configparser.ConfigParser()
    config.read(BASE_DIR+INI_FILE, encoding='utf-8')
    dic = dict(config._sections)
    return dic

class OnebrainConfig:
    def __init__(self):
        self.token = None
        self.server = None
        self.organizationId = None
        dic = read_config()
        if ONEBRAIN in dic:
          if 'token' in dic[ONEBRAIN]:
            self.token = dic[ONEBRAIN]['token']
          if 'server'in dic[ONEBRAIN]:
            self.server = dic[ONEBRAIN]['server']
          if 'organizationid' in dic[ONEBRAIN]:
             self.organizationId = dic[ONEBRAIN]['organizationid']
    def _write_config(self):
        dic = dict()
        if self.token:
          dic['token'] = self.token
        if self.server:
          dic['server'] = self.server
        if self.organizationId:
          dic['organizationid'] = self.organizationId
        write_config(dic)

    def set_token(self, token):
        self.token = token
        self._write_config()

    def get_token(self):
        return self.token

    def set_server(self, url):
        self.server = url
        self._write_config()

    def get_server(self):
        return self.server

    def set_organizationId(self, organizationId):
        self.organizationId = organizationId
        self._write_config()

    def get_organizationId(self):
        return self.organizationId

if __name__=='__main__':
    data = {
        'name': 'afas',
        'token': 'afdsafasfdsa'
    }
    write_config(data)
    dic = read_config()
    print(dic)
# FileName : YamlDemo.py
# Author   : Adil
# DateTime : 2017/12/29 12:00
# SoftWare : PyCharm

import yaml
import os

class YamlConfig():
    def load(self,filename):
        f = open(filename, 'r', encoding='utf-8')
        cont = f.read()
        x = yaml.load(cont, Loader=yaml.FullLoader)
        return x
        # print(type(x))
        # print(x)
        # print(x['EMAIL'])
        # print(type(x['EMAIL']))
        # print(x['EMAIL']['Smtp_Server'])
        # print(type(x['EMAIL']['Smtp_Server']))
        # print(x['DB'])
        # print(x['DB']['host'])
        #
        # print(x.get('DB').get('host'))
        #
        # print(type(x.get('DB')))

if __name__ == "__main__":
    yaml_config = YamlConfig()
    yaml_config.load("dataset.yaml")

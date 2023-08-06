#!/usr/bin/python3
import click
from  onebrain.utils.yamltool  import YamlConfig
from   onebrain.utils.requeststool import  RequestsTool
from onebrain.utils.configtool import OnebrainConfig
from onebrain.dataset import DataSet
@click.group()
def onebrain():
    pass

@click.command()
@click.option("-server",  prompt="server", help="the Url of onebrain server")
@click.option("-username", prompt="username",
                  help="username")
@click.option("-password", prompt="password", help="password")
def login(server, username, password):
    base_url = "/api/1/auth/cli/login"
    login_url = server + base_url
    params ={
        "password": password,
        "username": username
    }
    rq = RequestsTool()
    re = rq.post(login_url, params)
    print(re)
    if re['code'] == 200:
        print('token' + re['data']['token'])
        oc = OnebrainConfig()
        oc.set_server(server)
        oc.set_token(re['data']['token'])
    else:
        print(re['msg'])

    return

@click.command()
@click.option("-file",  prompt="filename", help="the filename of config ")
def create(file):
    yaml_config = YamlConfig()
    yaml = yaml_config.load(file)
    if 'kind' in yaml:
      if yaml['kind'].lower() == 'dataset'.lower():
         dataset = DataSet(yaml)
         dataset.create()
    return

@click.command()
@click.option("--f",  prompt="filename", help="the filename of config ")
def update(option ,filename):
    return
@click.command()
@click.option("--f",  prompt="filename", help="the filename of config ")
def delete(option ,filename):
    return
@click.command()
@click.option("-name",  prompt="name", help="the naem of dataset")
def find(name):
    dataset = DataSet()
    dataset.find(name)
onebrain.add_command(login)
onebrain.add_command(create)
onebrain.add_command(update)
onebrain.add_command(delete)
onebrain.add_command(find)
if __name__ == '__main__':
    onebrain()